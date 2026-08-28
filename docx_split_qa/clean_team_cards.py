from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"

CHINESE_REPLACEMENTS = {
    "周争平  Zhengping (David) Zhou": "周争平",
    "创始人、执业律师  |  Founder & Attorney": "创始人、执业律师",
    "中国长沙/美国硅谷  ·  Changsha,china & Silicon Valley,California ": "中国长沙/美国硅谷",
    "叶明博  Mingbo Ye": "叶明博",
    "周媛  Yuan Zhou": "周媛",
    "顾问律师  |  Of Counsel": "顾问律师",
}

ENGLISH_REPLACEMENTS = {
    "  Zhengping (David) Zhou": "Zhengping (David) Zhou",
    "  |  Founder & Attorney": "Founder & Attorney",
    "/  ·  Changsha,china & Silicon Valley,California ": "Changsha, China · Silicon Valley, California",
    "  Mingbo Ye": "Mingbo Ye",
    "  Yuan Zhou": "Yuan Zhou",
    "  |  Of Counsel": "Of Counsel",
}


def replace_paragraph(paragraph, value):
    runs = paragraph.xpath("./w:r", namespaces=NS)
    keeper = next((run for run in runs if run.xpath(".//w:t", namespaces=NS)), None)
    if keeper is None:
        raise RuntimeError("A card paragraph unexpectedly had no text run")
    for run in list(runs):
        if run is not keeper:
            paragraph.remove(run)
    text_nodes = keeper.xpath(".//w:t", namespaces=NS)
    text_nodes[0].text = value
    if value.startswith(" ") or value.endswith(" "):
        text_nodes[0].set(XML_SPACE, "preserve")
    else:
        text_nodes[0].attrib.pop(XML_SPACE, None)
    for node in text_nodes[1:]:
        node.getparent().remove(node)


for path, replacements in (
    (Path("docx_split_qa/Cathay_Praxis_Law_Firm_Profile_Chinese.docx"), CHINESE_REPLACEMENTS),
    (Path("docx_split_qa/Cathay_Praxis_Law_Firm_Profile_English.docx"), ENGLISH_REPLACEMENTS),
):
    with ZipFile(path) as source:
        files = {item.filename: source.read(item.filename) for item in source.infolist()}
    root = etree.fromstring(files["word/document.xml"])
    found = {key: 0 for key in replacements}
    for paragraph in root.xpath(".//w:tbl//w:p", namespaces=NS):
        text = "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))
        if text in replacements:
            replace_paragraph(paragraph, replacements[text])
            found[text] += 1
    missing = [key for key, count in found.items() if not count]
    if missing:
        raise RuntimeError(f"Card text was not found: {missing}")
    files["word/document.xml"] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    with NamedTemporaryFile(dir=path.parent, suffix=".docx", delete=False) as temporary_file:
        temporary = Path(temporary_file.name)
    with ZipFile(temporary, "w", ZIP_DEFLATED) as output:
        for name, data in files.items():
            output.writestr(name, data)
    temporary.replace(path)
