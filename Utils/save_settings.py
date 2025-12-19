import config
import logging
from tkinter import messagebox

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
    current_sink = globals.sink_var.get()

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
    save_chats = current_save_chats,
    default_sink = current_sink)
    
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
    globals.sink_var.set(settings["default_sink"])

    # Update logging
    logging.root.setLevel(getattr(logging, settings["logging_level"]))

    # Apply new theme
    config.apply_theme(current_active_theme)

    messagebox.showinfo("Settings Saved", "Settings saved successfully.")
    logging.info(f"Settings saved successfully.")
