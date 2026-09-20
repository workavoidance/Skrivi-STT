"""Home, practice and explicit update discovery; no speech content is persisted."""

from __future__ import annotations

import threading

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from whisper_dictate import __version__
from whisper_dictate.audio import microphone_name_from_identifier
from whisper_dictate.hotkeys import hotkey_display_name
from whisper_dictate.i18n import add_interface_language_listener, tr
from whisper_dictate.release_updates import check_release
from whisper_dictate.windows_startup import _running_with_package_identity


class UpdateEvents(QObject):
    result = Signal(str, str)


class UpdateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        self.message = QLabel()
        self.message.setWordWrap(True)
        layout.addWidget(self.message)
        self.notes = QPushButton(tr("Release notes and download"))
        self.notes.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(self.url)))
        layout.addWidget(self.notes)
        self.retry = QPushButton(tr("Check for updates"))
        self.retry.clicked.connect(self.check)
        layout.addWidget(self.retry)
        self.events = UpdateEvents(self)
        self.events.result.connect(self.received)
        self.busy = False
        self.url = "https://github.com/workavoidance/Skrivi-STT/releases"

    def check(self):
        if _running_with_package_identity():
            QDesktopServices.openUrl(QUrl("ms-windows-store://downloadsandupdates"))
            return
        self.setWindowTitle(tr("Check for updates"))
        self.show()
        self.raise_()
        if self.busy:
            return
        self.busy = True
        self.retry.setEnabled(False)
        self.message.setText(tr("Checking for updates…"))

        def work():
            try:
                available = check_release("Skrivi-STT", __version__)
                self.events.result.emit(available or "", "")
            except Exception:
                self.events.result.emit(
                    "",
                    "Could not check for updates. Check your connection and try again.",
                )

        threading.Thread(target=work, daemon=True).start()

    def received(self, version, error):
        self.busy = False
        self.retry.setEnabled(True)
        self.url = "https://github.com/workavoidance/Skrivi-STT/releases" + (
            f"/tag/v{version}" if version else ""
        )
        message = (
            tr(error)
            if error
            else tr("Version {version} is available.", version=version)
            if version
            else tr("You have the latest test release.")
        )
        self.message.setText(
            tr("Installed version: {version} · Test release", version=__version__)
            + "\n\n"
            + message
        )


class HomeWindow(QDialog):
    cancel_requested = Signal()
    retry_requested = Signal()

    def __init__(self, settings_window, store):
        super().__init__()
        self.settings_window = settings_window
        self.store = store
        self.resize(760, 680)
        self.setMinimumSize(640, 520)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 18)
        self.brand = QLabel("Skrivi Snakk")
        self.brand.setProperty("uiRole", "eyebrow")
        layout.addWidget(self.brand)
        self.heading = QLabel(tr("Dictation"))
        self.heading.setProperty("uiRole", "windowTitle")
        layout.addWidget(self.heading)
        self.status = QLabel(tr("Starting"))
        self.status.setWordWrap(True)
        self.status.setAccessibleName(tr("Current status"))
        layout.addWidget(self.status)
        self.summary = QLabel()
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)
        self.guide = QLabel()
        self.guide.setWordWrap(True)
        layout.addWidget(self.guide)
        self.practice = QTextEdit()
        self.practice.setAcceptRichText(False)
        layout.addWidget(self.practice, 1)
        self.notice = QLabel()
        self.notice.setWordWrap(True)
        layout.addWidget(self.notice)
        row = QHBoxLayout()
        self.settings_button = QPushButton()
        self.settings_button.clicked.connect(settings_window.show_settings)
        self.shortcuts_button = QPushButton(tr("Change shortcuts"))
        self.shortcuts_button.clicked.connect(self.change_shortcuts)
        self.help_button = QPushButton(tr("How to use"))
        self.help_button.clicked.connect(lambda: self.introduction(force=True))
        actions = QHBoxLayout()
        actions.addWidget(self.shortcuts_button)
        actions.addWidget(self.help_button)
        actions.addStretch()
        layout.insertLayout(4, actions)
        self.cancel_button = QPushButton()
        self.cancel_button.clicked.connect(self.cancel_requested)
        self.retry_button = QPushButton()
        self.retry_button.clicked.connect(self.retry_requested)
        self.retry_button.hide()
        self.clear_button = QPushButton()
        self.clear_button.clicked.connect(self.practice.clear)
        for button in (
            self.settings_button,
            self.cancel_button,
            self.retry_button,
            self.clear_button,
        ):
            row.addWidget(button)
        layout.addLayout(row)
        from whisper_dictate.ux_helpers import polish

        polish(self)
        add_interface_language_listener(self.refresh)
        self.refresh()

    def refresh(self):
        settings = self.store.load().settings
        self.setWindowTitle("Skrivi Snakk")
        self.brand.setText("Skrivi Snakk")
        self.heading.setText(tr("Speak wherever you write"))
        self.summary.setText(
            tr("Microphone")
            + ": "
            + tr(microphone_name_from_identifier(settings.microphone))
            + "\n"
            + tr("Dictation language")
            + ": "
            + tr(
                {"auto": "Automatic", "no": "Norwegian", "en": "English"}[
                    settings.language.value
                ]
            )
            + "\n"
            + tr("Keyboard shortcut")
            + ": "
            + tr(hotkey_display_name(settings.hotkey))
        )
        self.guide.setText(
            tr(
                "Click where you want to write in any app. "
                "Hold {shortcut}, speak, then release. Esc cancels."
            ).format(shortcut=tr(hotkey_display_name(settings.hotkey)))
        )
        self.shortcuts_button.setText(tr("Change shortcuts"))
        self.help_button.setText(tr("How to use"))
        self.practice.setPlaceholderText(tr("Optional: try dictation here…"))
        self.practice.setAccessibleName(tr("Optional: try dictation here…"))
        self.notice.setText(
            tr(
                "Practice text is not saved and is cleared when this window closes. "
                "Closing the window keeps Skrivi Snakk in the tray."
            )
        )
        self.settings_button.setText(tr("Settings"))
        self.cancel_button.setText(tr("Cancel"))
        self.retry_button.setText(tr("Retry speech model"))
        self.clear_button.setText(tr("Clear"))

    def set_status(self, state, text):
        self.status.setText(text)
        self.cancel_button.setEnabled(state in ("recording", "transcribing"))
        self.retry_button.setVisible(state == "model_error")

    def open(self):
        self.refresh()
        self.showNormal()
        self.raise_()
        self.activateWindow()
        self.introduction()

    def change_shortcuts(self):
        self.settings_window.show_settings()
        self.settings_window.tabs.setCurrentIndex(1)

    def introduction(self, *, force=False):
        from whisper_dictate.ux_helpers import show_welcome

        settings = self.store.load().settings
        show_welcome(
            self,
            "Skrivi Snakk",
            self.store.path.parent / "welcome-v1.done",
            [tr(hotkey_display_name(settings.hotkey))],
            self.change_shortcuts,
            tr,
            force=force,
        )

    def reject(self):
        self.practice.clear()
        self.hide()

    def closeEvent(self, event):
        self.practice.clear()
        self.hide()
        event.ignore()
