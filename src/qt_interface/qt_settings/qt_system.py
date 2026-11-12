# src/qt_interface/qt_settings/qt_system.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QComboBox,
    QLineEdit, QPushButton
)
from PySide6.QtCore import Qt
import logging
from src.utils.qt_save import save_qt_settings
from src.utils.factory_reset import total_factory_reset
from src.connections.ollama import uninstall_ollama
from src.connections.docker import uninstall_docker
from src.connections.kokoro import uninstall_kokoro
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

    # Networking
    net_title = QLabel("Networking")
    net_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
    layout.addWidget(net_title)

    # Ollama chat endpoint
    chat_row = QHBoxLayout()
    chat_row.addWidget(QLabel("Chats: "))
    globs.ollama_chat_path_box = QLineEdit()
    globs.ollama_chat_path_box.setPlaceholderText("http://localhost:11434/")
    globs.ollama_chat_path_box.setFixedWidth(220)
    globs.ollama_chat_path_box.setStyleSheet(dark.line_edit)
    globs.ollama_chat_path_box.setText(globs.ollama_chat_path)
    chat_row.addWidget(globs.ollama_chat_path_box)
    restore_chat_button = QPushButton("Restore Default")
    restore_chat_button.setStyleSheet(dark.settings_button)
    restore_chat_button.clicked.connect(lambda: restore_localhost(globs, "chat"))
    chat_row.addWidget(restore_chat_button)
    chat_row.addStretch()
    layout.addLayout(chat_row)

    # Ollama title endpoint
    title_row = QHBoxLayout()
    title_row.addWidget(QLabel("Chat Titles: "))
    globs.ollama_title_path_box = QLineEdit()
    globs.ollama_title_path_box.setPlaceholderText("http://localhost:11434/")
    globs.ollama_title_path_box.setFixedWidth(220)
    globs.ollama_title_path_box.setStyleSheet(dark.line_edit)
    globs.ollama_title_path_box.setText(globs.ollama_title_path)
    title_row.addWidget(globs.ollama_title_path_box)
    restore_title_button = QPushButton("Restore Default")
    restore_title_button.setStyleSheet(dark.settings_button)
    restore_title_button.clicked.connect(lambda: restore_localhost(globs, "title"))
    title_row.addWidget(restore_title_button)
    title_row.addStretch()
    layout.addLayout(title_row)

    # Danger Zone
    danger_title = QLabel("DANGER ZONE")
    danger_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; background-color: #d62828; padding: 8px; border-radius: 4px;")
    danger_title.setAlignment(Qt.AlignCenter)
    layout.addWidget(danger_title)

    # Factory Reset
    reset_row = QHBoxLayout()
    reset_row.addWidget(QLabel("Factory Reset"))
    reset_button = QPushButton("Reset")
    reset_button.setStyleSheet(dark.danger_button)
    reset_button.clicked.connect(lambda: total_factory_reset(globs))
    reset_row.addWidget(reset_button)
    reset_row.addStretch()
    layout.addLayout(reset_row)

    # Uninstall Ollama
    if globs.ollama_active:
        ollama_row = QHBoxLayout()
        ollama_row.addWidget(QLabel("Uninstall Ollama"))
        ollama_button = QPushButton("Uninstall")
        ollama_button.setStyleSheet(dark.danger_button)
        ollama_button.clicked.connect(lambda: uninstall_ollama(globs))
        ollama_row.addWidget(ollama_button)
        ollama_row.addStretch()
        layout.addLayout(ollama_row)

    # Uninstall Docker
    if globs.docker_active:
        docker_row = QHBoxLayout()
        docker_row.addWidget(QLabel("Uninstall Docker"))
        docker_button = QPushButton("Uninstall")
        docker_button.setStyleSheet(dark.danger_button)
        docker_button.clicked.connect(lambda: uninstall_docker(globs))
        docker_row.addWidget(docker_button)
        docker_row.addStretch()
        layout.addLayout(docker_row)

    # Uninstall Kokoro
    if globs.kokoro_active and globs.os_name.startswith("Linux"):
        kokoro_row = QHBoxLayout()
        kokoro_row.addWidget(QLabel("Uninstall Kokoro"))
        kokoro_button = QPushButton("Uninstall")
        kokoro_button.setStyleSheet(dark.danger_button)
        kokoro_button.clicked.connect(lambda: uninstall_kokoro(globs))
        kokoro_row.addWidget(kokoro_button)
        kokoro_row.addStretch()
        layout.addLayout(kokoro_row)

    return tab_widget


def restore_localhost(globs, type):
    """Restores the address to localhost."""
    if type == "chat":
        globs.ollama_chat_path = "http://localhost:11434/"
        globs.ollama_chat_path_box.setText("http://localhost:11434/")
    elif type == "title":
        globs.ollama_title_path = "http://localhost:11434/"
        globs.ollama_title_path_box.setText("http://localhost:11434/")
    save_qt_settings(globs)
