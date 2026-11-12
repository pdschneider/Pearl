from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox
)
from PySide6.QtCore import Qt
from src.qt_interface.qt_styling import dark


def create_tools_settings_tab(globs):
    """
    Create the Tools Settings tab for Qt interface.
    Returns a QWidget that can be added directly to the tab widget.
    """

    # Main Widget
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)
    layout.setAlignment(Qt.AlignTop)

    # Title
    title = QLabel("Tools")
    title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
    layout.addWidget(title)

    # Password Generator toggle
    globs.password_generator_checkbox = QCheckBox("Password Generation")
    globs.password_generator_checkbox.setStyleSheet(dark.settings_checkbox)
    globs.password_generator_checkbox.setChecked(globs.password_generator)
    layout.addWidget(globs.password_generator_checkbox)

    return tab_widget
