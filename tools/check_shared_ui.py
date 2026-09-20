"""Render the shared UX with disposable preferences, without audio or hotkeys."""

# ruff: noqa: E402
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

os.environ["QT_QPA_PLATFORM"] = "offscreen"
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtGui import QFont, QFontDatabase

from whisper_dictate.application import create_application
from whisper_dictate.i18n import InterfaceLanguage, set_interface_language
from whisper_dictate.settings import SettingsStore
from whisper_dictate.settings_window import SettingsWindow
from whisper_dictate.support import HomeWindow

app = create_application("Skrivi Snakk preview")
QFontDatabase.addApplicationFont(
    str(Path(os.environ["WINDIR"]) / "Fonts" / "segoeui.ttf")
)
app.setFont(QFont("Segoe UI", 10))
output = ROOT / "build" / "ux-preview"
output.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="snakk-ux-") as folder:
    store = SettingsStore(Path(folder) / "settings.json")
    settings = SettingsWindow(store)
    home = HomeWindow(settings, store)
    home.set_status("ready", "Ready to dictate")
    for language in (InterfaceLanguage.ENGLISH, InterfaceLanguage.NORWEGIAN_BOKMAL):
        set_interface_language(language)
        settings.show()
        app.processEvents()
        for index in range(settings.tabs.count()):
            settings.tabs.setCurrentIndex(index)
            app.processEvents()
            settings.grab().save(
                str(output / f"snakk-settings-{language.value}-{index}.png")
            )
        settings.hide()
        home.open()
        app.processEvents()
        home.grab().save(str(output / f"snakk-home-{language.value}.png"))
        home.close()
print("Rendered disposable Snakk home and settings previews in both languages.")
