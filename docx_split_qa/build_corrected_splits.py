from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
import re

SOURCE = Path("docx_split_qa/source.docx")
OUTPUTS = {
    "zh": Path("docx_split_qa/Cathay_Praxis_Law_Firm_Profile_Chinese.docx"),
    "en": Path("docx_split_qa/Cathay_Praxis_Law_Firm_Profile_English.docx"),
}
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
NS = {"w": W}


def character_counts(text):
    return (
        sum("\u3400" <= character <= "\u9fff" for character in text),
        sum(character.isascii() and character.isalpha() for character in text),
    )


def remove(node):
    parent = node.getparent()
    if parent is not None:
        parent.remove(node)


def set_run_text(run, text):
    nodes = run.xpath(".//w:t", namespaces=NS)
    if not nodes:
        return
    nodes[0].text = text
    if text.startswith(" ") or text.endswith(" "):
        nodes[0].set(XML_SPACE, "preserve")
    else:
        nodes[0].attrib.pop(XML_SPACE, None)
    for node in nodes[1:]:
        remove(node)


def in_table(paragraph):
    return bool(paragraph.xpath("ancestor::w:tbl", namespaces=NS))


def has_visual(paragraph):
    return bool(paragraph.xpath(".//w:drawing | .//w:pict | .//w:object", namespaces=NS))


def has_page_break(paragraph):
    return bool(
        paragraph.xpath(
            ".//w:br[@w:type='page'] | ./w:pPr/w:pageBreakBefore",
            namespaces=NS,
        )
    )


def language_of_run(text):
    chinese, english = character_counts(text)
    if chinese:
        return "zh" if not english else "mixed"
    if english:
        return "en"
    return "neutral"


def extract_mixed_label(text, target):
    """Split only visibly paired labels; keep Chinese acronyms such as M&A intact."""
    for separator in (r"\s+[/·]\s*", r"\s{2,}(?=[A-Za-z])"):
        match = re.search(separator, text)
        if not match:
            continue
        left, right = text[:match.start()].rstrip(), text[match.end():].lstrip()
        left_chinese, _ = character_counts(left)
        _, right_english = character_counts(right)
        if target == "zh" and left_chinese:
            return left
        if target == "en" and right_english:
            return right
    return text if target == "zh" else ""


def keep_run(run, paragraph, target):
    text = "".join(run.xpath(".//w:t/text()", namespaces=NS))
    if not text:
        return None
    kind = language_of_run(text)
    if kind == target:
        return text
    if kind == "mixed":
        return extract_mixed_label(text, target)
    if kind == "neutral":
        return text
    # Contact-card values and names in a table are language-neutral operational
    # information, even when they are spelled with Latin characters.
    if target == "zh" and in_table(paragraph):
        return text
    return ""


def split_paragraph(paragraph, target):
    runs = list(paragraph.xpath(".//w:r", namespaces=NS))
    kept = {}
    for run in runs:
        text = "".join(run.xpath(".//w:t/text()", namespaces=NS))
        if text:
            kept[id(run)] = bool(keep_run(run, paragraph, target))

    for run in runs:
        text = "".join(run.xpath(".//w:t/text()", namespaces=NS))
        if text:
            value = keep_run(run, paragraph, target)
            if value:
                if value != text:
                    set_run_text(run, value)
            else:
                remove(run)

    # Retain a line break only when it remains between surviving text runs.
    surviving_runs = [run for run in paragraph.xpath(".//w:r", namespaces=NS)]
    for index, run in enumerate(surviving_runs):
        if not run.xpath("./w:br", namespaces=NS):
            continue
        if run.xpath("./w:br[@w:type='page']", namespaces=NS):
            continue
        previous = next((item for item in reversed(surviving_runs[:index]) if "".join(item.xpath(".//w:t/text()", namespaces=NS))), None)
        following = next((item for item in surviving_runs[index + 1:] if "".join(item.xpath(".//w:t/text()", namespaces=NS))), None)
        if previous is None or following is None:
            remove(run)


