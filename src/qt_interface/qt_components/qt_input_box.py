# src/qt_interface/qt_components/qt_input_box.py
import logging
import time
import os
import sounddevice as sd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QComboBox, QTextEdit,
    QLabel
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from src.managers.chat_manager import send_message
from src.qt_interface.qt_styling import dark
from src.managers.attachments import attach_file
from src.utils.toast import show_toast
from src.connections.ollama import (
    get_all_models
)

MAX_INPUT_HEIGHT = 140

class InputBox(QTextEdit):
    """Custom QTextEdit that sends on Enter, newlines on Shift+Enter, with cooldown."""

    def __init__(self, globs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.globs = globs
        self.textChanged.connect(self._grow_to_fit)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and not event.modifiers() & Qt.ShiftModifier:
            self._handle_enter()
            return
        super().keyPressEvent(event)

    def dragEnterEvent(self, event):
        # Only accept drags carrying files so normal text drags still behave
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        if not event.mimeData().hasUrls():
            super().dropEvent(event)
            return
        try:
            path = event.mimeData().urls()[0].toLocalFile()
            if path:
                attach_file(self.globs, dialog=False, filepath=path)
        except Exception as e:
            logging.warning(f"Drag-and-drop failed due to: {e}")
            show_toast(
                self.globs,
                message="Could not attach dropped file",
                _type="error")
        event.acceptProposedAction()

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self._grow_to_fit)

    def _grow_to_fit(self):
        doc = self.document()
        width = self.viewport().width() - 12
        if width <= 0 or not self.isVisible():
            return
        doc.setTextWidth(width)
        needed = doc.size().height() + 12
        h = max(70, min(int(needed), MAX_INPUT_HEIGHT))
        self.setFixedHeight(h)
        self.parentWidget().setFixedHeight(h)

    def _handle_enter(self):
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

        send_message(self.globs, {"add_bubble": self.globs.add_bubble})


