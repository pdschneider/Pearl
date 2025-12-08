# Interface/Settings/general_settings.py
from tkinter import messagebox
import customtkinter as ctk
import logging
import config
from Managers.speech_manager import fetch_tts_models
import themes

def create_speech_tab(globals, speech_frame):
    """
    Creates the general settings tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    speech_frame: The main frame of the speech settings window.
    """

    ctk.CTkLabel(speech_frame, 
             text="Speech Settings", 
             font=themes.title_font, 
             anchor="center").pack(fill="x", pady=20, padx=10)

    # Options Frame
    options_frame = ctk.CTkFrame(speech_frame, bg_color="transparent", fg_color="transparent")
    options_frame.pack(fill="both", padx=10, pady=10)

    ctk.CTkLabel(options_frame,
              text="Enable TTS:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

    ctk.CTkCheckBox(options_frame,
                    variable=globals.tts_var,
                    text=None,
                    onvalue=True,
                    offvalue=False).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Dynamically build the source list
    source_options = ["default"]
    if globals.kokoro_active:
        source_options.append("kokoro")

    ctk.CTkComboBox(options_frame,
                 variable=globals.tts_source_var,
                 values=source_options,
                 width=150,
                 state="readonly").grid(row=1, column=0, padx=5, pady=5, sticky="w")

    tts_source_combobox = ctk.CTkComboBox(options_frame,
                variable=globals.active_voice_var,
                values=fetch_tts_models(globals),
                width=150,
                state="readonly")

    def update_voice_combobox(*_):
        """Dynamically updates the voice selection box"""
        if globals.kokoro_active and globals.tts_source_var.get() == "kokoro":
            tts_source_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        else:
            tts_source_combobox.grid_remove()
    update_voice_combobox()

    globals.tts_source_var.trace_add("write", update_voice_combobox)

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(speech_frame, bg_color="transparent", fg_color="transparent")
    save_button_frame.pack(pady=10)

    ctk.CTkButton(save_button_frame, 
               text="Save Settings", 
               command=lambda: save_all_settings(globals)).pack()

def save_all_settings(globals):
    """
    Save all settings to JSON files and update globals.

    Args:
        globals (Globals): The global configuration object containing UI variables and settings.
    """

    # Load current settings to get saved_logging_level and current dev_mode
    settings = config.load_settings()
    current_logging_level = globals.logging_var.get()
    saved_logging_level = settings.get("saved_logging_level", "INFO")
    current_active_theme = globals.theme_var.get()
    current_tts = globals.tts_var.get()
    current_active_voice = globals.active_voice_var.get()
    current_tts_source = globals.tts_source_var.get()
    current_save_chats = globals.save_chats_var.get()

    # Handle logging level based on dev mode change
    logging_level = current_logging_level
    saved_logging_level = current_logging_level  # Update saved_logging_level to match

    # Save settings with updated logging levels
    config.save_settings(
    logging_level = logging_level,
    saved_logging_level = saved_logging_level,
    active_theme = current_active_theme,
    tts_enabled = current_tts,
    active_voice = current_active_voice,
    tts_source = current_tts_source,
    save_chats = current_save_chats)

    # Refresh Globals
    globals.refresh_globals()

    # Reload settings to update globals
    settings = config.load_settings()
    globals.logging_var.set(settings["logging_level"])
    globals.theme_var.set(settings["active_theme"])
    globals.tts_var.set(settings["tts_enabled"])
    globals.active_voice_var.set(settings["active_voice"])
    globals.tts_source_var.set(settings["tts_source"])
    globals.save_chats_var.set(settings["save_chats"])

    # Update logging
    logging.root.setLevel(getattr(logging, settings["logging_level"]))

    # Apply new theme
    config.apply_theme(current_active_theme)

    messagebox.showinfo("Settings Saved", "Settings saved successfully.")
    logging.info(f"Settings saved successfully.")
