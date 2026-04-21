# Interface/Settings/sound_settings.py
import customtkinter as ctk
from CTkToolTip import CTkToolTip
from tkinter import messagebox
from PySide6.QtWidgets import QMessageBox
import logging
import subprocess
import sys
from src.utils.save_settings import save_all_settings
from src.connections.kokoro import fetch_current_language_models
from src.managers.sound_manager import get_sink_menu
from src.utils.load_settings import load_data_path
import src.utils.fonts as fonts


def create_sound_tab(globals, sound_tab):
    """
    Creates the general settings tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    sound_tab: The main frame of the speech settings window.
    """

    ctk.CTkLabel(sound_tab,
                 text="Sound",
                 font=fonts.title_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)

    # Options Frame
    options_frame = ctk.CTkFrame(sound_tab,
                                 bg_color="transparent",
                                 fg_color="transparent")
    options_frame.pack(fill="both", padx=10, pady=10)

    # Enable TTS Frame
    enable_tts_frame = ctk.CTkFrame(options_frame,
                                 bg_color="transparent",
                                 fg_color="transparent")
    enable_tts_frame.pack(fill="both", padx=10, pady=10)

    ctk.CTkLabel(enable_tts_frame,
                 text=None,
                 image=globals.sound_high_icon).pack(
                     side="left", padx=6, pady=0)

    enable_tts_button = ctk.CTkLabel(enable_tts_frame,
                                     text="Enable TTS",
                                     font=fonts.heading_font)
    enable_tts_button.pack(side="left", padx=5)
    CTkToolTip(enable_tts_button,
               message="Enables TTS",
               delay=0.6,
               follow=True,
               padx=10,
               pady=5)

    ctk.CTkCheckBox(enable_tts_frame,
                    variable=globals.tts_var,
                    text=None,
                    onvalue=True,
                    offvalue=False).pack(side="left", padx=5)

    # Sound Frame
    sound_frame = ctk.CTkFrame(options_frame,
                               bg_color="transparent",
                               fg_color="transparent")
    sound_frame.pack(fill="both", padx=10, pady=10)

    # Dynamically build the source list
    if globals.kokoro_active:
        globals.source_options.append("Kokoro")

    ctk.CTkLabel(sound_frame,
                 text=None,
                 image=globals.phone_icon).pack(side="left", padx=6, pady=0)

    tts_source_label = ctk.CTkLabel(sound_frame,
                                    text="TTS Source",
                                    font=fonts.heading_font)
    tts_source_label.pack(side="left", padx=5)
    CTkToolTip(tts_source_label,
               message="Choose the speech model",
               delay=0.6,
               follow=True,
               padx=10,
               pady=5)

    ctk.CTkComboBox(sound_frame,
                    variable=globals.tts_source_var,
                    values=globals.source_options,
                    width=150,
                    state="readonly").pack(side="left", padx=5)

    # TTS Voices Box
    if globals.kokoro_active:
        available_voices = {}

        # Create dictionary mapping human-readable names to Kokoro-readable names
        for model in fetch_current_language_models(globals):
            new_model = model[3:]
            available_voices[model] = new_model.capitalize()

        # Assign each name to label (human readable) and voice (Kokoro readable)
        voice_options = [{"label": label, "voice": key} 
                    for key, label in available_voices.items()]

        # Create a lists for 
        voice_labels = [entry["label"] for entry in voice_options]
        voice_names = [entry["voice"] for entry in voice_options]
        label_to_voice = {entry["label"]: entry["voice"] for entry in voice_options}

        # Create variable to store label
        voice_label_var = ctk.StringVar()

        def update_voice_var(*args):
            """Dynamically updates voice combobox."""
            selected_label = voice_label_var.get()
            voice_name = label_to_voice.get(selected_label, "Heart")
            globals.kokoro_active_voice_var.set(voice_name)

        # Watches voice combobox for changes, udpates on change
        voice_label_var.trace("w", update_voice_var)

        initial_voice = globals.kokoro_active_voice_var.get()
        initial_label = next(
            (label for label, voice in label_to_voice.items() if voice == initial_voice), "Heart")
        voice_label_var.set(initial_label)

        # logging.debug(f"Available Voices: {voice_options}")

        tts_source_combobox = ctk.CTkComboBox(sound_frame,
                                            variable=voice_label_var,
                                            values=voice_labels,
                                            width=150,
                                            state="readonly")
        tts_source_combobox.pack(side="left", padx=5)

    # Speakers Frame
    if globals.os_name.startswith("Linux"):
        globals.speakers_frame = ctk.CTkFrame(options_frame,
                                    bg_color="transparent",
                                    fg_color="transparent")
        globals.speakers_frame.pack(fill="both", padx=10, pady=10)

        ctk.CTkLabel(globals.speakers_frame,
                    text=None,
                    image=globals.speaker_icon).pack(side="left", padx=6, pady=0)

        globals.sink_list = get_sink_menu()
        sink_labels = [entry["label"] for entry in globals.sink_list]
        label_to_pulse = {entry["label"]: entry["pulse_name"] for entry in globals.sink_list}

        label_var = ctk.StringVar()

        def update_sink_var(*args):
            selected_label = label_var.get()
            pulse_name = label_to_pulse.get(selected_label, "Default")
            globals.sink_var.set(pulse_name)

        label_var.trace("w", update_sink_var)

        initial_pulse = globals.sink_var.get()
        initial_label = next((label for label, pulse in label_to_pulse.items() if pulse == initial_pulse), "Default")
        label_var.set(initial_label)

        sound_output_label = ctk.CTkLabel(globals.speakers_frame,
                                            text="Sound Output",
                                            font=fonts.heading_font)
        sound_output_label.pack(side="left", padx=5)
        CTkToolTip(sound_output_label,
                    message="Choose the speakers\n tts plays from\n",
                    delay=0.6,
                    follow=True,
                    padx=10,
                    pady=5)

        ctk.CTkComboBox(globals.speakers_frame,
                        variable=label_var,
                        values=sink_labels,
                        width=250,
                        state="readonly").pack(side="left", padx=5)

        globals.speakers_frame.pack(fill="both", padx=10, pady=10)

        # Dynamically update voice selection box
        def update_voice_combobox(*_):
            """Dynamically updates the voice selection box."""
            try:
                if globals.kokoro_active and globals.tts_source_var.get() == "Kokoro":
                    tts_source_combobox.pack(side="left", padx=5)
                else:
                    tts_source_combobox.pack_forget()
            except Exception as e:
                logging.error(f"Unable to update Kokoro voice dropdown due to: {e}")

        # Update box only if Kokoro is active
        if globals.kokoro_active:
            update_voice_combobox()

        globals.tts_source_var.trace_add("write", update_voice_combobox)

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(sound_tab,
                                     bg_color="transparent",
                                     fg_color="transparent")
    save_button_frame.pack(pady=10)

    ctk.CTkButton(save_button_frame,
                  text="Save Settings",
                  command=lambda: save_button(globals)).pack()

    def save_button(globals):
        """Saves and prompts for restart if required."""
        prompt_restart = False
        if globals.github_check != globals.github_check_var.get():
            prompt_restart = True
        elif globals.active_theme != globals.theme_var.get():
            prompt_restart = True
        elif globals.beta != globals.beta_var.get():
            prompt_restart = True
        save_all_settings(globals)

        if prompt_restart:
            if globals.qt_mode:
                reply = QMessageBox.question(
                    None,
                    "Restart Pearl?",
                    f"Would you like to restart Pearl to apply all changes?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes)
                if reply == QMessageBox.StandardButton.Yes:
                    subprocess.Popen(globals.app_path)
                    sys.exit(0)
            else:
                    reply = messagebox.askyesno(
                        parent=globals.root,
                        title="Restart Pearl",
                        message="Would you like restart Pearl to apply all changes?")
                    if reply:
                        subprocess.Popen(globals.app_path)
                        sys.exit(0)
