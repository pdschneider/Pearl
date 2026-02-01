import logging, os, json
from Utils.load_settings import load_settings, load_data_path
from config import apply_theme
from Utils.toast import show_toast

def save_all_settings(globals):
    """
    Save all settings to JSON files and update globals.

    Args:
        globals (Globals): The global configuration object containing UI variables and settings.
    """

    # Load current settings
    settings = load_settings()
    current_logging_level = globals.logging_var.get()
    current_active_theme = globals.theme_var.get()
    current_tts = globals.tts_var.get()
    current_active_voice = globals.active_voice_var.get()
    current_tts_source = globals.tts_source_var.get()
    current_save_chats = globals.save_chats_var.get()
    current_sink = globals.sink_var.get()

    # Handle logging level based on dev mode change
    logging_level = current_logging_level

    # Save Window Placement
    logging.debug(f"Root state: {globals.root.state()}")
    if globals.root.state() != "zoomed":  # don't save if maximized
        try:
            current_width = globals.root.winfo_width()
            current_height = globals.root.winfo_height()
            current_x = globals.root.winfo_x()
            current_y = globals.root.winfo_y()

            logging.debug(f"Saving via winfo: {current_width}x{current_height}"
                        f"+{current_x}+{current_y}")
        except Exception as e:
            logging.debug(f"Could not save window placement due to {e}")
            return
    else:
        return

    # Save settings with updated logging levels
    save_settings(
    logging_level = logging_level,
    active_theme = current_active_theme,
    tts_enabled = current_tts,
    active_voice = current_active_voice,
    tts_source = current_tts_source,
    save_chats = current_save_chats,
    default_sink = current_sink,
    saved_width = current_width,
    saved_height = current_height,
    saved_x = current_x,
    saved_y = current_y)

    # Refresh Globals
    globals.refresh_globals()

    # Reload settings to update globals
    settings = load_settings()
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
    apply_theme(current_active_theme)

    show_toast(globals, "Saved!")
    logging.info(f"Settings saved successfully.")

def save_settings(**kwargs):
    """Save settings to settings.json."""
    settings = load_settings()
    settings.update(kwargs)
    file_path = os.path.normpath(load_data_path("config", "settings.json"))
    try:
        with open(file_path, 'w') as f:
            json.dump(settings, f, indent=4)
        logging.info(f"Saving settings to: {file_path}")
    except Exception as e:
        logging.error(f"Error saving settings to {file_path}: {e}")
