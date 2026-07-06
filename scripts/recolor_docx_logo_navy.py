from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image
import sys


def recolor(source: Path, target: Path, navy=(14, 41, 65)):
    with ZipFile(source, "r") as zin:
        logo = Image.open(BytesIO(zin.read("word/media/image1.png"))).convert("RGBA")
        pixels = logo.load()
        for y in range(logo.height):
            for x in range(logo.width):
                _, _, _, alpha = pixels[x, y]
                if alpha:
                    pixels[x, y] = (*navy, alpha)
        buffer = BytesIO()
        logo.save(buffer, format="PNG", optimize=True)
        replacement = buffer.getvalue()

        with ZipFile(target, "w", ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = replacement if item.filename == "word/media/image1.png" else zin.read(item.filename)
                zout.writestr(item, data)


if __name__ == "__main__":
    recolor(Path(sys.argv[1]), Path(sys.argv[2]))
