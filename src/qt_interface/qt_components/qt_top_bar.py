# src/qt_interface/qt_components/qt_top_bar.py
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
import logging

def create_top_bar(globals, central_widget):
    """Creates the top navigation bar."""
    top_bar_widget = QWidget()
    top_bar = QHBoxLayout(top_bar_widget)
    top_bar.setContentsMargins(0, 0, 0, 5)
    top_bar.setSpacing(5)

    # Hamburger button for calling sidebar
    hamburger_button = QPushButton("☰", central_widget)
    hamburger_button.setFixedSize(40, 40)
    hamburger_button.setCursor(QCursor(Qt.PointingHandCursor))
    top_bar.addWidget(hamburger_button)

    # New Chat button
    new_chat_button = QPushButton("✎", central_widget)
    new_chat_button.setCursor(QCursor(Qt.PointingHandCursor))
    new_chat_button.setFixedSize(40, 40)
    top_bar.addWidget(new_chat_button)

    # Stretch Top Bar
    top_bar.addStretch()

    return top_bar_widget