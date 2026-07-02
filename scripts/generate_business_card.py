#!/usr/bin/env python3
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "business-card"
LOGO = ROOT / "images" / "logo.png"
WECHAT_QR = ROOT / "images" / "wechat-qr-zhengping-zhou.png"

# U.S. business card: 3.5 x 2 in trim, plus 0.125 in bleed on all sides.
TRIM_W, TRIM_H = 3.5 * inch, 2.0 * inch
BLEED = 0.125 * inch
PAGE_W, PAGE_H = TRIM_W + BLEED * 2, TRIM_H + BLEED * 2
SAFE = 0.18 * inch

BRAND_BLUE = colors.HexColor("#16324F")
TEXT = colors.HexColor("#111827")
MUTED = colors.HexColor("#6B7280")
LINE = colors.HexColor("#D1D5DB")
LOGO_FRONT = OUT_DIR / "logo-front-navy.png"
LOGO_FRONT_NO_ZH = OUT_DIR / "logo-front-navy-no-zh.png"

PERSON = {
    "display_name_en": "David Zhengping Zhou",
    "name_en": "David Zhengping Zhou",
    "name_zh": "周争平",
    "title_en": "Founder & Managing Partner",
    "title_zh": "执业律师",
    "firm_en": "Cathay Praxis Law, A Professional Corporation",
    "firm_zh": "美国博衡律师事务所",
    "phone_us": "+1 (341) 2379530",
    "phone_cn": "+86 13975181755",
    "email": "zhengping.zhou@cathaypraxislaw.com",
    "web": "www.cathaypraxislaw.com",
    "wechat": "Zhengping Zhou",
    "address_1": "1259 El Camino Real, Unit 1468",
    "address_2": "Menlo Park, California 94025, USA",
    "bar": "California & PRC Bar",
    "intro": "Cathay Praxis Law is a U.S.-based law firm advising businesses on cross-border transactions, regulatory compliance, international dispute resolution, and U.S.-related legal matters.",
}


def prepare_assets():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    logo = Image.open(LOGO).convert("RGBA")
    alpha = logo.getchannel("A")
    white = Image.new("RGB", logo.size, (255, 255, 255))
    navy = Image.new("RGB", logo.size, (22, 50, 79))
    white.paste(navy, mask=alpha)
    white.save(LOGO_FRONT)
    no_zh = white.copy()
    no_zh.paste((255, 255, 255), (0, 890, no_zh.width, no_zh.height))
    no_zh.save(LOGO_FRONT_NO_ZH)


def register_fonts():
    font_dir = Path("/System/Library/Fonts/Supplemental")
    candidates = {
        "Georgia": font_dir / "Georgia.ttf",
        "Georgia-Bold": font_dir / "Georgia Bold.ttf",
        "Georgia-Italic": font_dir / "Georgia Italic.ttf",
        "ArialUnicode": font_dir / "Arial Unicode.ttf",
    }
    for name, path in candidates.items():
        if path.exists():
            pdfmetrics.registerFont(TTFont(name, str(path)))


def draw_trim_marks(c):
    c.saveState()
    c.setStrokeColor(colors.HexColor("#94A3B8"))
    c.setLineWidth(0.25)
    m = BLEED
    mark = 0.075 * inch
    # Four corner crop marks, outside trim.
    for x in (m, PAGE_W - m):
        c.line(x, 0.03 * inch, x, m - mark)
        c.line(x, PAGE_H - 0.03 * inch, x, PAGE_H - m + mark)
    for y in (m, PAGE_H - m):
        c.line(0.03 * inch, y, m - mark, y)
        c.line(PAGE_W - 0.03 * inch, y, PAGE_W - m + mark, y)
    c.restoreState()


