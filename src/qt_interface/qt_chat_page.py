# src/qt_interface/qt_chat_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,  QScrollArea, QFrame,
    QApplication, QTextBrowser
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QTextOption
from src.connections.ollama import (
    get_loaded_models, unload_model
)
from src.utils.save_settings import save_settings
from src.qt_interface.qt_components.qt_input_box import create_input_area
from src.qt_interface.qt_styling import dark
import sounddevice as sd
import math


class AutoHeightBrowser(QTextBrowser):
    """QTextBrowser that auto-resizes height to fit content."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOpenExternalLinks(True)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.document().setDocumentMargin(0)
        self.textChanged.connect(self._update_height)

    def wheelEvent(self, event):
        # Bubbles are auto-sized to fit content, so they never scroll internally.
        # Ignore wheel events so they propagate to the chat scroll area instead
        # of being silently swallowed by the hidden internal scrollbar.
        event.ignore()

    def _update_height(self):
        doc = self.document()
        max_width = 600
        doc.setTextWidth(max_width)
        natural_width = math.ceil(doc.idealWidth()) + 2
        target_width = min(natural_width, max_width)
        doc.setTextWidth(target_width)
        height = int(doc.size().height())
        self.setFixedWidth(target_width)
        self.setFixedHeight(height + 2)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_height()


def create_chat_page(globs):
    """Creates the main chat page with chat area + input at the bottom."""

    globs.add_bubble = add_bubble
    # Main container for the chat page
    chat_page = QWidget()
    
    # Main vertical layout: chat area takes most space, input stays at bottom
    main_layout = QVBoxLayout(chat_page)
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)

    # Chat Area
    scroll_area = QScrollArea()
    scroll_area.setObjectName("chatScrollArea")
    scroll_area.verticalScrollBar().setObjectName("chatScrollBar")
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll_area.setStyleSheet(dark.scroll_area)

    # Container for messages
    chat_content = QWidget()
    chat_layout = QVBoxLayout(chat_content)
    chat_layout.setSpacing(15)
    chat_layout.addStretch(1)

    scroll_area.setWidget(chat_content)
    main_layout.addWidget(scroll_area, stretch=1)

    # Input Area
    globs.input_widget = create_input_area(globs)
    input_widget = globs.input_widget

    # Handle model switching from the toolbar combobox
    def on_model_changed():
        model = globs.model_combo.currentText()
        if not model or model == getattr(globs, "active_model", ""):
            return
        globs.active_model = model
        save_settings(active_model=model)
        # Unload any other loaded models to free VRAM/RAM
        for loaded in get_loaded_models(globs, globs.ollama_chat_path):
            if loaded != model:
                unload_model(globs, loaded)

    globs.model_combo.currentIndexChanged.connect(on_model_changed)

    main_layout.addWidget(input_widget)

    # Store references on globs so we can access them later from other functions
    globs.chat_main_layout = main_layout
    globs.chat_area_layout = chat_layout
    globs.chat_content = chat_content

    return chat_page


def add_bubble(globs, role, text, model=None):
    """Creates a message bubble in the chat area."""
    # Create a frame for the bubble
    bubble_frame = QFrame()
    bubble_frame.setStyleSheet("background-color: #3a3a3a; border-radius: 8px;")
    
    # Layout for the bubble
    bubble_layout = QVBoxLayout(bubble_frame)
    bubble_layout.setContentsMargins(10, 10, 10, 10)
    
    # Create the message label
    message_label = AutoHeightBrowser()
    message_label.setMarkdown(text)
    message_label.setFont(QFont("Ubuntu", 14))
    message_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    message_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    message_label.setReadOnly(True)
    
    # Style based on role
    if role == "user":
        message_label.setAlignment(Qt.AlignLeft)
    
    bubble_layout.addWidget(message_label)
    bubble_frame.adjustSize()
    
    # Add to chat layout
    globs.chat_area_layout.insertWidget(
        globs.chat_area_layout.count() - 1,
        bubble_frame,
        alignment=Qt.AlignRight if role == "user" else Qt.AlignLeft)
    
    return message_label


def clear_chat_area(globs):
    """Removes all message bubbles from the chat layout."""
    layout = globs.chat_area_layout
    while layout.count() > 1:  # keep the trailing stretch
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()


def refresh_chat_page(globs):
    """Rebuilds chat bubbles from the loaded conversation history."""
    clear_chat_area(globs)
    for message in globs.conversation_history:
        role = message.get("role")
        content = message.get("content", "")
        if role in ("user", "assistant") and content:
            add_bubble(globs, role=role, text=content)


def switch_to_chat_page(globs):
    """Flips to the chat page, bringing the input widget back home."""
    globs.page_stack.setCurrentIndex(1)
    globs.chat_main_layout.addWidget(globs.input_widget)
    globs.input_widget.setMaximumWidth(16777215)  # Qt's "no limit"


def switch_to_new_chat_page(globs):
    """Flips to the landing page and moves the input widget into its slot."""
    globs.page_stack.setCurrentIndex(0)
    globs.new_chat_input_slot.addWidget(globs.input_widget)
    globs.input_widget.setMaximumWidth(700)


def copy_to_clipboard(text):
    """Copies text to clipboard."""
    clipboard = QApplication.clipboard()
    clipboard.setText(text)


def scroll_to_bottom(scroll_area):
    """Scrolls the chat area to the bottom."""
    scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum())
