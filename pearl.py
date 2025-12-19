# pearl.py
# v0.1.9
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

- Functional chat history introduced
- Added audio output selection (Linux Only)
- Minor bug fixes and improvements

"""