def front(c):
    c.setFillColor(colors.white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    left = BLEED + 0.18 * inch
    right = PAGE_W - BLEED - 0.18 * inch
    top = PAGE_H - BLEED - 0.44 * inch
    bottom = BLEED + 0.18 * inch

    c.setFillColor(TEXT)
    c.setFont("Georgia-Bold", 10.4)
    c.drawString(left, top, PERSON["display_name_en"])
    c.setFont("ArialUnicode", 16.5)
    c.drawString(left, top - 0.29 * inch, PERSON["name_zh"])
    c.setFillColor(TEXT)
    c.setFont("ArialUnicode", 8.2)
    c.drawString(left, top - 0.60 * inch, PERSON["title_en"])

    logo_w = 0.92 * inch
    logo_h = logo_w
    logo_x = right - logo_w
    logo_y = PAGE_H - BLEED - 0.90 * inch
    c.drawImage(str(LOGO_FRONT_NO_ZH), logo_x, logo_y, logo_w, logo_h)
    c.setFillColor(BRAND_BLUE)
    c.setFont("ArialUnicode", 7.2)
    c.drawCentredString(logo_x + logo_w / 2, logo_y - 0.08 * inch, PERSON["firm_zh"])

    address_text = "1259 El Camino Real, Unit 1468, Menlo Park, CA 94025, USA"
    c.setFillColor(TEXT)
    c.setFont("ArialUnicode", 5.2)
    c.drawRightString(right, bottom + 0.42 * inch, address_text)

    c.setStrokeColor(LINE)
    c.setLineWidth(0.35)
    rule_y = bottom + 0.33 * inch
    c.line(BLEED + 0.08 * inch, rule_y, PAGE_W - BLEED - 0.08 * inch, rule_y)

    contact_y = bottom + 0.02 * inch
    columns = [
        ("phone", "M (U.S.)", PERSON["phone_us"], 0.00 * inch, 0.74 * inch),
        ("phone", "M (China)", PERSON["phone_cn"], 0.82 * inch, 0.74 * inch),
        ("mail", "Email", PERSON["email"], 1.65 * inch, 0.92 * inch),
        ("web", "Website", PERSON["web"], 2.58 * inch, 0.72 * inch),
    ]
    for kind, label, value, offset, width in columns:
        draw_contact_item(c, left + offset, contact_y, width, kind, label, value)

    separator_top = contact_y + 0.22 * inch
    separator_bottom = contact_y - 0.05 * inch
    for x in (left + 0.76 * inch, left + 1.58 * inch, left + 2.52 * inch):
        c.setStrokeColor(LINE)
        c.setLineWidth(0.35)
        c.line(x, separator_bottom, x, separator_top)

    draw_trim_marks(c)
    c.showPage()


def info_line(c, x, y, label, value, size=None):
    c.setFillColor(MUTED)
    c.setFont("ArialUnicode", 4.8)
    c.drawString(x, y, label.upper())
    c.setFillColor(TEXT)
    size = size or (5.1 if len(value) > 36 else 6.4)
    c.setFont("ArialUnicode", size)
    c.drawString(x, y - 0.095 * inch, value)


def draw_contact_item(c, x, y, width, kind, label, value):
    icon_r = 0.075 * inch
    icon_x = x + icon_r
    icon_y = y + 0.08 * inch
    c.setFillColor(BRAND_BLUE)
    c.circle(icon_x, icon_y, icon_r, stroke=0, fill=1)
    c.setStrokeColor(colors.white)
    c.setFillColor(colors.white)
    c.setLineWidth(1.0)
    if kind == "phone":
        c.line(icon_x - 0.025 * inch, icon_y + 0.030 * inch, icon_x + 0.025 * inch, icon_y - 0.030 * inch)
        c.circle(icon_x - 0.032 * inch, icon_y + 0.038 * inch, 0.010 * inch, stroke=0, fill=1)
        c.circle(icon_x + 0.032 * inch, icon_y - 0.038 * inch, 0.010 * inch, stroke=0, fill=1)
    elif kind == "mail":
        w, h = 0.095 * inch, 0.065 * inch
        c.rect(icon_x - w / 2, icon_y - h / 2, w, h, stroke=1, fill=0)
        c.line(icon_x - w / 2, icon_y + h / 2, icon_x, icon_y - 0.005 * inch)
        c.line(icon_x + w / 2, icon_y + h / 2, icon_x, icon_y - 0.005 * inch)
    else:
        r = 0.047 * inch
        c.circle(icon_x, icon_y, r, stroke=1, fill=0)
        c.line(icon_x - r, icon_y, icon_x + r, icon_y)
        c.line(icon_x, icon_y - r, icon_x, icon_y + r)
        c.ellipse(icon_x - 0.022 * inch, icon_y - r, icon_x + 0.022 * inch, icon_y + r, stroke=1, fill=0)

    text_x = x + 0.20 * inch
    c.setFillColor(TEXT)
    c.setFont("ArialUnicode", 4.6)
    c.drawString(text_x, y + 0.11 * inch, label.upper())
    value_size = 4.3 if len(value) < 18 else 3.2
    if label.lower() == "email":
        value_size = 2.75
    c.setFont("ArialUnicode", value_size)
    c.drawString(text_x, y + 0.005 * inch, value)


def back(c):
    c.setFillColor(colors.white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    left = BLEED + 0.28 * inch
    right = PAGE_W - BLEED - 0.28 * inch
    top = PAGE_H - BLEED - 0.40 * inch

    c.setFillColor(BRAND_BLUE)
    c.setFont("Georgia-Bold", 12.6)
    c.drawString(left, top, "Cross-Border Counsel")

    c.setFillColor(TEXT)
    c.setFont("ArialUnicode", 6.2)
    text = c.beginText(left, top - 0.31 * inch)
    text.setLeading(8.3)
    text.textLines(
        "Advising businesses on cross-border transactions,\n"
        "U.S. market entry, regulatory compliance, trade controls,\n"
        "economic sanctions, and international dispute resolution."
    )
    c.drawText(text)

    qr_size = 0.56 * inch
    qr_x = right - qr_size
    qr_y = BLEED + 0.35 * inch
    c.drawImage(str(WECHAT_QR), qr_x, qr_y, qr_size, qr_size)
    c.setFillColor(MUTED)
    c.setFont("ArialUnicode", 5.1)
    c.drawRightString(qr_x - 0.10 * inch, qr_y + 0.36 * inch, "WECHAT")
    c.setFillColor(TEXT)
    c.setFont("ArialUnicode", 6.3)
    c.drawRightString(qr_x - 0.10 * inch, qr_y + 0.20 * inch, PERSON["wechat"])

    draw_trim_marks(c)
    c.showPage()


def make_pdf():
    prepare_assets()
    register_fonts()
    path = OUT_DIR / "cathay-praxis-business-card-david-zhou-print.pdf"
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Cathay Praxis Law Business Card - David Zhou")
    front(c)
    back(c)
    c.save()
    return path


def make_html():
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cathay Praxis Law Business Card Preview</title>
  <style>
    :root {{
      --navy: #16324F;
      --muted: #6B7280;
      --line: #D1D5DB;
    }}
    body {{ margin: 0; min-height: 100vh; display: grid; place-items: center; background: #f1f5f9; font-family: Inter, -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; color: var(--navy); }}
    main {{ display: grid; grid-template-columns: repeat(2, minmax(320px, 1fr)); gap: 28px; padding: 36px; }}
    .card {{ width: 3.5in; height: 2in; box-shadow: 0 18px 40px rgba(15, 23, 42, .14); overflow: hidden; position: relative; background: white; }}
    .front {{ background: white; }}
    .front-logo {{ position: absolute; right: .18in; top: .19in; width: .92in; }}
    .front-logo-zh {{ position: absolute; right: .18in; top: .98in; width: .92in; text-align: center; color: var(--navy); font-size: 7.2pt; }}
    .front-name {{ position: absolute; left: .18in; top: .43in; font-family: Georgia, serif; font-weight: 700; font-size: 10.4pt; color: #111827; }}
    .front-zh {{ position: absolute; left: .18in; top: .72in; font-size: 16.5pt; color: #111827; }}
    .front-title {{ position: absolute; left: .18in; top: 1.02in; font-size: 8.2pt; color: #111827; }}
    .front-address {{ position: absolute; right: .18in; bottom: .62in; font-size: 5.2pt; color: #111827; white-space: nowrap; }}
    .front-rule {{ position: absolute; left: .08in; right: .08in; bottom: .51in; height: 1px; background: var(--line); }}
    .front-info {{ position: absolute; left: .18in; right: .18in; bottom: .16in; display: grid; grid-template-columns: .74in .74in .87in .72in; column-gap: .08in; align-items: center; }}
    .front-info .row {{ min-width: 0; position: relative; padding-left: .20in; color: #111827; font-size: 3.5pt; }}
    .front-info .row:not(:last-child)::after {{ content: ""; position: absolute; right: -.04in; top: -.04in; height: .27in; width: 1px; background: var(--line); }}
    .front-info .label {{ margin: 0 0 2px; color: #111827; font-size: 4.6pt; }}
    .front-info .row span:last-child {{ white-space: nowrap; }}
    .front-info .row.phone span:last-child {{ font-size: 4.3pt; }}
    .front-info .row.email span:last-child {{ font-size: 2.75pt; }}
    .front-info .row.web span:last-child {{ font-size: 3.2pt; }}
    .front-info .icon {{ position: absolute; left: 0; top: .005in; width: .15in; height: .15in; border-radius: 999px; background: var(--navy); color: white; display: grid; place-items: center; font-size: 7pt; line-height: 1; }}
    .back {{ padding: .40in .28in; }}
    .content {{ position: relative; z-index: 1; height: 100%; }}
    h1 {{ margin: 0; font-family: Georgia, serif; font-size: 8.8pt; line-height: 1; }}
    .role {{ margin-top: 8px; font-size: 7.2pt; }}
    .corp {{ margin-top: 8px; color: var(--muted); font-size: 5.7pt; }}
    .zh-name {{ position: absolute; right: 0; top: 0; font-family: Inter, -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; font-size: 9.2pt; font-weight: 400; }}
    .firm-zh {{ margin-top: 7px; color: var(--navy); font-size: 6.4pt; }}
    .rule {{ height: 1px; background: var(--line); margin: 14px 0 18px; }}
    .info {{ display: grid; grid-template-columns: 1.54in 1.10in; column-gap: .32in; row-gap: 11px; }}
    .row {{ font-size: 6.4pt; }}
    .row span:last-child {{ font-size: 6.4pt; }}
    .row.long span:last-child {{ font-size: 5.1pt; }}
    .label {{ display: block; margin-bottom: 3px; color: var(--muted); font-size: 4.8pt; text-transform: uppercase; }}
    .address {{ grid-column: 1 / span 2; }}
    .back-title {{ font-family: Georgia, serif; font-weight: 700; font-size: 12.6pt; color: var(--navy); margin: 0 0 .20in; }}
    .back-copy {{ width: 2.20in; font-size: 6.2pt; line-height: 1.34; color: #111827; }}
    .back-qr {{ position: absolute; right: .28in; bottom: .35in; width: .56in; }}
    .back-wechat-label {{ position: absolute; right: .94in; bottom: .71in; font-size: 5.1pt; color: var(--muted); }}
    .back-wechat-id {{ position: absolute; right: .94in; bottom: .55in; font-size: 6.3pt; color: #111827; }}
  </style>
</head>
<body>
  <main>
    <section class="card front">
      <img class="front-logo" src="logo-front-navy-no-zh.png" alt="Cathay Praxis Law">
      <div class="front-logo-zh">{PERSON["firm_zh"]}</div>
      <div class="front-name">{PERSON["display_name_en"]}</div>
      <div class="front-zh">{PERSON["name_zh"]}</div>
      <div class="front-title">{PERSON["title_en"]}</div>
      <div class="front-address">1259 El Camino Real, Unit 1468, Menlo Park, CA 94025, USA</div>
      <div class="front-rule"></div>
      <div class="front-info">
        <div class="row phone"><span class="icon">☎</span><span class="label">M (U.S.)</span><span>{PERSON["phone_us"]}</span></div>
        <div class="row phone"><span class="icon">☎</span><span class="label">M (China)</span><span>{PERSON["phone_cn"]}</span></div>
        <div class="row email"><span class="icon">✉</span><span class="label">Email</span><span>{PERSON["email"]}</span></div>
        <div class="row web"><span class="icon">◎</span><span class="label">Website</span><span>{PERSON["web"]}</span></div>
      </div>
    </section>
    <section class="card back">
      <div class="back-title">Cross-Border Counsel</div>
      <div class="back-copy">Advising businesses on cross-border transactions, U.S. market entry, regulatory compliance, trade controls, economic sanctions, and international dispute resolution.</div>
      <img class="back-qr" src="../../images/wechat-qr-zhengping-zhou.png" alt="WeChat QR">
      <div class="back-wechat-label">WECHAT</div>
      <div class="back-wechat-id">{PERSON["wechat"]}</div>
    </section>
  </main>
</body>
</html>
"""
    path = OUT_DIR / "cathay-praxis-business-card-preview.html"
    path.write_text(html, encoding="utf-8")
    return path


if __name__ == "__main__":
    pdf = make_pdf()
    html = make_html()
    print(pdf)
    print(html)
