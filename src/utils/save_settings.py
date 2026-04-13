import logging
import os
import json
from src.utils.load_settings import load_settings, load_data_path
from config import apply_theme
from src.utils.toast import show_toast


def save_all_settings(globals, reject_toast=False):
    """
    Save all settings to JSON files and update globals.

    Args:
        globals (Globals): The global configuration object
                           containing UI variables and settings.
    """

    # Load current settings
    settings = load_settings()
    current_logging_level = globals.logging_var.get()
    current_active_theme = globals.theme_var.get()
    current_tts = globals.tts_var.get()
    current_kokoro_active_voice = globals.kokoro_active_voice_var.get()
    current_default_active_voice = globals.default_active_voice_var.get()
    current_tts_source = globals.tts_source_var.get()
    current_save_chats = globals.save_chats_var.get()
    current_sink = globals.sink_var.get()
    current_github_check = globals.github_check_var.get()
    current_ollama_chat_path = globals.ollama_chat_path_var.get()
    current_ollama_context_path = globals.ollama_context_path_var.get()
    current_ollama_title_path = globals.ollama_title_path_var.get()
    current_enable_context = globals.enable_context_var.get()
    current_generate_titles = globals.generate_titles_var.get()

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
            logging_level=logging_level,
            active_theme=current_active_theme,
            tts_enabled=current_tts,
            kokoro_active_voice=current_kokoro_active_voice,
            default_active_voice=current_default_active_voice,
            tts_source=current_tts_source,
            save_chats=current_save_chats,
            default_sink=current_sink,
            saved_width=current_width,
            saved_height=current_height,
            saved_x=current_x,
            saved_y=current_y,
            github_check=current_github_check,
            ollama_chat_path=current_ollama_chat_path,
            ollama_context_path=current_ollama_context_path,
            ollama_title_path=current_ollama_title_path,
            enable_context=current_enable_context,
            generate_titles=current_generate_titles)

    # Refresh Globals
    globals.refresh_globals()

    # Reload settings to update globals
    settings = load_settings()
    globals.logging_var.set(settings["logging_level"])
    globals.theme_var.set(settings["active_theme"])
    globals.tts_var.set(settings["tts_enabled"])
    globals.kokoro_active_voice_var.set(settings["kokoro_active_voice"])
    globals.default_active_voice_var.set(settings["default_active_voice"])
    globals.tts_source_var.set(settings["tts_source"])
    globals.save_chats_var.set(settings["save_chats"])
    globals.sink_var.set(settings["default_sink"])
    globals.github_check_var.set(settings["github_check"])
    globals.ollama_chat_path_var.set(settings["ollama_chat_path"])
    globals.ollama_context_path_var.set(settings["ollama_context_path"])
    globals.ollama_title_path_var.set(settings["ollama_title_path"])
    globals.enable_context_var.set(settings["enable_context"])
    globals.generate_titles_var.set(settings["generate_titles"])

    # Update logging
    logging.root.setLevel(getattr(logging, settings["logging_level"]))

    # Apply new theme
    apply_theme(current_active_theme)

    if not reject_toast:
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
        logging.debug(f"Saving settings to: {file_path}")
    except Exception as e:
        logging.error(f"Error saving settings to {file_path}: {e}")
