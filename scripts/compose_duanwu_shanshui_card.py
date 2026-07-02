from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BACKGROUND = Path("/Users/mima0000/Downloads/已生成图像 1.png")
LOGO = ROOT / "images" / "logo.png"
OUT = ROOT / "images" / "duanwu-2026-shanshui-card.png"

W, H = 1080, 1920
SCALE = 2

FONT_KAITI = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/88d6cc32a907955efa1d014207889413890573be.asset/AssetData/Kaiti.ttc"
FONT_HEITI = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_SONGTI = "/System/Library/Fonts/Supplemental/Songti.ttc"
FONT_TIMES = "/System/Library/Fonts/Times.ttc"


def sx(value: float) -> int:
    return int(round(value * SCALE))


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size * SCALE, index=index)


def cover(src: Image.Image, size: tuple[int, int]) -> Image.Image:
    sw, sh = src.size
    tw, th = size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    img = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def centered_text(draw: ImageDraw.ImageDraw, y: int, text: str, fnt, fill):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    x = (W * SCALE - (bbox[2] - bbox[0])) // 2
    draw.text((x, sx(y)), text, font=fnt, fill=fill)


def text_at(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, fnt, fill):
    draw.text((sx(x), sx(y)), text, font=fnt, fill=fill)


def vertical_text(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, fnt, fill, gap: int = -18):
    cy = sx(y)
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=fnt)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((sx(x) - tw // 2, cy), ch, font=fnt, fill=fill)
        cy += th + sx(gap)


def recolored_logo(color=(23, 61, 49), width=240) -> Image.Image:
    logo = Image.open(LOGO).convert("RGBA")
    bbox = logo.getbbox()
    logo = logo.crop(bbox)
    # Keep the mark and English name, then redraw the Chinese firm name below
    # so the card clearly says this is a U.S. law firm.
    logo = logo.crop((0, 0, logo.width, int(logo.height * 0.845)))
    alpha = logo.getchannel("A")
    solid = Image.new("RGBA", logo.size, (*color, 255))
    solid.putalpha(alpha)
    logo_w = sx(width)
    logo_h = int(solid.height * logo_w / solid.width)
    return solid.resize((logo_w, logo_h), Image.Resampling.LANCZOS)


def subtle_shadow_text(draw, pos, text, fnt, fill, shadow=(255, 255, 246, 90), offset=(3, 4)):
    x, y = pos
    draw.text((x + sx(offset[0]), y + sx(offset[1])), text, font=fnt, fill=shadow)
    draw.text((x, y), text, font=fnt, fill=fill)


def centered_text_at(draw: ImageDraw.ImageDraw, center_x: int, y: int, text: str, fnt, fill):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text((sx(center_x) - tw // 2, sx(y)), text, font=fnt, fill=fill)


def main():
    bg = Image.open(BACKGROUND).convert("RGB")
    img = cover(bg, (W * SCALE, H * SCALE)).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    # Slight translucent washes keep text legible while preserving the generated painting.
    top_wash = Image.new("RGBA", img.size, (0, 0, 0, 0))
    twd = ImageDraw.Draw(top_wash, "RGBA")
    for y in range(0, sx(920)):
        alpha = int(32 * (1 - y / sx(920)))
        twd.line([(0, y), (W * SCALE, y)], fill=(255, 250, 234, alpha))
    img = Image.alpha_composite(img, top_wash)

    bottom_wash = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bwd = ImageDraw.Draw(bottom_wash, "RGBA")
    for y in range(sx(1260), H * SCALE):
        alpha = int(112 * ((y - sx(1260)) / (H * SCALE - sx(1260))))
        bwd.line([(0, y), (W * SCALE, y)], fill=(7, 49, 35, alpha))
    img = Image.alpha_composite(img, bottom_wash)
    draw = ImageDraw.Draw(img, "RGBA")

    logo_x = 78
    logo_w = 226
    img.alpha_composite(recolored_logo(width=logo_w), (sx(logo_x), sx(78)))
    brand_cn = font(FONT_HEITI, 19)
    centered_text_at(draw, logo_x + logo_w // 2, 258, "美国博衡律师事务所", brand_cn, (23, 61, 49, 238))

    calligraphy = font(FONT_KAITI, 170)
    vertical_text(draw, 540, 314, "端午", calligraphy, (18, 50, 40, 232), gap=20)

    small_cn = font(FONT_KAITI, 56)
    centered_text(draw, 710, "安 康", small_cn, (24, 74, 55, 214))
    draw.line([(sx(474), sx(812)), (sx(606), sx(812))], fill=(174, 139, 72, 135), width=sx(2))

    serif_big = font(FONT_TIMES, 67, index=0)
    serif_mid = font(FONT_TIMES, 74, index=0)
    serif_year = font(FONT_TIMES, 64, index=0)
    text_at(draw, 120, 1398, "DRAGON BOAT", serif_big, (255, 255, 244, 236))
    text_at(draw, 180, 1488, "FESTIVAL", serif_mid, (255, 255, 244, 236))
    text_at(draw, 338, 1592, "2026", serif_year, (255, 255, 244, 224))

    blessing = font(FONT_SONGTI, 40, index=0)
    centered_text(draw, 1732, "粽 叶 盈 香    法 意 长 宁", blessing, (255, 252, 232, 226))

    contact = font(FONT_TIMES, 26, index=0)
    centered_text(draw, 1818, "www.cathaypraxislaw.com  |  info@cathaypraxislaw.com", contact, (255, 252, 232, 206))

    img = img.resize((W, H), Image.Resampling.LANCZOS).convert("RGB")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=96)
    print(OUT)


if __name__ == "__main__":
    main()
