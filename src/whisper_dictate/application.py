from __future__ import annotations

import ctypes
import sys

from PySide6.QtCore import QLineF, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPalette, QPen, QPixmap
from PySide6.QtWidgets import QApplication

SKRIVI_ICON_SIZES = (16, 20, 24, 32, 48, 64, 128, 256)
SKRIVI_ORANGE = QColor("#F05A24")


def _windows_high_contrast_enabled() -> bool:
    if sys.platform != "win32":
        return False

    class HighContrast(ctypes.Structure):
        _fields_ = (
            ("size", ctypes.c_uint),
            ("flags", ctypes.c_uint),
            ("default_scheme", ctypes.c_wchar_p),
        )

    state = HighContrast(ctypes.sizeof(HighContrast), 0, None)
    try:
        available = ctypes.windll.user32.SystemParametersInfoW(
            0x0042, state.size, ctypes.byref(state), 0
        )
    except AttributeError, OSError:
        return False
    return bool(available and state.flags & 0x00000001)


def _qss_color(color: QColor) -> str:
    """Preserve translucent Windows palette colours in Qt stylesheets."""
    if color.alpha() == 255:
        return color.name()
    return f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()})"


def theme_colors(
    palette: QPalette, *, high_contrast: bool | None = None
) -> dict[str, str]:
    """Return theme colours that yield to Windows accessibility settings."""
    if high_contrast is None:
        high_contrast = _windows_high_contrast_enabled()
    dark = palette.color(QPalette.ColorRole.Window).lightness() < 128

    if high_contrast:
        window = palette.color(QPalette.ColorRole.Window)
        surface = palette.color(QPalette.ColorRole.Base)
        surface_muted = palette.color(QPalette.ColorRole.Button)
        border = palette.color(QPalette.ColorRole.WindowText)
        control_border = border
        text = palette.color(QPalette.ColorRole.WindowText)
        muted = text
        accent = palette.color(QPalette.ColorRole.Highlight)
        accent_textual = accent
        accent_text = palette.color(QPalette.ColorRole.HighlightedText)
        selection = accent
        selection_text = accent_text
        error = text
        success = text
    elif dark:
        window = palette.color(QPalette.ColorRole.Window)
        surface = palette.color(QPalette.ColorRole.Base)
        surface_muted = palette.color(QPalette.ColorRole.AlternateBase)
        border = palette.color(QPalette.ColorRole.Mid)
        control_border = palette.color(QPalette.ColorRole.Midlight)
        text = palette.color(QPalette.ColorRole.WindowText)
        muted = palette.color(QPalette.ColorRole.PlaceholderText)
        accent = QColor("#FF8A5B")
        accent_textual = accent
        accent_text = QColor("#181817")
        selection = palette.color(QPalette.ColorRole.Highlight)
        selection_text = palette.color(QPalette.ColorRole.HighlightedText)
        error = QColor("#FF8B82")
        success = QColor("#65D6A6")
    else:
        window = QColor("#FAF7F2")
        surface = QColor("#FFFDF9")
        surface_muted = QColor("#F3EEE8")
        border = QColor("#D7CEC5")
        control_border = QColor("#92877D")
        text = QColor("#181817")
        muted = QColor("#59544E")
        accent = SKRIVI_ORANGE
        accent_textual = QColor("#C74616")
        accent_text = QColor("#181817")
        selection = QColor("#FFE2D5")
        selection_text = text
        error = QColor("#A9362A")
        success = QColor("#157A52")

    return {
        "window": _qss_color(window),
        "surface": _qss_color(surface),
        "surface_muted": _qss_color(surface_muted),
        "border": _qss_color(border),
        "control_border": _qss_color(control_border),
        "text": _qss_color(text),
        "muted": _qss_color(muted),
        "accent": _qss_color(accent),
        "accent_textual": _qss_color(accent_textual),
        "accent_text": _qss_color(accent_text),
        "selection": _qss_color(selection),
        "selection_text": _qss_color(selection_text),
        "error": _qss_color(error),
        "success": _qss_color(success),
    }


