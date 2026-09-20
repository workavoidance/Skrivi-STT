import xml.etree.ElementTree as ET
from pathlib import Path

from whisper_dictate.runtime import APP_NAME, DISPLAY_NAME, BuildIdentity
from whisper_dictate.windows_startup import STARTUP_TASK_ID, VALUE_NAME

ROOT = Path(__file__).resolve().parents[1]


def test_snakk_display_name_is_separate_from_stable_identity():
    assert DISPLAY_NAME == "Skrivi Snakk"
    assert BuildIdentity("next", False).title == DISPLAY_NAME
    assert APP_NAME == "Skrivi"
    assert VALUE_NAME == "Skrivi"
    assert STARTUP_TASK_ID == "SkriviStartup"


def test_snakk_installer_renames_only_display_labels():
    script = (ROOT / "installer/Skrivi.iss").read_text(encoding="utf-8")
    assert '#define MyAppName "Skrivi Snakk"' in script
    assert "AppId={{B17E37FA-9342-4B72-96C4-76F57498A44E}" in script
    assert "DefaultDirName={localappdata}\\Programs\\Skrivi" in script
    assert 'Name: "{group}\\Skrivi Snakk"' in script
    assert "CompareText(Link.TargetPath, ExpectedTarget) <> 0" in script
    assert "Check: WantDesktopShortcut" in script


def test_snakk_store_display_names_keep_existing_product_identity():
    manifest = ET.parse(ROOT / "store/AppxManifest.xml").getroot()
    foundation = "{http://schemas.microsoft.com/appx/manifest/foundation/windows10}"
    assert manifest.find(f"{foundation}Identity").get("Name") == "Skrivi.Skrivi"
    for element in manifest.iter():
        if element.tag == f"{foundation}DisplayName":
            assert element.text == "Skrivi Snakk"
        if "DisplayName" in element.attrib:
            assert element.get("DisplayName") == "Skrivi Snakk"
