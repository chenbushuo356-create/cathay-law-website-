from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from lxml import etree


WORKSPACE = Path(__file__).resolve().parents[1]
OUTPUT_DIR = WORKSPACE / "deliverables"
TEMPLATE = Path("/Users/mima0000/Desktop/CP律所/信纸/CP信纸模版V7.docx")
SOURCES = {
    "SANY_America_External_Counsel_Strategic_Report_Bilingual_CP_Letterhead.docx": Path(
        "/Users/mima0000/Library/Containers/com.tencent.xinWeChat/Data/Documents/"
        "xwechat_files/wxid_hp1zeqv5q9hi22_9c0f/msg/attach/"
        "d1d63bb7e943bcd1586e9b5f1e23994e/2026-07/Rec/d31a0e04a6c522fc/F/0/"
        "SANY_America_External_Counsel_Strategic_Report_Bilingual_20p.docx"
    ),
    "SANY_America_Two_Pillar_Compliance_Framework_CP_Letterhead.docx": Path(
        "/Users/mima0000/Library/Containers/com.tencent.xinWeChat/Data/Documents/"
        "xwechat_files/wxid_hp1zeqv5q9hi22_9c0f/msg/attach/"
        "d1d63bb7e943bcd1586e9b5f1e23994e/2026-07/Rec/d31a0e04a6c522fc/F/1/"
        "SANY_America_Two_Pillar_Compliance_Framework_Internal_Discus.docx"
    ),
}

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"w": W_NS, "r": R_NS}


def source_body_text_hash(path: Path) -> str:
    """Hash the body text nodes only, excluding headers, footers, and metadata."""
    with ZipFile(path) as package:
        root = etree.fromstring(package.read("word/document.xml"))
    body = root.find("w:body", NS)
    text = "\u241e".join(node.text or "" for node in body.iter(qn("w:t")))
    return sha256(text.encode("utf-8")).hexdigest()


def all_cell_paragraphs(table):
    for row in table.rows:
        for cell in row.cells:
            yield from cell.paragraphs
            for nested in cell.tables:
                yield from all_cell_paragraphs(nested)


def all_tables(document):
    """Yield all body and nested tables once."""
    def visit(table):
        yield table
        for row in table.rows:
            for cell in row.cells:
                for nested in cell.tables:
                    yield from visit(nested)

    for top_level in document.tables:
        yield from visit(top_level)


def remove_children(parent, child_tag: str) -> None:
    for child in list(parent):
        if child.tag == qn(child_tag):
            parent.remove(child)


def set_border(borders, edge: str, value: str, size: str = "8") -> None:
    border = borders.find(qn(f"w:{edge}"))
    if border is None:
        border = OxmlElement(f"w:{edge}")
        borders.append(border)
    border.set(qn("w:val"), value)
    border.set(qn("w:sz"), size)
    border.set(qn("w:space"), "0")
    border.set(qn("w:color"), "000000")


def new_borders() -> OxmlElement:
    borders = OxmlElement("w:tblBorders")
    set_border(borders, "top", "single", "12")
    set_border(borders, "left", "nil", "0")
    set_border(borders, "bottom", "single", "12")
    set_border(borders, "right", "nil", "0")
    set_border(borders, "insideH", "nil", "0")
    set_border(borders, "insideV", "nil", "0")
    return borders


def apply_three_line_table(table) -> None:
    """Make a plain black three-line table without touching table text/geometry."""
    table_properties = table._tbl.tblPr
    # Remove the source table style, shading, and colored border definition.
    for tag in ("w:tblStyle", "w:shd", "w:tblBorders"):
        remove_children(table_properties, tag)
    table_properties.append(new_borders())

    # Cell borders/shading override the table settings in Word, so remove them.
    for row in table.rows:
        for cell in row.cells:
            cell_properties = cell._tc.tcPr
            for tag in ("w:shd", "w:tcBorders"):
                remove_children(cell_properties, tag)
            for paragraph in cell.paragraphs:
                paragraph_properties = paragraph._p.pPr
                if paragraph_properties is not None:
                    remove_children(paragraph_properties, "w:shd")

    # The third line is the rule below the header row. A one-row table keeps
    # only its top and bottom rules, as there is no separate header/body split.
    if len(table.rows) > 1:
        for cell in table.rows[0].cells:
            cell_properties = cell._tc.tcPr
            header_borders = OxmlElement("w:tcBorders")
            set_border(header_borders, "bottom", "single", "6")
            cell_properties.append(header_borders)


def set_run_format(run, bold: bool) -> None:
    # STFangsong is the installed Mac 仿宋 face. Using an installed face keeps
    # Chinese glyphs visible in the rendered QA output instead of relying on
    # an unavailable Windows-only 仿宋_GB2312 substitution.
    run.font.name = "STFangsong"
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:ascii"), "STFangsong")
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:hAnsi"), "STFangsong")
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "STFangsong")
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0, 0, 0)
    run.bold = bold
    run.italic = False
    run.underline = False


def is_title_or_heading(paragraph) -> bool:
    style_name = (paragraph.style.name or "").strip().lower()
    return style_name == "title" or style_name == "subtitle" or style_name.startswith("heading")


def format_paragraph(paragraph, bold: bool | None = None) -> None:
    use_bold = is_title_or_heading(paragraph) if bold is None else bold
    for run in paragraph.runs:
        set_run_format(run, use_bold)


