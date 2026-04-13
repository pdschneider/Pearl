import sys
import logging
from src.utils.dependencies import check_dependencies
check_dependencies()
from config import globals
from src.qt_interface.qt_interface import create_interface
from src.interface.setup.setup_wizard import create_wizard
from src.utils.startup import startup


startup(globals)

globals.qt_mode = True

if not globals.ollama_active:
    create_wizard(globals)

if __name__ == "__main__":
    # Initialize GUI
    create_interface(globals)
    sys.exit(globals.app.exec())
