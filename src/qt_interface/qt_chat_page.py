# src/qt_interface/qt_chat_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QPushButton, QLabel,
    QScrollArea, QFrame, QSizePolicy,
    QApplication)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCursor, QFont, QFontMetrics
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


class InputBox(QTextEdit):
    """Custom QTextEdit that sends on Enter, newlines on Shift+Enter, with cooldown."""
    
    def __init__(self, globs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.globs = globs
        self.ui_elements = {"add_bubble": lambda *a, **kw: add_bubble(*a, **kw)}

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and not event.modifiers() & Qt.ShiftModifier:
            self._handle_enter()
            return
        
        super().keyPressEvent(event)

    def _handle_enter(self):
        import time

        text = self.toPlainText().strip()

        # If streaming and no new text, ignore
        if self.globs.still_streaming and not text:
            return

        # If streaming with new text and 2+ seconds elapsed, cancel current stream
        if self.globs.still_streaming and text:
            if time.time() - self.globs.last_message_time >= 2:
                if self.globs.cancel_event:
                    self.globs.cancel_event.set()
            else:
                return  # Too soon, ignore

        send_message(self.globs, self.ui_elements)


def handle_send_click(globs):
    """Toggles between send and stop depending on streaming state."""
    if globs.still_streaming and globs.cancel_event:
        globs.cancel_event.set()
        globs.send_button.setText("➤")
    else:
        send_message(globs, {"add_bubble": add_bubble})


def update_send_button_visibility(globs):
    """Shows send button when there's text or streaming, hides otherwise."""
    if globs.still_streaming:
        globs.send_button.setVisible(True)
    elif globs.input_box.toPlainText().strip():
        globs.send_button.setVisible(True)
    else:
        globs.send_button.setVisible(False)


def create_input_area(globs):
    """Creates a unified input area with text box + toolbar row inside one rounded container."""
    input_widget = QWidget()
    outer_layout = QVBoxLayout(input_widget)
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer_layout.setSpacing(0)

    # Single unified rounded container
    input_container = QFrame()
    input_container.setStyleSheet(
        """
        QFrame {
            background-color: #2b2b2b;
            border: 1px solid #3a3a3a;
            border-radius: 12px;
        }
        """
    )
    container_layout = QVBoxLayout(input_container)
    container_layout.setContentsMargins(8, 8, 8, 8)
    container_layout.setSpacing(0)

    # Top row: Text input + send button (combined)
    top_row = QWidget()
    top_row.setFixedHeight(50)
    top_layout = QHBoxLayout(top_row)
    top_layout.setContentsMargins(0, 0, 0, 0)
    top_layout.setSpacing(0)

    # Text input (shorter now)
    globs.input_box = InputBox(globs)
    globs.input_box.setPlaceholderText("Message Pearl...")
    globs.input_box.setFont(QFont("Ubuntu", 14))
    globs.input_box.setMaximumHeight(50)
    globs.input_box.setMinimumHeight(50)
    globs.input_box.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    globs.input_box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    globs.input_box.setStyleSheet(
        """
        QTextEdit {
            background-color: transparent;
            border: none;
            color: white;
            padding: 6px;
        }
        QTextEdit:focus {
            outline: none;
        }
        """
    )
    top_layout.addWidget(globs.input_box, stretch=1)

    # Send button
    globs.send_button = QPushButton("➤")
    globs.send_button.setFixedSize(32, 32)
    globs.send_button.setStyleSheet(
        """
        QPushButton {
            background-color: #4a4a4a;
            border: none;
            border-radius: 16px;
            color: white;
        }
        QPushButton:hover {
            background-color: #5a5a5a;
        }
        """
    )
    globs.send_button.clicked.connect(lambda: handle_send_click(globs))

    # Hide/show button based on input content
    globs.input_box.textChanged.connect(lambda: update_send_button_visibility(globs))
    globs.send_button.setVisible(False)

    top_layout.addWidget(globs.send_button)
    top_layout.addSpacing(8)

    container_layout.addWidget(top_row)

    # Bottom row: Toolbar (blended-in, invisible for now)
    toolbar_row = QWidget()
    toolbar_row.setFixedHeight(28)  # Small toolbar height
    toolbar_layout = QHBoxLayout(toolbar_row)
    toolbar_layout.setContentsMargins(8, 0, 8, 0)
    toolbar_layout.setSpacing(6)
    toolbar_layout.addStretch()  # Future buttons pinned left

    # Same background as container so it blends perfectly
    toolbar_row.setStyleSheet(
        """
        QWidget {
            background-color: transparent;
        }
        """
    )
    container_layout.addWidget(toolbar_row)

    outer_layout.addWidget(input_container)

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


def copy_to_clipboard(text):
    """Copies text to clipboard."""
    clipboard = QApplication.clipboard()
    clipboard.setText(text)


def scroll_to_bottom(scroll_area):
    """Scrolls the chat area to the bottom."""
    scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum())
