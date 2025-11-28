# pearl.py
# v0.1.2
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

- Skips intitial Ollama API requests when Ollama is not found, speeding up loading on systems without Ollama.
- Added TTS (requires Kokoro)
- Suppressed requests debug log messages
- Added dynamic settings updates

"""