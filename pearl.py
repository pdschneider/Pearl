# pearl.py
# v0.1.4
from config import globals, setup_logging
from Interface.interface import create_interface
from Connections.ollama import ollama_test
from Managers.speech import kokoro_test
from Utils.hardware import get_hardware_stats

# Sets up logging
setup_logging()

# Tests dependencies and sets flags
ollama_success = ollama_test()
if ollama_success:
    globals.ollama_active = True
kokoro_success = kokoro_test()
if kokoro_success:
    globals.kokoro_active = True

# Query for hardware stats
get_hardware_stats()

# Initialize GUI
create_interface(globals)

# Start the Tkinter main event loop
globals.root.mainloop()

"""
Changelog:

- Added universal cross-platform default TTS
- UI improvements
- Queries and logs CPU/RAM/GPU data for logging & error handling
- General error handling improvements

"""