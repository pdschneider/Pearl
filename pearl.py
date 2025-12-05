# pearl.py
# v0.1.6
import logging
from config import globals, setup_logging
from Interface.interface import create_interface
from Connections.ollama import ollama_test, load_model, get_loaded_models
from Managers.speech_manager import kokoro_test
from Utils.hardware import get_hardware_stats

# Sets up logging
setup_logging()

# Tests dependencies and sets flags
ollama_success = ollama_test()
if ollama_success:
    globals.ollama_active = True
    try:
        loaded_models = get_loaded_models()
        if globals.active_model not in loaded_models:
            logging.debug(f"Attempting to load initial model....")
            load_model(globals.active_model)
            logging.debug(f"Initial model load of {globals.active_model} succeeded!")
    except:
        logging.error(f"Initial model load failed.")
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

- Major UI overhaul
- Converted entire GUI to Custom Tkinter
- Added 3 new themes
- Improved folder path detection on Windows systems
- Improved logging

"""