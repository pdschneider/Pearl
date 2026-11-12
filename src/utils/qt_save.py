# src/qt_interface/qt_settings/qt_save.py
import logging
import json
import os
from src.utils.save_settings import save_settings
from src.utils.load import load_settings, load_tools, load_data_path
from PySide6.QtCore import Qt


def save_qt_settings(globs):
    """
    Save Qt-specific settings to JSON.
    Currently handles only the GitHub check setting.
    """

    # Read the checkbox states
    new_github_check = globs.github_check_checkbox.isChecked()
    new_beta = globs.beta_checkbox.isChecked()
    new_window_size = globs.window_checkbox.isChecked()
    new_legacy_mode = globs.legacy_checkbox.isChecked()
    new_logging_level = globs.logging_level_box.currentText().upper()
    new_generate_titles = globs.generate_titles_checkbox.isChecked()
    new_tts_enabled = globs.tts_button.isChecked()
    new_chat_path = globs.ollama_chat_path_box.text().strip() or "http://localhost:11434/"
    new_title_path = globs.ollama_title_path_box.text().strip() or "http://localhost:11434/"

    # Checkbox States for Tools
    new_password_generator = globs.password_generator_checkbox.isChecked()

    # Update the globs object immediately
    globs.github_check = new_github_check
    globs.beta = new_beta
    globs.dynamic_window_size = new_window_size
    globs.legacy_mode = new_legacy_mode
    globs.logging_level = new_logging_level
    globs.generate_titles = new_generate_titles
    globs.tts_enabled = new_tts_enabled
    globs.ollama_chat_path = new_chat_path
    globs.ollama_title_path = new_title_path
    globs.password_generator = new_password_generator

    # Load current settings to merge with new value
    current_settings = load_settings()
    current_settings["github_check"] = new_github_check
    current_settings["beta"] = new_beta
    current_settings["dynamic_window_size"] = new_window_size
    current_settings["legacy_mode"] = new_legacy_mode
    current_settings["logging_level"] = new_logging_level
    current_settings["previous_version"] = globs.current_version
    current_settings["generate_titles"] = new_generate_titles
    current_settings["tts_enabled"] = new_tts_enabled
    current_settings["tts_source"] = globs.tts_source
    current_settings["kokoro_active_voice"] = globs.kokoro_active_voice
    current_settings["default_sink"] = globs.default_sink
    current_settings["ollama_chat_path"] = new_chat_path
    current_settings["ollama_title_path"] = new_title_path

    # Load current tools to merge with new value
    current_tools = load_tools()
    current_tools["password_generator"] = new_password_generator

    def save_window_placement(globs):
        if globs.window.windowState() != Qt.WindowState.WindowMaximized:
            try:
                current_geometry = globs.window.geometry()
                current_width = current_geometry.width()
                current_height = current_geometry.height()
                current_horizontal_placement = current_geometry.x()
                current_vertical_placement = current_geometry.y()
                
                logging.debug(f"Window size: {current_width}x{current_height}")
                logging.debug(f"Window position: ({current_horizontal_placement}, {current_vertical_placement})")
                
                # Store geometry in current_settings so it gets saved
                current_settings["saved_x"] = current_horizontal_placement
                current_settings["saved_y"] = current_vertical_placement
                current_settings["saved_width"] = current_width
                current_settings["saved_height"] = current_height
                globs.saved_x = current_horizontal_placement
                globs.saved_y = current_vertical_placement
                globs.saved_width = current_width
                globs.saved_height = current_height

            except Exception as e:
                logging.debug(f"Could not save window placement due to {e}")
        else:
            logging.debug("Window is maximized, skipping placement save")

    # Save geometry
    save_window_placement(globs)

    # Save to JSON file
    try:
        save_settings(**current_settings)
        save_tools(**current_tools)
        logging.info(f"Setting Saved!")
    except Exception as e:
        logging.error(f"Failed to save settings: {e}")


def save_tools(**kwargs):
    """Save settings to settings.json."""
    tools = load_tools()
    tools.update(kwargs)
    file_path = os.path.normpath(load_data_path("config", "tools.json"))
    try:
        with open(file_path, 'w') as f:
            json.dump(tools, f, indent=4)
        logging.debug(f"Saving tools to: {file_path}")
    except Exception as e:
        logging.error(f"Error saving tools to {file_path}: {e}")
