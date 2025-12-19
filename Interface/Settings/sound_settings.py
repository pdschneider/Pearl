# Interface/Settings/sound_settings.py
import customtkinter as ctk
from Utils.save_settings import save_all_settings
from Managers.sound_manager import fetch_tts_models
from Managers.sound_manager import get_sink_menu
import Utils.fonts as fonts
from config import os_name

def create_sound_tab(globals, sound_tab):
    """
    Creates the general settings tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    sound_tab: The main frame of the speech settings window.
    """

    ctk.CTkLabel(sound_tab, 
             text="Sound Settings", 
             font=fonts.title_font, 
             anchor="center").pack(fill="x", pady=20, padx=10)

    # Options Frame
    options_frame = ctk.CTkFrame(sound_tab, bg_color="transparent", fg_color="transparent")
    options_frame.pack(fill="both", padx=10, pady=10)

    ctk.CTkLabel(options_frame,
              text="Enable TTS:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

    ctk.CTkCheckBox(options_frame,
                    variable=globals.tts_var,
                    text=None,
                    onvalue=True,
                    offvalue=False).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Dynamically build the source list
    source_options = ["Default"]
    if globals.kokoro_active:
        source_options.append("Kokoro")

    ctk.CTkLabel(options_frame,
              text="TTS Source:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

    ctk.CTkComboBox(options_frame,
                 variable=globals.tts_source_var,
                 values=source_options,
                 width=150,
                 state="readonly").grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tts_source_combobox = ctk.CTkComboBox(options_frame,
                variable=globals.active_voice_var,
                values=fetch_tts_models(globals),
                width=150,
                state="readonly")

    def update_voice_combobox(*_):
        """Dynamically updates the voice selection box"""
        if globals.kokoro_active and globals.tts_source_var.get() == "Kokoro":
            tts_source_combobox.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        else:
            tts_source_combobox.grid_remove()
    update_voice_combobox()

    globals.tts_source_var.trace_add("write", update_voice_combobox)

    # Default Speakers
    if os_name.startswith("Linux"):
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

        ctk.CTkLabel(options_frame,
                text="Sound Output:").grid(row=2, column=0, padx=5, pady=5, sticky="w")

        ctk.CTkComboBox(options_frame,
                    variable=label_var,
                    values=sink_labels,
                    width=250,
                    state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(sound_tab, bg_color="transparent", fg_color="transparent")
    save_button_frame.pack(pady=10)

    ctk.CTkButton(save_button_frame, 
               text="Save Settings", 
               command=lambda: save_all_settings(globals)).pack()
