# pearl.py
# v0.1.7
import logging
from config import globals, setup_logging
from Interface.interface import create_interface
from Connections.ollama import ollama_test, load_model, get_loaded_models
from Managers.speech_manager import kokoro_test
from Utils.hardware import get_hardware_stats

# Sets up logging
setup_logging()

# Tests dependencies and sets flags
try:
    ollama_success = ollama_test()
    if ollama_success:
        globals.ollama_active = True
        loaded_models = get_loaded_models()
        if globals.active_model not in loaded_models:
            logging.debug(f"Attempting to load initial model....")
            load_model(globals.active_model)  # Loads the active model before startup
    kokoro_success = kokoro_test()
    if kokoro_success:
        globals.kokoro_active = True
except:
    logging.error(f"Initial Ollama/Kokoro setup failed.")

# Query for hardware stats
get_hardware_stats()

# Initialize GUI
create_interface(globals)

# Start the Tkinter main event loop
globals.root.mainloop()

"""
Changelog:

- Total overhaul of main chat UI
- Total overhaul of setup page
- Added about page
- Minor bug fixes and improvements
- Brought closer to PEP8 compliance

- Downgraded: Lost markdown text

"""
