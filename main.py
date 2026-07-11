# pearl.py
import sys
import logging
from src.utils.dependencies import check_dependencies
check_dependencies()
from config import globs
from src.utils.startup import startup
from src.interface.interface import create_interface
from src.qt_interface.qt_interface import create_qt_interface
from src.utils.startup import startup
from src.utils.save_settings import save_all_settings
from src.utils.factory_reset import factory_reset_config


# Tests dependencies and sets flags
startup(globs)


def on_closing():
    """Saves all settings and shuts down logging before closing the program."""
    try:
        save_all_settings(globs, reject_toast=True)
    except Exception as e:
        logging.error(f"Error occurred when saving settings: {e}")
    if globs.legacy_mode:
        globs.root.withdraw()
        globs.root.quit()
        globs.root.destroy()
        if globs.startup_root:
            globs.startup_root.quit()
    logging.shutdown()

if __name__ == "__main__":
    # Initialize GUI
    if not globs.legacy_mode:
        create_qt_interface(globs)
        sys.exit(globs.app.exec())
    else:
        if getattr(sys, 'frozen', False):  # If bundled
            try:
                create_interface(globs)
                globs.root.protocol("WM_DELETE_WINDOW", on_closing)
                globs.root.mainloop()
            except Exception as error:
                logging.critical(f"Crash in bundled mode!")
                factory_reset_config(globs, error)
                if globs.root:
                    try:
                        globs.root.quit()
                    except Exception as e:
                        logging.error(f"Error occurred when closing window: {e}")
        else:  # Not bundled
            create_interface(globs)
            globs.root.protocol("WM_DELETE_WINDOW", on_closing)
            globs.root.mainloop()
