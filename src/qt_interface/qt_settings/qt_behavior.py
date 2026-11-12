from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox
    )
from PySide6.QtCore import Qt
from src.qt_interface.qt_styling import dark


def create_behavior_settings_tab(globs):
    """
    Create the Behavior Settings tab for Qt interface.
    Returns a QWidget that can be added directly to the tab widget.
    """

    # Main Widget
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)
    layout.setAlignment(Qt.AlignTop)

    # Title
    title = QLabel("Behavior")
    title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
    layout.addWidget(title)

    # Generate Chat Titles
    chat_titles_layout = QHBoxLayout()
    chat_titles_label = QLabel()
    chat_titles_label.setText("Generate Chat Titles")
    chat_titles_label.setStyleSheet("QLabel { color: white; font-size: 14px; }")
    chat_titles_layout.addWidget(chat_titles_label)

    globs.generate_titles_checkbox = QCheckBox()
    globs.generate_titles_checkbox.setStyleSheet(dark.settings_checkbox)
    globs.generate_titles_checkbox.setChecked(globs.generate_titles)
    chat_titles_layout.addWidget(globs.generate_titles_checkbox)

    chat_titles_layout.addStretch()
    layout.addLayout(chat_titles_layout)

    return tab_widget
