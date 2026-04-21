# src/qt_interface/qt_chat_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QPushButton, QLabel,
    QScrollArea, QFrame)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCursor, QFont
import logging
from src.managers.chat_manager import send_message
import src.utils.fonts as fonts


def create_chat_page(globals):
    """Creates the main chat page with chat area + input at the bottom."""
    
    # Main container for the chat page
    chat_page = QWidget()
    
    # Main vertical layout: chat area takes most space, input stays at bottom
    main_layout = QVBoxLayout(chat_page)
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)

    # === CHAT AREA ===
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    # Container for messages
    chat_content = QWidget()
    chat_layout = QVBoxLayout(chat_content)
    chat_layout.setSpacing(15)
    chat_layout.addStretch(1)

    scroll_area.setWidget(chat_content)
    main_layout.addWidget(scroll_area, stretch=1)

    # === INPUT AREA ===
    input_widget = create_input_area(globals)
    main_layout.addWidget(input_widget)

    # Store references on globals so we can access them later from other functions
    globals.chat_area_layout = chat_layout

    return chat_page


def create_input_area(globals):
    """Creates the bottom input box + send button"""
    input_widget = QWidget()
    input_layout = QHBoxLayout(input_widget)
    input_layout.setContentsMargins(0, 0, 0, 0)
    input_layout.setSpacing(8)

    # Multi-line text input
    input_box = QTextEdit()
    input_box.setPlaceholderText("Message Pearl...")
    input_box.setFont(QFont("Ubuntu", 14))
    input_box.setMaximumHeight(100)        # Allow a few lines but not too tall
    input_box.setMinimumHeight(40)

    ui_elements = {
        "add_bubble": lambda *args, **kwargs: add_bubble(*args, **kwargs)}

    # Send button
    send_button = QPushButton("Send")
    send_button.setFixedWidth(80)
    send_button.setMinimumHeight(40)
    send_button.clicked.connect(lambda e: send_message(globals, ui_elements))

    # Optional: make Enter key send message later
    # input_box.installEventFilter(...)  # we'll add this later

    input_layout.addWidget(input_box)
    input_layout.addWidget(send_button)

    # Store reference so other parts of the app can access the input box
    globals.input_box = input_box

    return input_widget

def add_bubble(globals, role, text, model=None):
    """Creates a message bubble in the chat area."""
    # Create a frame for the bubble
    bubble_frame = QFrame()
    
    # Layout for the bubble
    bubble_layout = QVBoxLayout(bubble_frame)
    bubble_layout.setContentsMargins(5, 5, 5, 5)
    
    # Create the message label
    message_label = QLabel(text)
    message_label.setWordWrap(True)
    message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
    message_label.setFont(QFont("Ubuntu", 14))
    
    # Style based on role
    if role == "user":
        message_label.setAlignment(Qt.AlignRight)
    else:
        message_label.setAlignment(Qt.AlignLeft)
    
    bubble_layout.addWidget(message_label)
    
    # Add to chat layout
    globals.chat_area_layout.insertWidget(
        globals.chat_area_layout.count() - 1,  # Insert before the stretch
        bubble_frame)
    
    return message_label