def format_report(source: Path, output: Path) -> None:
    source_hash = source_body_text_hash(source)
    document = Document(source)

    # Body paragraphs retain their source sequence, tables, and list numbering.
    for paragraph in document.paragraphs:
        format_paragraph(paragraph)
    for table in all_tables(document):
        for paragraph in all_cell_paragraphs(table):
            format_paragraph(paragraph, bold=False)
        # Multi-row tables conventionally place their field labels in row one.
        if len(table.rows) > 1:
            for cell in table.rows[0].cells:
                for paragraph in cell.paragraphs:
                    format_paragraph(paragraph, bold=True)
        apply_three_line_table(table)

    section = document.sections[0]
    section.top_margin = Inches(1.35)
    section.bottom_margin = Inches(0.80)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    section.header_distance = Inches(0.05)
    section.footer_distance = Inches(0.50)
    section.different_first_page_header_footer = False

    props = document.core_properties
    props.author = "Cathay Praxis Law P.C."
    props.comments = ""
    props.title = ""
    props.subject = ""
    props.keywords = ""
    props.category = ""

    document.save(output)
    install_template_header(output)

    final_hash = source_body_text_hash(output)
    if source_hash != final_hash:
        raise RuntimeError(f"Body text changed in {output.name}: {source_hash} != {final_hash}")


def install_template_header(output: Path) -> None:
    """Inject the intact letterhead header and detach the source report footer."""
    template_parts = {}
    with ZipFile(TEMPLATE) as template_package:
        for part_name in (
            "word/header1.xml",
            "word/_rels/header1.xml.rels",
            "word/media/image1.png",
        ):
            template_parts[part_name] = template_package.read(part_name)

    with ZipFile(output) as package:
        original = {name: package.read(name) for name in package.namelist()}

    document_root = etree.fromstring(original["word/document.xml"])
    for section_properties in document_root.xpath(".//w:sectPr", namespaces=NS):
        for footer_ref in section_properties.findall("w:footerReference", NS):
            section_properties.remove(footer_ref)
    original["word/document.xml"] = etree.tostring(
        document_root, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    # Remove the detached source footer parts and their relationship so the
    # former report branding cannot remain in the delivered package.
    for part_name in ("word/footer1.xml", "word/_rels/footer1.xml.rels"):
        original.pop(part_name, None)
    document_relationships = etree.fromstring(original["word/_rels/document.xml.rels"])
    for relationship in list(document_relationships):
        if relationship.get("Type", "").endswith("/footer"):
            document_relationships.remove(relationship)
    original["word/_rels/document.xml.rels"] = etree.tostring(
        document_relationships, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    original.update(template_parts)

    # The source reports have no images, so their packages may not declare PNG.
    # Preserve the original content-types part and add only the needed default.
    content_types_ns = "http://schemas.openxmlformats.org/package/2006/content-types"
    content_types = etree.fromstring(original["[Content_Types].xml"])
    png_default = content_types.xpath(
        "./ct:Default[@Extension='png']", namespaces={"ct": content_types_ns}
    )
    if not png_default:
        etree.SubElement(
            content_types,
            f"{{{content_types_ns}}}Default",
            Extension="png",
            ContentType="image/png",
        )
        original["[Content_Types].xml"] = etree.tostring(
            content_types, xml_declaration=True, encoding="UTF-8", standalone=True
        )
    for override in list(content_types):
        if override.get("PartName") == "/word/footer1.xml":
            content_types.remove(override)
    original["[Content_Types].xml"] = etree.tostring(
        content_types, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    with NamedTemporaryFile(suffix=".docx", delete=False, dir=output.parent) as temp_file:
        temporary_output = Path(temp_file.name)
    try:
        with ZipFile(temporary_output, "w", ZIP_DEFLATED) as rebuilt:
            for part_name, content in original.items():
                rebuilt.writestr(part_name, content)
        temporary_output.replace(output)
    finally:
        if temporary_output.exists():
            temporary_output.unlink()


def verify(output: Path) -> None:
    with ZipFile(output) as package:
        document_root = etree.fromstring(package.read("word/document.xml"))
        if document_root.xpath(".//w:footerReference", namespaces=NS):
            raise RuntimeError(f"Footer reference remains in {output.name}")
        if package.read("word/header1.xml") != ZipFile(TEMPLATE).read("word/header1.xml"):
            raise RuntimeError(f"Template letterhead was not retained in {output.name}")
        if package.read("word/media/image1.png") != ZipFile(TEMPLATE).read("word/media/image1.png"):
            raise RuntimeError(f"Template logo was not retained in {output.name}")
        if any(part_name.startswith("word/footer") for part_name in package.namelist()):
            raise RuntimeError(f"Source footer package part remains in {output.name}")
    document = Document(output)
    for paragraph in list(document.paragraphs) + [p for table in all_tables(document) for p in all_cell_paragraphs(table)]:
        for run in paragraph.runs:
            if run.font.size is None or run.font.size.pt != 14:
                raise RuntimeError(f"Non-14pt body run found in {output.name}")
            if run.font.color.rgb is None or str(run.font.color.rgb) != "000000":
                raise RuntimeError(f"Non-black body run found in {output.name}")
    for table in all_tables(document):
        if any(True for _ in table._tbl.iter(qn("w:shd"))):
            raise RuntimeError(f"Table shading remains in {output.name}")


def main() -> None:
    expected_template_hash = "031c5582fb24f6863f625fff42826a340ec12ab8c11e51fd8746aaea78f91600"
    if sha256(TEMPLATE.read_bytes()).hexdigest() != expected_template_hash:
        raise RuntimeError("The reference letterhead does not match the distilled template.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for output_name, source in SOURCES.items():
        output = OUTPUT_DIR / output_name
        format_report(source, output)
        verify(output)
        print(f"Created {output}")
        print(f"  body-text-sha256: {source_body_text_hash(output)}")


if __name__ == "__main__":
    main()
