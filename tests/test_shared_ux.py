from __future__ import annotations

from unittest.mock import patch

from test_ui import application

from whisper_dictate.i18n import InterfaceLanguage, set_interface_language
from whisper_dictate.release_updates import select_release
from whisper_dictate.settings import SettingsStore, SettingsWriteError
from whisper_dictate.settings_window import SettingsWindow
from whisper_dictate.support import HomeWindow


def test_test_channel_finds_newer_prerelease_without_offering_downgrade():
    releases = [
        {"tag_name": "v0.2.1"},
        {"tag_name": "v0.4.2", "prerelease": True},
        {"tag_name": "v9.0.0", "draft": True},
        {"tag_name": "v0.5.0-alpha"},
    ]
    assert select_release(releases, "0.4.1", test_releases=True)["tag_name"] == "v0.4.2"
    assert select_release(releases, "0.4.1", test_releases=False) is None
    assert select_release(releases, "0.4.2", test_releases=True) is None


def test_failed_autosave_restores_control_and_preserves_disk(tmp_path):
    application()
    store = SettingsStore(tmp_path / "settings.json")
    window = SettingsWindow(store)
    before = store.load().settings
    with patch.object(
        window, "_save_settings", side_effect=SettingsWriteError("Disk unavailable")
    ):
        window.overlay_checkbox.setChecked(False)
    assert window.overlay_checkbox.isChecked()
    assert store.load().settings == before
    assert not window._warning.isHidden()
    assert "Disk unavailable" in window._warning.text()


def test_language_refresh_never_persists_a_missing_microphone(tmp_path):
    application()
    set_interface_language(InterfaceLanguage.ENGLISH)
    store = SettingsStore(tmp_path / "settings.json")
    window = SettingsWindow(store)
    window.interface_language_combo.setCurrentIndex(
        window.interface_language_combo.findData("nb")
    )
    assert store.load().settings.microphone == "windows_default"
    window.reject()
    assert store.load().settings.interface_language.value == "nb"
    set_interface_language(InterfaceLanguage.ENGLISH)


def test_home_close_clears_practice_and_keeps_settings(tmp_path):
    application()
    store = SettingsStore(tmp_path / "settings.json")
    settings = SettingsWindow(store)
    home = HomeWindow(settings, store)
    home.show()
    home.practice.setPlainText("Private practice text")
    home.close()
    assert not home.isVisible()
    assert not home.practice.toPlainText()
    assert not (tmp_path / "settings.json").exists()
