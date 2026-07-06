from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
import sys

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def fix(source: Path, target: Path):
    with ZipFile(source, "r") as zin:
        xml = zin.read("word/document.xml")
        root = etree.fromstring(xml)
        matches = []
        for p in root.xpath(".//w:p", namespaces=NS):
            text = "".join(p.xpath(".//w:t/text()", namespaces=NS))
            if "核心团队成员" in text and "Core team" in text:
                matches.append(p)
        if len(matches) != 1:
            raise RuntimeError(f"Expected one Core team paragraph, found {len(matches)}")
        p = matches[0]
        page_breaks = p.xpath(".//w:br[@w:type='page']", namespaces=NS)
        if len(page_breaks) != 1:
            raise RuntimeError(f"Expected one page break in Core team paragraph, found {len(page_breaks)}")

        # The existing break sits after the title text, leaving the title alone on
        # the previous page. Move only that break to the start of the same paragraph.
        br = page_breaks[0]
        parent = br.getparent()
        parent.remove(br)
        if len(parent) == 0:
            parent.getparent().remove(parent)
        first_run = p.find(f"{{{W}}}r")
        new_run = etree.Element(f"{{{W}}}r")
        new_break = etree.SubElement(new_run, f"{{{W}}}br")
        new_break.set(f"{{{W}}}type", "page")
        if first_run is None:
            p.append(new_run)
        else:
            p.insert(p.index(first_run), new_run)

        new_xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(target, "w", ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = new_xml if item.filename == "word/document.xml" else zin.read(item.filename)
                zout.writestr(item, data)


if __name__ == "__main__":
    fix(Path(sys.argv[1]), Path(sys.argv[2]))
