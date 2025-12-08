# pearl.py
# v0.1.8
from config import globals, setup_logging
from Interface.interface import create_interface
from Utils.startup import startup

# Sets up logging
setup_logging()

# Tests dependencies and sets flags
startup(globals)

# Initialize GUI
create_interface(globals)

# Start the Tkinter main event loop
globals.root.mainloop()

"""
Changelog:

- Ships as AppImage for Linux users
- Added progress bar for slow startup scenarios
- Added program icon
- Added sidebar for later chat history implementation
- Added changelog page
- Moved startup logic to new script
- Added context detection logging
- Minor bug fixes and improvements

"""
