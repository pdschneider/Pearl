# src/qt_interface/qt_settings/save_qt.py
import logging
from src.utils.save_settings import save_settings
from src.utils.load import load_settings


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

    # Update the globs object immediately
    globs.github_check = new_github_check
    globs.beta = new_beta
    globs.dynamic_window_size = new_window_size
    globs.legacy_mode = new_legacy_mode
    globs.logging_level = new_logging_level

    # Load current settings to merge with new value
    current_settings = load_settings()
    current_settings["github_check"] = new_github_check
    current_settings["beta"] = new_beta
    current_settings["dynamic_window_size"] = new_window_size
    current_settings["legacy_mode"] = new_legacy_mode
    current_settings["logging_level"] = new_logging_level
    current_settings["previous_version"] = globs.current_version

    # Save to JSON file
    try:
        save_settings(**current_settings)
        logging.info(f"Setting Saved!")

    except Exception as e:
        logging.error(f"Failed to save settings: {e}")