def handle_send_click(globs):
    """Toggles between send and stop depending on streaming state."""
    if globs.still_streaming and globs.cancel_event:
        globs.cancel_event.set()
        globs.send_button.setText("➤")
    else:
        send_message(globs, {"add_bubble": globs.add_bubble})


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
    globs.show_attachment_chip = show_attachment_chip  # registered like add_bubble
    input_widget = QWidget()

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
    top_layout = QHBoxLayout(top_row)
    top_layout.setContentsMargins(0, 0, 0, 0)
    top_layout.setSpacing(0)

    # Text input
    globs.input_box = InputBox(globs)
    globs.input_box.setPlaceholderText("Message Pearl...")
    globs.input_box.setAcceptRichText(False)
    globs.input_box.setFont(QFont("Ubuntu", 15))
    # globs.input_box.setMaximumHeight(70)
    # globs.input_box.setMinimumHeight(70)
    globs.input_box.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    globs.input_box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    globs.input_box.setStyleSheet(dark.input_box)
    top_layout.addWidget(globs.input_box, stretch=1)

    # Send button
    globs.send_button = QPushButton("➤")
    globs.send_button.setFixedSize(32, 32)
    globs.send_button.setStyleSheet(dark.send_button)
    globs.send_button.clicked.connect(lambda: handle_send_click(globs))

    # Hide/show button based on input content
    globs.input_box.textChanged.connect(lambda: update_send_button_visibility(globs))
    globs.send_button.setVisible(False)

    top_layout.addWidget(globs.send_button)
    top_layout.addSpacing(8)

    container_layout.addWidget(top_row)

    # Attachment chip row (starts hidden until a file is attached)
    globs.attachment_chip_row = QWidget()
    chip_row_layout = QHBoxLayout(globs.attachment_chip_row)
    chip_row_layout.setContentsMargins(0, 0, 0, 6)
    chip_row_layout.setSpacing(6)
    chip_row_layout.addStretch()

    container_layout.insertWidget(0, globs.attachment_chip_row)
    globs.attachment_chip_row.setVisible(False)

    # Bottom row: Toolbar
    toolbar_row = QWidget()
    toolbar_row.setFixedHeight(28)  # Small toolbar height
    toolbar_layout = QHBoxLayout(toolbar_row)
    toolbar_layout.setContentsMargins(8, 0, 8, 0)
    toolbar_layout.setSpacing(6)

    # Attachment button (pinned bottom-left)
    globs.attach_button = QPushButton("+")
    globs.attach_button.setFixedSize(22, 22)
    globs.attach_button.setStyleSheet(dark.attach_button)
    globs.attach_button.clicked.connect(lambda: attach_file(globs))
    toolbar_layout.addWidget(globs.attach_button)

    toolbar_layout.addStretch()  # Separates two sides of the toolbar

    # TTS Toggle
    globs.tts_button = QPushButton("\U0001F50A" if globs.tts_enabled else "\U0001F507")
    globs.tts_button.setFixedSize(22, 22)
    globs.tts_button.setCheckable(True)
    globs.tts_button.setChecked(globs.tts_enabled)
    globs.tts_button.setStyleSheet(dark.tts_button)
    globs.tts_button.setToolTip("Text-to-Speech")
    globs.tts_button.clicked.connect(lambda: toggle_tts(globs))
    toolbar_layout.addWidget(globs.tts_button)

    # Model selector (right of TTS toggle)
    globs.model_combo = QComboBox()
    globs.model_combo.setMinimumWidth(140)
    globs.model_combo.setStyleSheet(dark.combobox)
    globs.model_combo.setToolTip("Active chat model")
    toolbar_layout.addWidget(globs.model_combo)

    # Populate with installed models
    if globs.ollama_active:
        models = sorted(get_all_models(globs, globs.ollama_chat_path) or [])
        globs.model_combo.addItems(models)

    # Pre-select the saved active model if present
    if getattr(globs, "active_model", "") in [
            globs.model_combo.itemText(i) for i in range(globs.model_combo.count())]:
        globs.model_combo.setCurrentText(globs.active_model)

    def toggle_tts(globs):
        sd.stop()
        on = globs.tts_button.isChecked()
        globs.tts_enabled = on
        globs.tts_button.setText("\U0001F50A" if on else "\U0001F507")

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


def show_attachment_chip(globs, filepath):
    """Rebuilds the attachment chip row for the current attachment_path."""

    # Wipe any old chips (keep the trailing stretch at index 0..n)
    layout = globs.attachment_chip_row.layout()
    while layout.count() > 1:  # keep the trailing stretch
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
    if not filepath:
        globs.attachment_chip_row.setVisible(False)
        return

    # Single chip: icon + truncated name + remove button
    chip = QFrame()
    chip.setObjectName("attachmentChip")
    chip.setStyleSheet(dark.attachment_chip)
    chip_layout = QHBoxLayout(chip)
    chip_layout.setContentsMargins(8, 2, 2, 2)
    chip_layout.setSpacing(6)

    name = os.path.basename(filepath)
    if len(name) > 18:
        name = name[:15] + "..."
    label = QLabel("📄 " + name)
    label.setStyleSheet(dark.attachment_chip_label)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
    chip_layout.addWidget(label)

    remove_btn = QPushButton("✕")
    remove_btn.setFixedSize(18, 18)
    remove_btn.setFlat(True)
    remove_btn.setStyleSheet(dark.attachment_chip_remove)
    remove_btn.clicked.connect(lambda: remove_attachment(globs))
    chip_layout.addWidget(remove_btn)

    layout.insertWidget(0, chip)  # before the stretch
    globs.attachment_chip_row.setVisible(True)


def remove_attachment(globs):
    """Clears the current attachment and hides the chip row."""
    globs.file_attachment = None
    globs.attachment_path = None
    globs.image_attachment = None
    show_attachment_chip(globs, None)
