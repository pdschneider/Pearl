# src/utils/save_settings.py
import logging
import os
import json
from src.utils.load import load_settings, load_data_path
from config import apply_theme
from src.utils.toast import show_toast


def save_all_settings(globs, reject_toast=False):
    """
    Save all settings to JSON files and update globs.

    Args:
        globs: The global configuration object
                    containing UI variables and settings.
    """

    # Load current settings
    settings = load_settings()
    current_logging_level = globs.logging_var.get()
    current_active_theme = globs.theme_var.get()
    current_tts = globs.tts_var.get()
    current_kokoro_active_voice = globs.kokoro_active_voice_var.get()
    current_default_active_voice = globs.default_active_voice_var.get()
    current_tts_source = globs.tts_source_var.get()
    current_save_chats = globs.save_chats_var.get()
    current_sink = globs.sink_var.get()
    current_github_check = globs.github_check_var.get()
    current_beta = globs.beta_var.get()
    current_ollama_chat_path = globs.ollama_chat_path_var.get()
    current_ollama_context_path = globs.ollama_context_path_var.get()
    current_ollama_title_path = globs.ollama_title_path_var.get()
    current_enable_context = globs.enable_context_var.get()
    current_generate_titles = globs.generate_titles_var.get()
    current_dynamic_window_size = globs.dynamic_window_size_var.get()
    current_legacy_mode = globs.legacy_mode_var.get()

    # Handle logging level based on dev mode change
    logging_level = current_logging_level

    # Save Window Placement
    logging.debug(f"Root state: {globs.root.state()}")
    if globs.root.state() != "zoomed":  # don't save if maximized
        try:
            current_width = globs.root.winfo_width()
            current_height = globs.root.winfo_height()
            current_x = globs.root.winfo_x()
            current_y = globs.root.winfo_y()

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
            beta=current_beta,
            ollama_chat_path=current_ollama_chat_path,
            ollama_context_path=current_ollama_context_path,
            ollama_title_path=current_ollama_title_path,
            enable_context=current_enable_context,
            generate_titles=current_generate_titles,
            dynamic_window_size=current_dynamic_window_size,
            legacy_mode=current_legacy_mode)

    # Refresh Globals
    globs.refresh_globs()

    # Reload settings to update globs
    settings = load_settings()
    globs.logging_var.set(settings["logging_level"])
    globs.theme_var.set(settings["active_theme"])
    globs.tts_var.set(settings["tts_enabled"])
    globs.kokoro_active_voice_var.set(settings["kokoro_active_voice"])
    globs.default_active_voice_var.set(settings["default_active_voice"])
    globs.tts_source_var.set(settings["tts_source"])
    globs.save_chats_var.set(settings["save_chats"])
    globs.sink_var.set(settings["default_sink"])
    globs.github_check_var.set(settings["github_check"])
    globs.beta_var.set(settings["beta"])
    globs.ollama_chat_path_var.set(settings["ollama_chat_path"])
    globs.ollama_context_path_var.set(settings["ollama_context_path"])
    globs.ollama_title_path_var.set(settings["ollama_title_path"])
    globs.enable_context_var.set(settings["enable_context"])
    globs.generate_titles_var.set(settings["generate_titles"])
    globs.dynamic_window_size_var.set(settings["dynamic_window_size"])
    globs.legacy_mode_var.set(settings["legacy_mode"])

    # Update logging
    logging.root.setLevel(getattr(logging, settings["logging_level"]))

    # Apply new theme
    apply_theme(current_active_theme)

    if not reject_toast:
        show_toast(globs, "Saved!")
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
