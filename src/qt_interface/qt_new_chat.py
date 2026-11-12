# src/qt_interface/qt_new_chat.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


def create_new_chat_page(globs):
    """Landing page shown for a new chat: centered Pearl title + input slot."""
    page = QWidget()

    layout = QVBoxLayout(page)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)

    # Stretch pushes the title/input cluster toward vertical center
    layout.addStretch(1)

    title = QLabel("Pearl")
    title.setFont(QFont("Ubuntu", 42, QFont.Weight.Bold))
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)

    subtitle = QLabel("What's on your mind?")
    subtitle.setFont(QFont("Ubuntu", 14))
    subtitle.setAlignment(Qt.AlignCenter)
    layout.addWidget(subtitle)

    # Empty slot where the input widget gets reparented into
    globs.new_chat_input_slot = QVBoxLayout()
    globs.new_chat_input_slot.setAlignment(Qt.AlignHCenter)
    layout.addLayout(globs.new_chat_input_slot)

    layout.addStretch(1)

    globs.new_chat_page = page
    return page
