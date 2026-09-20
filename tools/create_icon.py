"""Generate packaged icons from the same microphone renderer as the live UI."""

import sys
from io import BytesIO
from pathlib import Path

from PIL import Image
from PySide6.QtCore import QBuffer, QIODevice
from PySide6.QtWidgets import QApplication

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from whisper_dictate.application import _skrivi_icon_pixmap  # noqa: E402

STORE_ASSETS = {
    "StoreLogo.png": 50,
    "Square44x44Logo.png": 44,
    "Square150x150Logo.png": 150,
    "Square44x44Logo.targetsize-44_altform-unplated.png": 44,
}


def main() -> None:
    app = QApplication.instance() or QApplication([])
    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    _skrivi_icon_pixmap(1024).save(buffer, "PNG")
    image = Image.open(BytesIO(bytes(buffer.data()))).convert("RGBA")
    output = ROOT / "assets" / "skrivi.ico"
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, sizes=[(s, s) for s in (16, 24, 32, 48, 64, 256)])
    for name, size in STORE_ASSETS.items():
        path = ROOT / "store" / "assets" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        image.resize((size, size), Image.Resampling.LANCZOS).save(path)
    listing = ROOT / "store" / "listing" / "Skrivi-300x300.png"
    listing.parent.mkdir(parents=True, exist_ok=True)
    image.resize((300, 300), Image.Resampling.LANCZOS).save(listing)
    del app


if __name__ == "__main__":
    main()
