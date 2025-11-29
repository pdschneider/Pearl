# pearl.py
# v0.1.3
from config import globals, setup_logging
from Interface.interface import create_interface
from Connections.ollama import ollama_test
from Managers.speech import kokoro_test

# Sets up logging
setup_logging()

# Tests dependencies and sets flags
ollama_success = ollama_test()
if ollama_success:
    globals.ollama_active = True
kokoro_success = kokoro_test()
if kokoro_success:
    globals.kokoro_active = True

# Initialize GUI
create_interface(globals)

# Start the Tkinter main event loop
globals.root.mainloop()

"""
Changelog:

- Updated fonts for Windows users
- Removed unused query_ollama function
- Added support for markdown italics, bold, and strikethrough
- Improved TTS by removing italics, bold, and strikethrough markdown from speech

"""