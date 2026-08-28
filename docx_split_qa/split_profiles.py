from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
import re

SOURCE = Path("docx_split_qa/source.docx")
OUTPUT_DIR = Path("docx_split_qa")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def counts(text):
    return (
        sum("\u3400" <= char <= "\u9fff" for char in text),
        sum(char.isascii() and char.isalpha() for char in text),
    )


def remove_node(node):
    parent = node.getparent()
    if parent is not None:
        parent.remove(node)


def in_table(paragraph):
    return bool(paragraph.xpath("ancestor::w:tbl", namespaces=NS))


def has_contact_value(text):
    return bool(re.search(r"@|www\.|https?://|\+?\d[\d .()\-]{5,}", text, re.I))


def has_visual(paragraph):
    return bool(paragraph.xpath(".//w:drawing | .//w:pict | .//w:object", namespaces=NS))


def set_run_text(run, value):
    text_nodes = run.xpath(".//w:t", namespaces=NS)
    if not text_nodes:
        return
    text_nodes[0].text = value
    xml_space = "{http://www.w3.org/XML/1998/namespace}space"
    if value.startswith(" ") or value.endswith(" "):
        text_nodes[0].set(xml_space, "preserve")
    else:
        text_nodes[0].attrib.pop(xml_space, None)
    for text_node in text_nodes[1:]:
        remove_node(text_node)


def mixed_part(text, target):
    # A separator denotes two translated labels. Without one, keep the Chinese
    # run intact because it may contain an acronym or a formal English name.
    for pattern in (r"\s+[/·]\s*", r"\s{2,}(?=[A-Za-z])"):
        match = re.search(pattern, text)
        if not match:
            continue
        left, right = text[:match.start()].rstrip(), text[match.end():].lstrip()
        left_cjk, _ = counts(left)
        _, right_ascii = counts(right)
        if target == "zh" and left_cjk:
            return left
        if target == "en" and right_ascii:
            return right
    return text if target == "zh" else ""


def retain_chinese_runs(paragraph):
    # In a Chinese-dominant paragraph, standalone English runs are the adjacent
    # translation. Mixed runs are preserved for names and legal abbreviations.
    for run in list(paragraph.xpath(".//w:r", namespaces=NS)):
        text = "".join(run.xpath(".//w:t/text()", namespaces=NS))
        cjk, ascii_letters = counts(text)
        if ascii_letters and not cjk:
            remove_node(run)


def process_part(root, target):
    for paragraph in list(root.xpath(".//w:p", namespaces=NS)):
        text = "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))
        if not text.strip():
            continue
        cjk, ascii_letters = counts(text)
        if cjk == 0:
            if target != "en" and not in_table(paragraph) and not has_contact_value(text) and not has_visual(paragraph):
                remove_node(paragraph)
            continue
        if ascii_letters == 0:
            if target != "zh" and not has_visual(paragraph):
                remove_node(paragraph)
            continue
        if cjk >= 20:
            if target == "en":
                if not has_visual(paragraph):
                    remove_node(paragraph)
            else:
                retain_chinese_runs(paragraph)
            continue
        # Short bilingual headings, lists, metadata, and table labels.
        for run in list(paragraph.xpath(".//w:r", namespaces=NS)):
            run_text = "".join(run.xpath(".//w:t/text()", namespaces=NS))
            if not run_text:
                if run.xpath("./w:br", namespaces=NS):
                    remove_node(run)
                continue
            run_cjk, run_ascii = counts(run_text)
            if run_cjk and run_ascii:
                value = mixed_part(run_text, target)
                if value:
                    set_run_text(run, value)
                else:
                    remove_node(run)
            elif run_cjk and target != "zh":
                remove_node(run)
            elif run_ascii and target != "en":
                remove_node(run)
        if not "".join(paragraph.xpath(".//w:t/text()", namespaces=NS)).strip() and not has_visual(paragraph):
            remove_node(paragraph)


for target, filename in (("zh", "Cathay_Praxis_Law_Firm_Profile_Chinese.docx"), ("en", "Cathay_Praxis_Law_Firm_Profile_English.docx")):
    with ZipFile(SOURCE) as source:
        files = {item.filename: source.read(item.filename) for item in source.infolist()}
    for name, data in list(files.items()):
        if not name.startswith("word/") or not name.endswith(".xml"):
            continue
        try:
            root = etree.fromstring(data)
        except etree.XMLSyntaxError:
            continue
        if root.xpath(".//w:p", namespaces=NS):
            process_part(root, target)
            files[name] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    with ZipFile(OUTPUT_DIR / filename, "w", ZIP_DEFLATED) as output:
        for name, data in files.items():
            output.writestr(name, data)