def application_stylesheet(
    palette: QPalette, *, high_contrast: bool | None = None
) -> str:
    """Build a warm Skrivi theme that yields to Windows accessibility colours."""
    colors = theme_colors(palette, high_contrast=high_contrast)
    return f"""
QDialog {{
    background: {colors["window"]};
    color: {colors["text"]};
}}
QWidget#settingsPage, QScrollArea, QScrollArea > QWidget > QWidget {{
    background: transparent;
}}
QLabel, QCheckBox, QTabWidget {{
    color: {colors["text"]};
}}
QLabel[uiRole="eyebrow"] {{
    color: {colors["accent_textual"]};
    font-size: 9pt;
    font-weight: 700;
}}
QLabel[uiRole="windowTitle"] {{
    font-size: 19pt;
    font-weight: 700;
}}
QLabel[uiRole="pageTitle"] {{
    font-size: 16pt;
    font-weight: 700;
}}
QLabel[uiRole="sectionTitle"] {{
    font-size: 11pt;
    font-weight: 700;
}}
QLabel[uiRole="secondary"] {{
    color: {colors["muted"]};
}}
QLabel[uiRole="value"] {{
    font-weight: 650;
}}
QLabel[uiRole="statusBadge"] {{
    background: {colors["surface_muted"]};
    border-radius: 7px;
    padding: 5px 9px;
    font-weight: 650;
}}
QLabel[uiRole="warning"] {{
    background: {colors["surface_muted"]};
    border: 1px solid {colors["error"]};
    border-radius: 8px;
    padding: 10px 12px;
}}
QLabel#statusDot {{
    color: {colors["accent"]};
    font-size: 14pt;
}}
QLabel#statusDot[statusState="ready"] {{ color: {colors["success"]}; }}
QLabel#statusDot[statusState="recording"] {{ color: {colors["error"]}; }}
QLabel#statusDot[statusState="error"],
QLabel#statusDot[statusState="model_error"] {{ color: {colors["error"]}; }}
QFrame[uiRole="card"] {{
    background: {colors["surface"]};
    border: 1px solid {colors["border"]};
    border-radius: 12px;
}}
QFrame[uiRole="quietCard"] {{
    background: {colors["surface_muted"]};
    border: 1px solid {colors["border"]};
    border-radius: 10px;
}}
QTabWidget::pane {{
    border: 0;
    background: transparent;
    top: -1px;
}}
QTabBar::tab {{
    color: {colors["muted"]};
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    margin-right: 4px;
    padding: 9px 15px;
}}
QTabBar::tab:hover {{
    background: {colors["surface_muted"]};
    color: {colors["text"]};
}}
QTabBar::tab:selected {{
    background: {colors["surface"]};
    color: {colors["text"]};
    border-color: {colors["border"]};
    border-bottom: 3px solid {colors["accent"]};
    font-weight: 650;
}}
QPushButton, QComboBox {{
    background: {colors["surface"]};
    color: {colors["text"]};
    border: 1px solid {colors["control_border"]};
    border-radius: 8px;
    padding: 7px 12px;
    min-height: 20px;
}}
QComboBox {{
    padding-right: 28px;
}}
QPushButton:hover, QComboBox:hover {{
    border-color: {colors["accent"]};
}}
QPushButton:focus, QComboBox:focus {{
    border: 2px solid {colors["accent"]};
    padding: 6px 11px;
}}
QPushButton:default, QPushButton[buttonRole="primary"] {{
    background: {colors["accent"]};
    border-color: {colors["accent"]};
    color: {colors["accent_text"]};
    font-weight: 700;
}}
QPushButton[buttonRole="destructive"] {{
    color: {colors["error"]};
}}
QPushButton:disabled, QComboBox:disabled {{
    background: {colors["surface_muted"]};
    color: {colors["muted"]};
    border-color: {colors["border"]};
}}
QCheckBox {{
    spacing: 9px;
    padding: 4px 0;
}}
QProgressBar {{
    background: {colors["surface_muted"]};
    color: {colors["text"]};
    border: 1px solid {colors["border"]};
    border-radius: 7px;
    min-height: 22px;
    text-align: center;
}}
QProgressBar::chunk {{
    background: {colors["accent"]};
    border-radius: 6px;
}}
QMenu {{
    background: {colors["surface"]};
    color: {colors["text"]};
    border: 1px solid {colors["border"]};
}}
QMenu::item {{ padding: 7px 24px; }}
QMenu::item:selected {{
    background: {colors["selection"]};
    color: {colors["selection_text"]};
}}
QToolTip {{
    background: {colors["surface"]};
    color: {colors["text"]};
    border: 1px solid {colors["border"]};
    padding: 5px;
}}
"""


def _skrivi_icon_pixmap(size: int) -> QPixmap:
    """Render the orange dictation microphone at one native icon size."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Same orange and rounded geometry as the companion reader's speaker.
    painter.scale(size / 100, size / 100)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(SKRIVI_ORANGE)
    painter.drawRoundedRect(QRectF(34, 8, 32, 51), 16, 16)
    pen = QPen(SKRIVI_ORANGE, 7)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawArc(QRectF(22, 27, 56, 48), 180 * 16, 180 * 16)
    painter.drawLine(QLineF(22, 42, 22, 51))
    painter.drawLine(QLineF(78, 42, 78, 51))
    painter.drawLine(QLineF(50, 75, 50, 90))
    painter.drawLine(QLineF(35, 90, 65, 90))
    painter.end()
    return pixmap


def skrivi_icon() -> QIcon:
    """Create Skrivi's readable multi-size tray and application icon."""
    icon = QIcon()
    for size in SKRIVI_ICON_SIZES:
        icon.addPixmap(_skrivi_icon_pixmap(size))
    return icon


def create_application(title: str) -> QApplication:
    """Return Skrivi's single Qt application instance."""
    existing = QApplication.instance()
    if existing is not None:
        app = existing
    else:
        app = QApplication(sys.argv)
    app.setApplicationName("Skrivi")
    app.setApplicationDisplayName(title)
    app.setOrganizationName("Skrivi")
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(skrivi_icon())

    def refresh_theme(palette: QPalette) -> None:
        stylesheet = application_stylesheet(palette)
        if app.styleSheet() != stylesheet:
            app.setStyleSheet(stylesheet)

    refresh_theme(app.palette())
    if not getattr(app, "_skrivi_palette_listener", False):
        app.paletteChanged.connect(refresh_theme)
        app._skrivi_palette_listener = True
    return app