def split_story(root, target):
    for paragraph in list(root.xpath(".//w:p", namespaces=NS)):
        before = "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))
        if not before.strip():
            continue
        split_paragraph(paragraph, target)
        after = "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))
        if not after.strip() and not has_visual(paragraph) and not has_page_break(paragraph):
            remove(paragraph)


def replace_visible_text(root, replacements):
    for text_node in root.xpath(".//w:t", namespaces=NS):
        text = text_node.text or ""
        for old, new in replacements:
            if old in text:
                text = text.replace(old, new)
        text_node.text = text
        if text.startswith(" ") or text.endswith(" "):
            text_node.set(XML_SPACE, "preserve")


def apply_cover_title_color(root):
    for paragraph in root.xpath(".//w:p", namespaces=NS):
        if "".join(paragraph.xpath(".//w:t/text()", namespaces=NS)) != "博衡律师事务所":
            continue
        for run in paragraph.xpath(".//w:r", namespaces=NS):
            properties = run.find(f"{{{W}}}rPr")
            if properties is None:
                properties = etree.Element(f"{{{W}}}rPr")
                run.insert(0, properties)
            color = properties.find(f"{{{W}}}color")
            if color is None:
                color = etree.SubElement(properties, f"{{{W}}}color")
            color.set(f"{{{W}}}val", "AE8B47")
            for attribute in (f"{{{W}}}themeColor", f"{{{W}}}themeShade", f"{{{W}}}themeTint"):
                color.attrib.pop(attribute, None)
        return
    raise RuntimeError("Chinese cover title not found")


ENGLISH_REVISIONS = [
    ("Dual-Licensed Perspective", "U.S.–China Dual-Jurisdiction Perspective"),
    ("operating across the United States and Asia", "operating across China, the United States, and Asia"),
    ("International Trade & Anti-Dumping Investigations", "International Trade & Anti-Dumping Defense"),
    ("Mingbo Ye is admitted in Texas and California", "Mingbo Ye is admitted to practice in Texas and California"),
    ("Chinese government-sponsored scholar", "China Scholarship Council-sponsored scholar"),
    ("Changsha,china", "Changsha, China"),
    ("Silicon Valley,California", "Silicon Valley, California"),
    ("Core team", "Core Team"),
    ("Lawyers with International Perspective", "Lawyers with an International Perspective"),
    (
        "She has also served as Legal Counsel to MOFCOM’s Trade Remedy Investigation Bureau in CVD proceedings,",
        "She has also served as legal counsel in CVD proceedings before MOFCOM’s Trade Remedy Investigation Bureau,",
    ),
    (
        "Served as Legal Counsel to MOFCOM’s Trade Remedy Investigation Bureau in CVD proceedings,",
        "Served as legal counsel in CVD proceedings before MOFCOM’s Trade Remedy Investigation Bureau,",
    ),
]


with ZipFile(SOURCE) as source:
    source_files = {item.filename: source.read(item.filename) for item in source.infolist()}

for target, output_path in OUTPUTS.items():
    files = dict(source_files)
    for name, data in list(files.items()):
        if not name.startswith("word/") or not name.endswith(".xml"):
            continue
        try:
            root = etree.fromstring(data)
        except etree.XMLSyntaxError:
            continue
        if not root.xpath(".//w:p", namespaces=NS):
            continue
        split_story(root, target)
        if target == "zh" and name == "word/document.xml":
            apply_cover_title_color(root)
        if target == "en":
            replace_visible_text(root, ENGLISH_REVISIONS)
        files[name] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

    with NamedTemporaryFile(dir=output_path.parent, suffix=".docx", delete=False) as temporary_file:
        temporary_path = Path(temporary_file.name)
    with ZipFile(temporary_path, "w", ZIP_DEFLATED) as output:
        for name, data in files.items():
            output.writestr(name, data)
    temporary_path.replace(output_path)
