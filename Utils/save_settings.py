import config
import logging

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

    # Save Window Placement
    logging.debug(f"Root state: {globals.root.state()}")
    if globals.root.state() != "zoomed":  # don't save if maximized
        try:
            current_width = globals.root.winfo_width()
            current_height = globals.root.winfo_height()
            current_horizontal_placement = globals.root.winfo_x()
            current_vertical_placement = globals.root.winfo_y()

            logging.debug(f"Saving via winfo: {current_width}x{current_height}"
                        f"+{current_horizontal_placement}+{current_vertical_placement}")
        except Exception as e:
            logging.debug(f"Could not save window placement due to {e}")
            return
    else:
        return

    # Save settings with updated logging levels
    config.save_settings(
    logging_level = logging_level,
    saved_logging_level = saved_logging_level,
    active_theme = current_active_theme,
    tts_enabled = current_tts,
    active_voice = current_active_voice,
    tts_source = current_tts_source,
    save_chats = current_save_chats,
    default_sink = current_sink,
    saved_width = current_width,
    saved_height = current_height,
    saved_horizontal_placement = current_horizontal_placement,
    saved_vertical_placement = current_vertical_placement)

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

    logging.info(f"Settings saved successfully.")
