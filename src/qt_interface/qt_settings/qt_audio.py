# src/qt_interface/qt_settings/qt_audio.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox
)
from PySide6.QtCore import Qt
from src.qt_interface.qt_styling import dark
from src.connections.kokoro import fetch_current_language_models
from src.managers.sound_manager import get_sink_menu


def create_audio_settings_tab(globs):
    """
    Create the Audio Settings tab for Qt interface.
    Returns a QWidget that can be added directly to the tab widget.
    """

# TODO:
# > Voice Selection
# > Speaker Selection

    # Main Widget
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)
    layout.setAlignment(Qt.AlignTop)

    # Title
    title = QLabel("Audio")
    title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
    layout.addWidget(title)

    # TTS Source Row
    source_row = QHBoxLayout()
    source_label = QLabel("TTS Source")
    source_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
    source_row.addWidget(source_label)
    layout.addLayout(source_row)

    source_combo = QComboBox()
    options = ["Default"] + (["Kokoro"] if globs.kokoro_active else [])
    source_combo.addItems(options)
    source_combo.setStyleSheet(dark.combobox)
    source_row.addWidget(source_combo)
    source_row.addStretch()

    # Sync combo to saved setting ("default" / "kokoro")
    saved = globs.tts_source.capitalize() if globs.tts_source else "Default"
    if saved in options:
        source_combo.setCurrentText(saved)

    def on_source_changed(text):
        globs.tts_source = text
        voice_container.setVisible(text == "Kokoro")

    source_combo.currentTextChanged.connect(on_source_changed)

    # Voice Row (Kokoro only)
    if globs.kokoro_active:
        voice_container = QWidget()
        voice_row = QHBoxLayout(voice_container)
        voice_row.setContentsMargins(0, 0, 0, 0)
        voice_label = QLabel("Voice")
        voice_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        voice_row.addWidget(voice_label)
        layout.addWidget(voice_container)

        label_to_voice = {model[3:].capitalize(): model
                          for model in fetch_current_language_models(globs)}
        voice_combo = QComboBox()
        voice_combo.addItems(list(label_to_voice.keys()))
        voice_combo.setStyleSheet(dark.combobox)

        # Sync saved voice
        saved_voice = globs.kokoro_active_voice
        saved_label = next((lbl for lbl, v in label_to_voice.items()
                            if v == saved_voice), None)
        if saved_label:
            voice_combo.setCurrentText(saved_label)

        def on_voice_changed(text):
            globs.kokoro_active_voice = label_to_voice.get(text, saved_voice)

        voice_combo.currentTextChanged.connect(on_voice_changed)
        voice_row.addWidget(voice_combo)
        voice_row.addStretch()
        voice_container.setVisible(globs.tts_source == "Kokoro")

    # Sound Output Row (Linux only)
    if globs.os_name.startswith("Linux"):
        sink_container = QWidget()
        sink_row = QHBoxLayout(sink_container)
        sink_row.setContentsMargins(0, 0, 0, 0)

        sink_label = QLabel("Sound Output")
        sink_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        sink_row.addWidget(sink_label)

        globs.sink_list = get_sink_menu()
        label_to_pulse = {entry["label"]: entry["pulse_name"]
                          for entry in globs.sink_list}
        sink_combo = QComboBox()
        sink_combo.addItems(list(label_to_pulse.keys()))
        sink_combo.setStyleSheet(dark.combobox)

        # Sync saved sink
        saved_sink = globs.default_sink
        saved_sink_label = next((lbl for lbl, p in label_to_pulse.items()
                                 if p == saved_sink), "Default")
        sink_combo.setCurrentText(saved_sink_label)

        def on_sink_changed(text):
            globs.default_sink = label_to_pulse.get(text, "Default")

        sink_combo.currentTextChanged.connect(on_sink_changed)
        sink_row.addWidget(sink_combo)
        sink_row.addStretch()
        layout.addWidget(sink_container)

    return tab_widget
