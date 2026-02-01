# pearl.py
# v0.1.12

# Tests dependencies and sets flags
from config import globals
from Utils.startup import startup
startup(globals)

# Imports
from Interface.interface import create_interface
from Utils.startup import startup
from Utils.save_settings import save_all_settings
from Utils.factory_reset import factory_reset
import sys, logging

# Tests dependencies and sets flags
startup(globals)

def on_closing():
    """Saves all settings before closing the program."""
    try:
        save_all_settings(globals)
    except Exception as e:
        logging.error(f"Error occurred when saving settings: {e}")
    globals.root.destroy()

# Initialize GUI
if getattr(sys, 'frozen', False):  # If bundled
    try:
        create_interface(globals)
        globals.root.protocol("WM_DELETE_WINDOW", on_closing)
        globals.root.mainloop()
    except Exception as error:
        if globals.root:
            try:
                globals.root.destroy()
            except Exception as e:
                logging.error(f"Error occurred when destroying window: {e}")
        factory_reset(error)
else:  # Not bundled
    create_interface(globals)
    globals.root.protocol("WM_DELETE_WINDOW", on_closing)
    globals.root.mainloop()

"""
Changelog:

- Added startup checks which analyze and sanitize corrupted values and files
- Moved loading logic to new load_settings.py
- Draws window in the center of the screen when opening the program for the first time
- Improved logic for opening the logs folder on Windows
- Normalized buttons across operating systems with updated icons
- Added bug report icon to top bar that opens default email application
- Added delete all chats button in settings
- Added factory reset option upon GUI failure
- Added paperclip icon underneath user messages to indicate a file attachment
- Added icons to settings pages
- Updated dependencies
- General stability & UI improvements

"""
