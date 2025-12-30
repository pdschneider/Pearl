# pearl.py
# v0.1.11
from config import globals, setup_logging
from Interface.interface import create_interface
from Utils.startup import startup
from Utils.save_settings import save_all_settings

# Sets up logging
setup_logging()

# Tests dependencies and sets flags
startup(globals)

# Initialize GUI
create_interface(globals)

def on_closing():
    """Saves all settings before closing the program."""
    try:
        save_all_settings(globals)
    except:
        pass
    globals.root.destroy()
globals.root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main event loop
globals.root.mainloop()

"""
Changelog:

- Dynamic prompt switching with context model enabled
- Added model name underneath assistant messages
- Added time groups to chat history view
- Added start/end times to assistant messages
- File attachment paths are logged for each message
- Added view logs button to advanced tab
- Added github button to about tab
- Remembers window placement for more consistent user experience
- Minor bug fixes and improvements

"""