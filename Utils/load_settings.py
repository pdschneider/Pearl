# Utils/load_settings.py
import os, logging, sys, shutil, json, platform

def load_data_path(direct=None, filename=None):
    """
    Get the path to a writable data folder or a specific file, copying bundled files if needed.

            Parameters:
                    direct = The file type to specify its directory, either configuration, persistent user data, or logs
                    filename = The file name being accessed

    """
    os_name = platform.platform()
    default_files = ["settings.json", 
                             "context.json", 
                             "prompts.json", 
                             "assets/Pearl.png",
                             "assets/Pearl_Sparkle.png",
                             "assets/attach-1.png",
                             "assets/attach-2.png",
                             "assets/attach-3.png",
                             "assets/attach-4.png",
                             "assets/bug-1.png",
                             "assets/bug-2.png",
                             "assets/bug-3.png",
                             "assets/ellipses.png",
                             "assets/hamburger.png",
                             "assets/pen-1.png",
                             "assets/pen-2.png",
                             "assets/pencil.png",
                             "assets/send.png",
                             "assets/settings.png",
                             "assets/stop-1.png",
                             "assets/stop-2.png",
                             "assets/stop-3.png",
                             "assets/stop-4.png",
                             "assets/toggle.png",
                             "assets/copy.png",
                             "assets/check-1.png",
                             "assets/cancel.png",
                             "assets/chat.png",
                             "assets/chats.png",
                             "assets/curve-up.png",
                             "assets/location.png",
                             "assets/note.png",
                             "assets/notification-1.png",
                             "assets/notification-2.png",
                             "assets/notification-3.png",
                             "assets/ollama.png",
                             "assets/phone.png",
                             "assets/settings-2.png",
                             "assets/sound_high.png",
                             "assets/sound_low.png",
                             "assets/speaker.png",
                             "assets/theme.png",
                             "assets/preferences.png",
                             "themes/cosmic_sky.json", 
                             "themes/pastel_green.json", 
                             "themes/blazing_red.json", 
                             "themes/dark_cloud.json", 
                             "themes/soft_light.json"]

    if getattr(sys, 'frozen', False):  # Running as bundled executable
        if direct == "config":
            if os_name.startswith("Windows"):
                persistent_dir = os.path.normpath(os.path.join(os.getenv("APPDATA"), "Pearl"))
            else:
                persistent_dir = os.path.normpath(os.path.expanduser("~/.config/Pearl"))
                if not os_name.startswith("Linux"):
                    logging.warning(f"OS not found. Defaulting to Linux paths.")
        elif direct == "local":
            if os_name.startswith("Windows"):
                persistent_dir = os.path.normpath(os.path.join(os.getenv("LOCALAPPDATA"), "Pearl"))
            else:
                persistent_dir = os.path.normpath(os.path.expanduser("~/.local/share/Pearl"))
                if not os_name.startswith("Linux"):
                    logging.warning(f"OS not found. Defaulting to Linux paths.")
            default_files = []
        else:
            if os_name.startswith("Windows"):
                persistent_dir = os.path.normpath(os.path.join(os.getenv("LOCALAPPDATA"), "Pearl", "Cache"))
            else:
                persistent_dir = os.path.normpath(os.path.expanduser("~/.cache/Pearl"))
                if not os_name.startswith("Linux"):
                    logging.warning(f"OS not found. Defaulting to Linux paths.")
            default_files = []

        # Checks if any file has themes/ or assets/ path
        try:
            if "themes/" in str(default_files):
                themes_dir = os.path.join(persistent_dir, "themes")
                os.makedirs(themes_dir, exist_ok=True)
            if "assets/" in str(default_files):
                assets_dir = os.path.join(persistent_dir, "assets")
                os.makedirs(assets_dir, exist_ok=True)
            os.makedirs(persistent_dir, exist_ok=True)
            if not os.access(persistent_dir, os.W_OK):
                raise PermissionError(f"No write permission for {persistent_dir}")
        except Exception as e:
            logging.error(f"Error creating persistent data directory: {e}")
            raise
        bundled_dir = os.path.normpath(os.path.join(sys._MEIPASS, "defaults"))
        for default_file in default_files:
            bundled_file = os.path.normpath(os.path.join(bundled_dir, default_file))
            persistent_file = os.path.normpath(os.path.join(persistent_dir, default_file))
            if os.path.exists(bundled_file) and not os.path.exists(persistent_file):
                try:
                    logging.info(f"Copying {default_file} from {bundled_file} to {persistent_file}")
                    shutil.copy(bundled_file, persistent_file)
                except Exception as e:
                    logging.error(f"Error copying {default_file}: {e}")
        data_dir = persistent_dir

    else:  #  Running in development
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.normpath(os.path.join(base_dir, "data"))
        defaults_dir = os.path.normpath(os.path.join(base_dir, "defaults"))

        # Checks if any file has themes/ or assets/ path
        try:
            os.makedirs(data_dir, exist_ok=True)
            if "themes/" in str(default_files):
                themes_dir = os.path.join(data_dir, "themes")
                os.makedirs(themes_dir, exist_ok=True)
            if "assets/" in str(default_files):
                assets_dir = os.path.join(data_dir, "assets")
                os.makedirs(assets_dir, exist_ok=True)
            if not os.access(data_dir, os.W_OK):
                raise PermissionError(f"No write permission for {persistent_dir}")
        except Exception as e:
            logging.error(f"Error creating persistent data directory: {e}")
            raise

        # Loads defaults
        for default_file in default_files:
            bundled_file = os.path.normpath(os.path.join(defaults_dir, default_file))
            persistent_file = os.path.normpath(os.path.join(data_dir, default_file))

            if os.path.exists(bundled_file) and not os.path.exists(persistent_file):
                try:
                    logging.info(f"Copying {default_file} from {bundled_file} to {persistent_file}")
                    shutil.copy(bundled_file, persistent_file)
                except Exception as e:
                    logging.error(f"Error copying {default_file}: {e}")
        try:
            os.makedirs(data_dir, exist_ok=True)
            if not os.access(data_dir, os.W_OK):
                raise PermissionError(f"No write permission for {data_dir}")
        except Exception as e:
            logging.error(f"Error creating data directory: {e}")
            raise
    return os.path.normpath(os.path.join(data_dir, filename)) if filename else data_dir

def load_settings():
    try:
        with open(load_data_path("config", 'settings.json')) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load settings.json due to: {e}.")
        return {}

def load_prompts():
    """Loads the prompts dictionary."""
    try:
        with open(load_data_path("config", 'prompts.json')) as f:
            logging.debug(f"Successfully loaded prompts dictionary.")
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load prompts.json due to: {e}")
        return {"greeting": "Pearl at your service!"}

def load_context():
    """Load context keywords from JSON file, return empty dict on failure."""
    try:
        with open(load_data_path("config", 'context.json')) as f:
            logging.debug(f"Successfully loaded context dictionary.")
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading context.json: {e}")
        return {}
