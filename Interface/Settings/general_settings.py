# Interface/Settings/general_settings.py
from tkinter import messagebox
import customtkinter as ctk
import logging
import config

def create_general_settings_tab(globals, general_frame):
    """Creates the general settings tab and initializes widgets."""

    ctk.CTkLabel(general_frame, 
             text="General Settings", 
             anchor="center").pack(fill="x", pady=20, padx=10)

    # Options Frame
    options_frame = ctk.CTkFrame(general_frame, bg_color="transparent", fg_color="transparent")
    options_frame.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(options_frame,
              text="Save Chats:").pack(side="left", padx=(0, 12))
    
    ctk.CTkCheckBox(options_frame,
                    variable=globals.save_chats_var,
                    onvalue=True,
                    text=None,
                    offvalue=False).pack(side="left", padx=5)

    # Theme Frame
    theme_frame = ctk.CTkFrame(general_frame, bg_color="transparent", fg_color="transparent")
    theme_frame.pack(fill="x", pady=10, padx=10)

    ctk.CTkLabel(theme_frame, 
    text="Theme:").pack(side="left", padx=(0, 12))

    ctk.CTkComboBox(theme_frame,
        variable=globals.theme_var,
        values=["cosmic_sky", "pastel_green", "blazing_red", "dark_cloud",  "soft_light"],
        state="readonly",
        width=150).pack(side="left")

    # Advanced Frame
    advanced_frame = ctk.CTkFrame(general_frame, bg_color="transparent", fg_color="transparent")
    advanced_frame.pack(anchor="w", pady=5)

    ctk.CTkLabel(advanced_frame,
              text="Advanced").grid(row=1, column=0, padx=5, pady=5, sticky="w")

    ctk.CTkLabel(advanced_frame, 
             text="Logging Level:").grid(row=2, column=0, padx=5, sticky="w")
    
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    col = 1
    for level in levels:
        ctk.CTkRadioButton(advanced_frame, 
                       text=level, 
                       value=level, 
                       variable=globals.logging_var).grid(row=2, column=col, padx=5, sticky="w")
        col += 1

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(general_frame, bg_color="transparent", fg_color="transparent")
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