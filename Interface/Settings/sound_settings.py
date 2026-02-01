# Interface/Settings/sound_settings.py
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from CTkToolTip import CTkToolTip
from Utils.save_settings import save_all_settings
from Managers.sound_manager import fetch_tts_models
from Managers.sound_manager import get_sink_menu
from Utils.load_settings import load_data_path
import Utils.fonts as fonts

def create_sound_tab(globals, sound_tab):
    """
    Creates the general settings tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    sound_tab: The main frame of the speech settings window.
    """

    # Get Icons
    globals.sound_high_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/sound_high.png")),
    dark_image=Image.open(load_data_path("config", "assets/sound_high.png")),
    size=(40, 40))

    globals.speaker_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/speaker.png")),
    dark_image=Image.open(load_data_path("config", "assets/speaker.png")),
    size=(40, 40))

    globals.phone_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/phone.png")),
    dark_image=Image.open(load_data_path("config", "assets/phone.png")),
    size=(40, 40))

    ctk.CTkLabel(sound_tab, 
             text="Sound Settings", 
             font=fonts.title_font, 
             anchor="center").pack(fill="x", pady=20, padx=10)

    # Options Frame
    options_frame = ctk.CTkFrame(sound_tab, bg_color="transparent", fg_color="transparent")
    options_frame.pack(fill="both", padx=10, pady=10)

    ctk.CTkLabel(options_frame, text=None, image=globals.sound_high_icon).pack(side="left", padx=6, pady=0)

    enable_tts_button = ctk.CTkLabel(options_frame,
              text="Enable TTS",
              font=fonts.heading_font)
    enable_tts_button.pack(side="left", padx=5)
    CTkToolTip(enable_tts_button, message="Enables TTS", delay=0.6, follow=True, padx=10, pady=5)

    ctk.CTkCheckBox(options_frame,
                    variable=globals.tts_var,
                    text=None,
                    onvalue=True,
                    offvalue=False).pack(side="left", padx=5)

    # Sound Frame
    sound_frame = ctk.CTkFrame(sound_tab, bg_color="transparent", fg_color="transparent")
    sound_frame.pack(fill="both", padx=10, pady=10)

    # Dynamically build the source list
    source_options = ["Default"]
    if globals.kokoro_active:
        source_options.append("Kokoro")

    ctk.CTkLabel(sound_frame, text=None, image=globals.phone_icon).pack(side="left", padx=6, pady=0)

    tts_source_label = ctk.CTkLabel(sound_frame,
              text="TTS Source",
              font=fonts.heading_font)
    tts_source_label.pack(side="left", padx=5)
    CTkToolTip(tts_source_label, message="Choose the speech model", delay=0.6, follow=True, padx=10, pady=5)

    ctk.CTkComboBox(sound_frame,
                 variable=globals.tts_source_var,
                 values=source_options,
                 width=150,
                 state="readonly").pack(side="left", padx=5)

    tts_source_combobox = ctk.CTkComboBox(sound_frame,
                variable=globals.active_voice_var,
                values=fetch_tts_models(globals),
                width=150,
                state="readonly")

    def update_voice_combobox(*_):
        """Dynamically updates the voice selection box"""
        if globals.kokoro_active and globals.tts_source_var.get() == "Kokoro":
            tts_source_combobox.pack(side="left", padx=5)
        else:
            tts_source_combobox.pack_forget()
    update_voice_combobox()

    globals.tts_source_var.trace_add("write", update_voice_combobox)

    # Speakers Frame
    speakers_frame = ctk.CTkFrame(sound_tab, bg_color="transparent", fg_color="transparent")
    speakers_frame.pack(fill="both", padx=10, pady=10)

    ctk.CTkLabel(speakers_frame, text=None, image=globals.speaker_icon).pack(side="left", padx=6, pady=0)

    # Default Speakers
    if globals.os_name.startswith("Linux"):
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

        sound_output_label = ctk.CTkLabel(speakers_frame,
                text="Sound Output",
                font=fonts.heading_font)
        sound_output_label.pack(side="left", padx=5)
        CTkToolTip(sound_output_label, message="Choose the speakers\n tts plays from", delay=0.6, follow=True, padx=10, pady=5)

        ctk.CTkComboBox(speakers_frame,
                    variable=label_var,
                    values=sink_labels,
                    width=250,
                    state="readonly").pack(side="left", padx=5)

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(sound_tab, bg_color="transparent", fg_color="transparent")
    save_button_frame.pack(pady=10)

    ctk.CTkButton(save_button_frame, 
               text="Save Settings", 
               command=lambda: save_all_settings(globals)).pack()
