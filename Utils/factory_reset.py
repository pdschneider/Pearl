# Utils/factory_reset.py
import shutil
import sys
import os
import logging
from PySide6.QtWidgets import QMessageBox
from Utils.load_settings import load_data_path


def factory_reset_config(globals, error=None):
    """Deletes the entire configuration folder for Pearl."""
    # Create a messagebox
    msg = QMessageBox()
    msg.setWindowTitle("A Critical Error Occurred!")
    msg.setText(
"""It looks like you ran into an error while building the GUI!
Would you like to reset settings back to defaults?""")
    msg.setInformativeText(f"Error: {error}")
    msg.setDetailedText(
"""This is a rare error.

Sometimes settings files from older versions of Pearl can conflict with newer releases, or vice versa.
Clicking yes will delete all current configuration files for Pearl.

This will not affect your saved chats or logs, but it will require you to reinstall Kokoro if it was previously installed via Pearl.

Deleting settings files fixes some errors, but not all.

If this issue persists, send a report to bugs@phillipplays.com.""")
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg.setDefaultButton(QMessageBox.StandardButton.Yes)

    # Call the messagebox
    reply = msg.exec()
    
    # Remove the entire config folder 
    if reply == QMessageBox.StandardButton.Yes:
        shutil.rmtree(load_data_path("config"))
        sys.exit(0)



def total_factory_reset(globals):
    """Completely wipes all Pearl-related data."""
    answer = QMessageBox.question(
        None,
        "Reset Pearl?",
"""Danger - This will reset all of your settings, chats, and logs.

Do you wish to completely wipe all Pearl-related data?""",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    if answer == QMessageBox.StandardButton.Yes:
        try:
            if os.path.isdir(load_data_path("config")):
                shutil.rmtree(load_data_path("config"))
            if os.path.isdir(load_data_path("local")):
                shutil.rmtree(load_data_path("local"))
            if os.path.isdir(load_data_path("cache")):
                shutil.rmtree(load_data_path("cache"))

            # Show success box
            QMessageBox.information(
                None,
                "Reset Successful!",
                "Successfully deleted all Pearl-related data!",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok)

        # Exit on exception
        except Exception as e:
            logging.error(f"Unable to perform reset due to: {e}")
            QMessageBox.warning(
                None,
                "Reset Failed",
                f"Unable to perform reset due to: {e}",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok)
            return
