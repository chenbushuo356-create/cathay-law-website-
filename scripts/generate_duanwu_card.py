from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "duanwu-2026-card-minimal.png"
LOGO = ROOT / "images" / "logo.png"

W, H = 1080, 1920
SCALE = 2
random.seed(20260619)


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size * SCALE, index=index)


FONT_HEITI = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_KAITI = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/88d6cc32a907955efa1d014207889413890573be.asset/AssetData/Kaiti.ttc"
FONT_SONGTI = "/System/Library/Fonts/Supplemental/Songti.ttc"
FONT_TIMES = "/System/Library/Fonts/Times.ttc"


def sx(v: float) -> int:
    return int(round(v * SCALE))


def polygon(draw: ImageDraw.ImageDraw, pts, fill):
    draw.polygon([(sx(x), sx(y)) for x, y in pts], fill=fill)


def line(draw: ImageDraw.ImageDraw, pts, fill, width=1):
    draw.line([(sx(x), sx(y)) for x, y in pts], fill=fill, width=sx(width), joint="curve")


def text_center(draw: ImageDraw.ImageDraw, y: int, content: str, fnt, fill, spacing=0):
    bbox = draw.textbbox((0, 0), content, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text(((W * SCALE - tw) // 2, sx(y)), content, font=fnt, fill=fill, spacing=sx(spacing))


def vertical_text(draw: ImageDraw.ImageDraw, x: int, y: int, chars: str, fnt, fill, gap: int = 8):
    cy = sx(y)
    for ch in chars:
        bbox = draw.textbbox((0, 0), ch, font=fnt)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((sx(x) - tw // 2, cy), ch, font=fnt, fill=fill)
        cy += th + sx(gap)


def add_texture(img: Image.Image) -> Image.Image:
    noise = Image.new("L", img.size, 0)
    pix = noise.load()
    for y in range(0, img.height, 2):
        for x in range(0, img.width, 2):
            v = random.randint(0, 26)
            pix[x, y] = v
            if x + 1 < img.width:
                pix[x + 1, y] = v
            if y + 1 < img.height:
                pix[x, y + 1] = v
            if x + 1 < img.width and y + 1 < img.height:
                pix[x + 1, y + 1] = v
    tint = Image.new("RGBA", img.size, (255, 255, 255, 0))
    tint.putalpha(noise.filter(ImageFilter.GaussianBlur(sx(0.6))))
    return Image.alpha_composite(img, tint)


def draw_mist(draw: ImageDraw.ImageDraw, y: int, opacity: int, bands: int = 5):
    for i in range(bands):
        yy = y + i * 24
        pts = []
        for x in range(-80, W + 120, 80):
            pts.append((x, yy + math.sin((x + i * 40) * 0.014) * 12 + random.randint(-7, 7)))
        line(draw, pts, (238, 249, 232, opacity), width=random.randint(15, 28))


def draw_mountains(layer: Image.Image):
    d = ImageDraw.Draw(layer, "RGBA")
    ranges = [
        (330, (203, 229, 205, 185), 0.55),
        (440, (159, 207, 177, 190), 0.75),
        (565, (95, 156, 118, 220), 1.0),
    ]
    for base, color, amp in ranges:
        pts = [(-50, H)]
        for x in range(-50, W + 90, 90):
            peak = base - random.randint(70, int(170 * amp))
            pts.append((x, peak))
            pts.append((x + 45, base + random.randint(-25, 35)))
        pts.append((W + 50, H))
        polygon(d, pts, color)
        for x in range(0, W, 75):
            top = base - random.randint(45, int(135 * amp))
            polygon(d, [(x, base + 20), (x + 25, top), (x + 55, base + 16)], (232, 246, 225, random.randint(35, 70)))
    return layer.filter(ImageFilter.GaussianBlur(sx(0.7)))


def draw_bamboo_leaf(d: ImageDraw.ImageDraw, cx, cy, length, angle, color, alpha=150):
    w = length * 0.16
    dx = math.cos(angle)
    dy = math.sin(angle)
    px = -dy
    py = dx
    p1 = (cx - dx * length * 0.48, cy - dy * length * 0.48)
    p2 = (cx + dx * length * 0.50, cy + dy * length * 0.50)
    pts = [
        (p1[0], p1[1]),
        (cx + px * w, cy + py * w),
        (p2[0], p2[1]),
        (cx - px * w, cy - py * w),
    ]
    polygon(d, pts, (*color, alpha))
    line(d, [p1, p2], (*color, min(255, alpha + 40)), width=1.4)


def draw_boat(d: ImageDraw.ImageDraw):
    # A quiet dragon boat silhouette on the river, used as a festive cue without making the card busy.
    hull = [(210, 1045), (370, 1018), (650, 1025), (815, 1048), (760, 1088), (285, 1086)]
    polygon(d, hull, (37, 86, 57, 230))
    line(d, [(300, 1028), (365, 970), (430, 1024)], (45, 96, 63, 230), width=7)
    line(d, [(722, 1025), (786, 986), (760, 1048)], (45, 96, 63, 230), width=7)
    for x in range(330, 705, 55):
        line(d, [(x, 1010), (x - 18, 935)], (37, 86, 57, 170), width=5)
        polygon(d, [(x - 22, 932), (x + 7, 932), (x - 5, 980)], (214, 166, 79, 190))
    line(d, [(250, 1100), (820, 1100)], (229, 244, 219, 120), width=4)


def draw_zongzi(d: ImageDraw.ImageDraw):
    cx, cy = 805, 1280
    tri = [(cx, cy - 110), (cx - 120, cy + 90), (cx + 125, cy + 75)]
    polygon(d, tri, (42, 111, 70, 238))
    polygon(d, [(cx - 92, cy + 45), (cx, cy - 110), (cx + 10, cy + 92)], (67, 142, 84, 230))
    polygon(d, [(cx + 8, cy + 90), (cx, cy - 110), (cx + 125, cy + 75)], (20, 89, 59, 230))
    line(d, [(cx - 112, cy + 78), (cx + 112, cy - 62)], (232, 223, 173, 210), width=4)
    line(d, [(cx - 88, cy - 26), (cx + 120, cy + 72)], (232, 223, 173, 210), width=4)
    line(d, [(cx - 65, cy + 96), (cx - 5, cy - 103), (cx + 80, cy + 82)], (15, 67, 46, 125), width=3)


def draw_soft_poly(d: ImageDraw.ImageDraw, pts, fill, blur: int = 0):
    layer = Image.new("RGBA", (W * SCALE, H * SCALE), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer, "RGBA")
    polygon(ld, pts, fill)
    if blur:
        layer = layer.filter(ImageFilter.GaussianBlur(sx(blur)))
    return layer


def logo_layer(color=(27, 61, 50), width=235):
    logo = Image.open(LOGO).convert("RGBA")
    bbox = logo.getbbox()
    logo = logo.crop(bbox)
    alpha = logo.getchannel("A")
    logo_color = Image.new("RGBA", logo.size, (*color, 255))
    logo_color.putalpha(alpha)
    logo_w = sx(width)
    logo_h = int(logo_color.height * logo_w / logo_color.width)
    return logo_color.resize((logo_w, logo_h), Image.Resampling.LANCZOS)


def draw_minimal_leaf(d: ImageDraw.ImageDraw):
    # A restrained zongzi-leaf motif: festive, but quiet enough for a law firm greeting.
    base = [(730, 1270), (915, 1118), (1004, 1318), (814, 1468)]
    polygon(d, base, (25, 89, 59, 220))
    polygon(d, [(760, 1288), (914, 1118), (850, 1452)], (56, 126, 79, 205))
    line(d, [(739, 1282), (996, 1316)], (229, 215, 162, 205), width=3)
    line(d, [(807, 1462), (918, 1129)], (229, 215, 162, 170), width=3)
    line(d, [(756, 1388), (940, 1198)], (16, 70, 48, 80), width=2)


def draw_elegant_dragon_boat(d: ImageDraw.ImageDraw):
    ink = (24, 82, 58, 175)
    light = (244, 250, 238, 80)
    gold = (194, 161, 91, 150)

    # Low, quiet dragon-boat silhouette with five rowers.
    hull_top = [(265, 1068), (356, 1048), (655, 1050), (792, 1072)]
    hull_bottom = [(302, 1107), (704, 1109), (820, 1078), (792, 1072), (655, 1090), (356, 1088), (265, 1068)]
    polygon(d, hull_bottom, ink)
    line(d, hull_top, (20, 70, 50, 205), width=4)
    line(d, [(318, 1118), (720, 1120), (825, 1085)], light, width=2)

    # Dragon head and tail, simplified enough not to crowd the composition.
    line(d, [(792, 1072), (850, 1044), (836, 1082), (875, 1086), (819, 1100)], ink, width=4)
    line(d, [(285, 1065), (230, 1038), (260, 1086), (302, 1107)], ink, width=4)
    line(d, [(836, 1061), (858, 1054)], gold, width=2)

    rowers = [370, 430, 492, 555, 618]
    for i, x in enumerate(rowers):
        y = 1043 + (i % 2) * 3
        # Head and body.
        d.ellipse((sx(x - 6), sx(y - 36), sx(x + 6), sx(y - 24)), fill=(22, 75, 54, 170))
        line(d, [(x, y - 22), (x + 10, y + 16)], ink, width=4)
        # Arms and paddle; alternate angles for a rowing rhythm.
        if i % 2 == 0:
            line(d, [(x + 2, y - 8), (x + 36, y - 2), (x + 54, y + 48)], ink, width=3)
            line(d, [(x + 51, y + 46), (x + 66, y + 72)], gold, width=3)
        else:
            line(d, [(x + 2, y - 7), (x - 28, y + 2), (x - 46, y + 48)], ink, width=3)
            line(d, [(x - 44, y + 45), (x - 58, y + 70)], gold, width=3)


def draw_quiet_river_scene(d: ImageDraw.ImageDraw):
    ink = (22, 76, 54, 82)
    pale = (246, 251, 241, 72)
    reed = (23, 83, 56, 132)

    # A calm mid-ground landscape replaces the figurative dragon boat, keeping the card refined.
    line(d, [(210, 1052), (350, 1038), (520, 1050), (705, 1030), (880, 1045)], ink, width=3)
    for y, a, offset in [(1088, 76, 0), (1128, 58, 38), (1172, 46, -18)]:
        line(d, [(170, y), (330, y + 8), (510, y - 6), (700, y + 10), (910, y - 4)], (246, 251, 241, a), width=2)
        line(d, [(260 + offset, y + 24), (420 + offset, y + 18), (595 + offset, y + 28), (760 + offset, y + 20)], pale, width=2)

    # Sparse reeds on the right edge add a natural cue without clutter.
    for x, h, lean in [(846, 72, -18), (874, 98, -8), (902, 82, 14), (930, 118, 7)]:
        line(d, [(x, 1155), (x + lean, 1155 - h)], reed, width=2)
        draw_bamboo_leaf(d, x + lean - 4, 1155 - h - 8, 42, -1.25 if lean < 0 else -1.9, (26, 91, 58), 88)


def main():
    img = Image.new("RGBA", (W * SCALE, H * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    # Premium sage gradient with generous negative space.
    top = (232, 244, 224)
    mid = (179, 219, 194)
    bottom = (17, 80, 55)
    for y in range(H * SCALE):
        t = y / (H * SCALE - 1)
        if t < 0.62:
            u = t / 0.62
            col = tuple(int(top[i] * (1 - u) + mid[i] * u) for i in range(3))
        else:
            u = (t - 0.62) / 0.38
            col = tuple(int(mid[i] * (1 - u) + bottom[i] * u) for i in range(3))
        d.line([(0, y), (W * SCALE, y)], fill=(*col, 255))

    # Soft light bloom in the upper-left, replacing the busy illustrated sky.
    bloom = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(bloom, "RGBA")
    for r, a in [(520, 34), (860, 18), (1160, 8)]:
        bd.ellipse((sx(40 - r), sx(40 - r), sx(40 + r), sx(40 + r)), fill=(252, 242, 199, a))
    bloom = bloom.filter(ImageFilter.GaussianBlur(sx(48)))
    img = Image.alpha_composite(img, bloom)
    d = ImageDraw.Draw(img, "RGBA")

    # Minimal distant mountains, deliberately low contrast.
    mountain_layers = [
        ([(0, 720), (165, 640), (310, 705), (480, 610), (648, 690), (812, 620), (1080, 725), (1080, 1040), (0, 1040)], (110, 163, 129, 52), 8),
        ([(-40, 845), (190, 785), (390, 850), (595, 770), (785, 840), (1035, 790), (1120, 845), (1120, 1140), (-40, 1140)], (52, 122, 83, 67), 10),
    ]
    for pts, fillc, blur in mountain_layers:
        img = Image.alpha_composite(img, draw_soft_poly(d, pts, fillc, blur))
        d = ImageDraw.Draw(img, "RGBA")

    # Quiet river band and a few ink-like ripples.
    river = [(0, 920), (230, 895), (470, 928), (680, 890), (1080, 940), (1080, 1240), (0, 1240)]
    polygon(d, river, (214, 236, 220, 92))
    for y, a, w in [(980, 82, 3), (1055, 64, 2), (1142, 52, 2)]:
        line(d, [(-40, y), (180, y + 14), (385, y - 10), (620, y + 18), (870, y - 6), (1120, y + 10)], (244, 250, 237, a), width=w)

    draw_quiet_river_scene(d)

    # A single statement leaf near the lower right.
    draw_minimal_leaf(d)

    # A dark lower wash gives the English title enough contrast without a hard block.
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    for y in range(sx(1280), H * SCALE):
        a = int(10 + 104 * ((y - sx(1280)) / (H * SCALE - sx(1280))))
        od.line([(0, y), (W * SCALE, y)], fill=(0, 34, 22, a))
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img, "RGBA")

    img.alpha_composite(logo_layer(width=220), (sx(78), sx(74)))
    d = ImageDraw.Draw(img, "RGBA")

    # Main greeting.
    calli = font(FONT_KAITI, 176)
    for off, fill in [((3, 4), (255, 255, 247, 72)), ((0, 0), (19, 51, 42, 235))]:
        vertical_text(d, 544 + off[0], 350 + off[1], "端午", calli, fill, gap=-18)
    sub = font(FONT_KAITI, 58)
    text_center(d, 745, "安 康", sub, (24, 82, 58, 210))
    line(d, [(470, 850), (610, 850)], (184, 158, 88, 130), width=2)

    # English title and year.
    serif_big = font(FONT_TIMES, 78, index=0)
    serif_mid = font(FONT_TIMES, 84, index=0)
    serif_year = font(FONT_TIMES, 68, index=0)
    text_center(d, 1452, "DRAGON BOAT", serif_big, (255, 255, 244, 236))
    text_center(d, 1546, "FESTIVAL", serif_mid, (255, 255, 244, 236))
    text_center(d, 1650, "2026", serif_year, (255, 255, 244, 225))

    zh_line = font(FONT_SONGTI, 42, index=0)
    text_center(d, 1782, "粽 叶 盈 香    法 意 长 宁", zh_line, (248, 247, 229, 214))

    img = add_texture(img)
    img = img.resize((W, H), Image.Resampling.LANCZOS).convert("RGB")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=96)
    print(OUT)


if __name__ == "__main__":
    main()
