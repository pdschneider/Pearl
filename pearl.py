# pearl.py
# v0.1.0
from Interface.interface import create_interface
from config import Globals

# Initiates global variables and GUI
globals = Globals()
create_interface(globals)

# Start the Tkinter main event loop
globals.root.mainloop()

"""
Changelog:

- Created wireframe
- Added Cosmic Sky theme
- Added Pastel Green theme
- Ollama functions for model fetching, unloading, and chat
- Budget script for later implementation
- TTS script for later implementation
- Hardware checking script for later implementation
- Chat page, models page, and settings page
- Context script for later implementation
- Added models list treeview
- Added load and unload buttons to models treeview
- Added logging
- Added docstrings to most functions
- Added logging level setting
- Corrected file paths for Windows or Linux
- Added load/unload models buttons
- Added button for selecting active model
- Added persistent chat history
- Added changelog

"""