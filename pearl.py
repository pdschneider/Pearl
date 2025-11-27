# pearl.py
# v0.1.1
from config import Globals, setup_logging
from Interface.interface import create_interface
from Connections.ollama import ollama_test
from Managers.speech import kokoro_test

# Sets up logging
setup_logging()

# Initiates global variables
globals = Globals()

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

- Added requirements.txt
- Added rotating log files
- Improved error handling 
- Added setup instructions for users without Ollama installed

"""