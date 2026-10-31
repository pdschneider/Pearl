# src/qt_interface/qt_settings/qt_system.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QComboBox
)
from PySide6.QtCore import Qt
import logging
from src.qt_interface.qt_styling import dark


def create_system_settings_tab(globs):
    """
    Create the General Settings tab for Qt interface.
    Returns a QWidget that can be added directly to the tab widget.
    """

    # Create the main widget that will BE the tab
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)
    layout.setAlignment(Qt.AlignTop)

    # Title
    title = QLabel("System Settings")
    title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
    layout.addWidget(title)

    # Logging Level
    logging_layout = QHBoxLayout()

    logging_label = QLabel()
    logging_label.setText("Logging Level: ")
    logging_layout.addWidget(logging_label)

    logging_levels = ["Debug", "Info", "Warning", "Error", "Critical"]
    globs.logging_level_box = QComboBox()
    globs.logging_level_box.addItems(logging_levels)
    globs.logging_level_box.setFixedWidth(100)
    globs.logging_level_box.setCurrentText(globs.logging_level.capitalize())
    globs.logging_level_box.setStyleSheet(dark.combobox)
    logging_layout.addWidget(globs.logging_level_box)

    # Add some spacer at the bottom so it doesn't hug the edge
    logging_layout.addStretch()

    layout.addLayout(logging_layout)

    return tab_widget
