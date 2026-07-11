from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


def create_appearance_settings_tab(globs):
    """
    Create the Appearance Settings tab for Qt interface.
    Returns a QWidget that can be added directly to the tab widget.
    """

    # Main Widget
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)
    layout.setAlignment(Qt.AlignTop)

    # Title
    title = QLabel("Appearance")
    title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
    layout.addWidget(title)

    return tab_widget
