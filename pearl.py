# pearl.py
from config import globals
from Utils.startup import startup
from Interface.interface import create_interface
from Utils.startup import startup
from Utils.save_settings import save_all_settings
from Utils.factory_reset import factory_reset_config
import sys
import logging


# Tests dependencies and sets flags
startup(globals)


def on_closing():
    """Saves all settings before closing the program."""
    try:
        save_all_settings(globals, reject_toast=True)
    except Exception as e:
        logging.error(f"Error occurred when saving settings: {e}")
    globals.root.quit()

if __name__ == "__main__":
    # Initialize GUI
    if getattr(sys, 'frozen', False):  # If bundled
        try:
            logging.debug(f"About to call create_interface()...")
            create_interface(globals)
            logging.info(f"create_interface() returned successfully!")
            globals.root.protocol("WM_DELETE_WINDOW", on_closing)
            logging.debug(f"Entering mainloop...")
            globals.root.mainloop()
        except Exception as error:
            logging.critical(f"Creash in bundled mode!")
            factory_reset_config(error)
            if globals.root:
                try:
                    globals.root.destroy()
                except Exception as e:
                    logging.error(f"Error occurred when closing window: {e}")
    else:  # Not bundled
        create_interface(globals)
        globals.root.protocol("WM_DELETE_WINDOW", on_closing)
        globals.root.mainloop()
