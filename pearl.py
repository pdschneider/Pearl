# pearl.py
import sys
import logging
from src.utils.dependencies import check_dependencies
check_dependencies()
from config import globals
from src.utils.startup import startup
from src.interface.interface import create_interface
from src.utils.startup import startup
from src.utils.save_settings import save_all_settings
from src.utils.factory_reset import factory_reset_config


# Tests dependencies and sets flags
startup(globals)

def on_closing():
    """Saves all settings and shuts down logging before closing the program."""
    try:
        save_all_settings(globals, reject_toast=True)
    except Exception as e:
        logging.error(f"Error occurred when saving settings: {e}")
    globals.root.withdraw()
    globals.root.quit()
    globals.root.destroy()
    if globals.startup_root:
        globals.startup_root.quit()
    logging.shutdown()

if __name__ == "__main__":
    # Initialize GUI
    if getattr(sys, 'frozen', False):  # If bundled
        try:
            create_interface(globals)
            globals.root.protocol("WM_DELETE_WINDOW", on_closing)
            globals.root.mainloop()
        except Exception as error:
            logging.critical(f"Creash in bundled mode!")
            factory_reset_config(globals, error)
            if globals.root:
                try:
                    globals.root.quit()
                except Exception as e:
                    logging.error(f"Error occurred when closing window: {e}")
    else:  # Not bundled
        create_interface(globals)
        globals.root.protocol("WM_DELETE_WINDOW", on_closing)
        globals.root.mainloop()
