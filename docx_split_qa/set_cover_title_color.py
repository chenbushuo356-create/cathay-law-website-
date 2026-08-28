from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree

DOCUMENT = Path("docx_split_qa/Cathay_Praxis_Law_Firm_Profile_Chinese.docx")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


with ZipFile(DOCUMENT) as source:
    files = {item.filename: source.read(item.filename) for item in source.infolist()}

root = etree.fromstring(files["word/document.xml"])
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
        color.attrib.pop(f"{{{W}}}themeColor", None)
        color.attrib.pop(f"{{{W}}}themeShade", None)
        color.attrib.pop(f"{{{W}}}themeTint", None)
    break
else:
    raise RuntimeError("Cover title not found")

files["word/document.xml"] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
with NamedTemporaryFile(dir=DOCUMENT.parent, suffix=".docx", delete=False) as temp_file:
    temporary = Path(temp_file.name)
with ZipFile(temporary, "w", ZIP_DEFLATED) as output:
    for name, data in files.items():
        output.writestr(name, data)
temporary.replace(DOCUMENT)
