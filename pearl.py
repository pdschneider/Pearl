# pearl.py
# v0.1.10
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

- Supports attachments for filetypes: .txt, .csv, .json, .py, .pyw, .log, .ini, .cfg, .xml, .sh, .bat, .ps1, .md, .tsv, .toml, .yaml, .html, .css, .spec
- Added experimental underlying context model choice
- Copy button for messages
- New chat button to the top bar
- Internal logging for each chat message's token count
- Separated default settings from development settings for a more consistent default user experience
- Added tooltips
- Minor bug fixes and improvements

"""