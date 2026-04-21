# src/qt_interface/qt_components/qt_top_bar.py
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
import logging

def create_top_bar(globals):
    """Creates the top navigation bar."""
    top_bar_widget = QWidget()
    top_bar_widget.setFixedHeight(50)

    top_bar_layout = QHBoxLayout(top_bar_widget)
    top_bar_layout.setContentsMargins(5, 5, 5, 5)
    top_bar_layout.setSpacing(5)

    # == Left Side ==
    # Hamburger button for calling sidebar
    hamburger_button = QPushButton("☰")
    hamburger_button.setFixedSize(40, 40)
    hamburger_button.setCursor(QCursor(Qt.PointingHandCursor))
    top_bar_layout.addWidget(hamburger_button)

    # New Chat button
    new_chat_button = QPushButton("✎")
    new_chat_button.setFixedSize(40, 40)
    new_chat_button.setCursor(QCursor(Qt.PointingHandCursor))
    top_bar_layout.addWidget(new_chat_button)

    # Stretch Top Bar
    top_bar_layout.addStretch()

    # == Right Side ==
    # Bug Report Button
    bug_button = QPushButton("🐞")
    bug_button.setFixedSize(40,40)
    bug_button.setCursor(QCursor(Qt.PointingHandCursor))
    top_bar_layout.addWidget(bug_button)

    # Settings Button
    settings_button = QPushButton("⚙")
    settings_button.setFixedSize(40,40)
    settings_button.setCursor(QCursor(Qt.PointingHandCursor))
    top_bar_layout.addWidget(settings_button)

    return top_bar_widget