# src/qt_interface/qt_components/qt_top_bar.py
from PySide6.QtWidgets import (QHBoxLayout,
                               QPushButton, QWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
import logging
import sounddevice as sd
from src.qt_interface.qt_components.qt_sidebar import toggle_sidebar
from src.qt_interface.qt_settings.qt_settings import toggle_settings_panel
from src.managers.chat_history import start_new_conversation


def create_top_bar(globs):
    """Creates the top navigation bar."""
    top_bar_widget = QWidget()
    top_bar_widget.setFixedHeight(50)

    top_bar_layout = QHBoxLayout(top_bar_widget)
    top_bar_layout.setContentsMargins(5, 5, 5, 5)
    top_bar_layout.setSpacing(5)

    # Hamburger button for calling sidebar
    hamburger_button = QPushButton("☰")
    hamburger_button.setFixedSize(40, 40)
    hamburger_button.setCursor(QCursor(Qt.PointingHandCursor))
    hamburger_button.clicked.connect(lambda: toggle_sidebar(globs, globs.sidebar))
    top_bar_layout.addWidget(hamburger_button)

    # New Chat button
    new_chat_button = QPushButton("✎  New Chat")
    new_chat_button.setFixedSize(100, 40)
    new_chat_button.setCursor(QCursor(Qt.PointingHandCursor))
    new_chat_button.clicked.connect(lambda: start_new_chat(globs))
    top_bar_layout.addWidget(new_chat_button)

    # Stretch Top Bar
    top_bar_layout.addStretch()

    def start_new_chat(globs):
        """Resets to a new conversation and clears the chat page."""

        # Stop sound
        sd.stop()

        # Start new conversation
        start_new_conversation(globs)

    return top_bar_widget
