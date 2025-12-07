# config.py
import customtkinter as ctk
import os, json, sys, logging, platform, shutil
from logging.handlers import TimedRotatingFileHandler

os_name = platform.platform()
pyinstaller_bundle = getattr(sys, 'frozen', False)
if pyinstaller_bundle:
    logging.info(f"Application built with Pyinstaller.")

class Globals:
    """Class to store global variables"""
    def __init__(self):
        """Initializes settings variables from refresh_globals."""
        all_prompts = load_prompts()
        self.refresh_globals()

        # Current Version
        self.current_version = "v0.1.7"

        # Temporary Variables
        self.theme_var = None
        self.logging_var = None
        self.tts_var = None
        self.active_voice_var = None
        self.tts_source_var = None
        self.save_chats_var = None

        # UI variables
        self.root = None
        self.chat_page = None
        self.tabview = None
        self.model_tree = None
        self.settings_overlay = None
        self.setup_page = None
        self.top_bar = None
        self.main_frame = None
        self.assistant_label = None
        self.theme_path = None
        self.theme_dict = None
        self.greeting = "Pearl at your service!"
        self.ollama_download_tooltip = None
        self.kokoro_download_tooltip = None

        # Chat Variables
        self.chat_history = []
        self.system_prompt = all_prompts.get(self.active_prompt)
        self.chat_history.append({"role": "system", "content": all_prompts.get(self.active_prompt, {}).get("prompt", "")})
        self.chat_message = None
        self.assistant_message = ""

        # Flags
        self.ollama_active = None
        self.kokoro_active = None
        self.ram_found = None
        self.cpu_found = None
        self.gpu_found = None
        self.ollama_download_state = None
        self.kokoro_download_state = None

    def refresh_globals(self):
        """Reloads all settings from disk and updates the class."""
        settings = load_settings()
        self.all_prompts = load_prompts()

        # Variables from settings
        self.active_model = settings.get("active_model", "llama3.2:3b")
        self.active_voice = settings.get("active_voice", "af_heart")
        self.active_prompt = settings.get("active_prompt", "Assistant")
        self.tts_enabled = settings.get("tts_enabled", False)
        self.tts_source = settings.get("tts_source", "default")
        self.dynamic_mode = settings.get("dynamic_mode", False)
        self.active_theme = settings.get("active_theme", "cosmic_sky")
        self.logging_level = settings.get("logging_level", "INFO")
        self.save_chats = settings.get("save_chats", False)

def get_data_path(direct=None, filename=None):
    """
    Get the path to a writable data folder or a specific file, copying bundled files if needed.

    Args:
    direct = The file type to specify its directory, either configuration, persistent user data, or logs.
    filename = The file name being accessed.

    """
    if getattr(sys, 'frozen', False):  # Running as bundled executable
        if direct == "config":
            if os_name.startswith("Windows"):
                persistent_dir = os.path.normpath(os.path.join(os.getenv("APPDATA"), "Pearl"))
            else:
                persistent_dir = os.path.normpath(os.path.expanduser("~/.config/Pearl"))
                if not os_name.startswith("Linux"):
                    logging.warning(f"OS not found. Defaulting to Linux paths.")
            default_files = ["settings.json", 
                             "context.json", 
                             "prompts.json", 
                             "tts.json", 
                             "themes/cosmic_sky.json", 
                             "themes/pastel_green.json", 
                             "themes/blazing_red.json", 
                             "themes/dark_cloud.json", 
                             "themes/soft_light.json"]
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
        try:
            if "themes/" in str(default_files):  # checks if any file has themes/ path
                themes_dir = os.path.join(persistent_dir, "themes")
                os.makedirs(themes_dir, exist_ok=True)
            os.makedirs(persistent_dir, exist_ok=True)
            if not os.access(persistent_dir, os.W_OK):
                raise PermissionError(f"No write permission for {persistent_dir}")
        except Exception as e:
            logging.error(f"Error creating persistent data directory: {e}")
            raise
        bundled_dir = os.path.normpath(os.path.join(sys._MEIPASS, "data"))
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
    else:  # Running in development
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.normpath(os.path.join(base_dir, "data"))
        try:
            os.makedirs(data_dir, exist_ok=True)
            if not os.access(data_dir, os.W_OK):
                raise PermissionError(f"No write permission for {data_dir}")
        except Exception as e:
            logging.error(f"Error creating data directory: {e}")
            raise
    logging.debug(f"Accessing data directory: {data_dir}")
    return os.path.normpath(os.path.join(data_dir, filename)) if filename else data_dir

def load_settings():
    try:
        with open(get_data_path("config", 'settings.json')) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load settings.json due to: {e}.")
        return {}

def save_settings(**kwargs):
    """Save settings to settings.json."""
    settings = load_settings()
    settings.update(kwargs)
    file_path = os.path.normpath(get_data_path("config", "settings.json"))
    try:
        with open(file_path, 'w') as f:
            json.dump(settings, f, indent=4)
        logging.info(f"Saving settings to: {file_path}")
    except Exception as e:
        logging.error(f"Error saving settings to {file_path}: {e}")

def load_prompts():
    try:
        with open(get_data_path("config", 'prompts.json')) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load prompts.json ({e}), using default prompts")
        return {"Custom": {"prompt": "", "greeting": "Pearl at your service!"}}

def apply_theme(name: str) -> None:
    """Loads the user's chosen theme and applies it to ctk widgets."""
    try:
        globals.theme_path = os.path.normpath(os.path.join(get_data_path(direct="config"), f"themes/{globals.active_theme}.json"))
        try:
            with open(globals.theme_path, 'r') as f:
                globals.theme_dict = json.load(f)
        except:
            logging.warning(f"Unable to load theme into dictionary.")
        ctk.set_default_color_theme(globals.theme_path)
        logging.debug(f"CTk theme found at: {globals.theme_path}")
    except Exception as e:
        logging.warning(f"Could not retrieve CTk active theme due to: {e}")

def setup_logging():
    """Sets up logging for both the log file as well as standard console output."""
    logging.getLogger().handlers.clear()  # Clears output destinations
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logs_dir = os.path.join(get_data_path(direct="cache"), "logs")  # Sets up logs folder
    os.makedirs(logs_dir, exist_ok=True)  # Creates the logs folder if it doesn't exist

    # Sets up logging to files
    logfile_handler = TimedRotatingFileHandler(os.path.join(logs_dir, "pearl.log"), when="midnight", backupCount=50)
    logfile_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logging.getLogger().addHandler(logfile_handler)

    # Loads correct logging level from settings
    settings = load_settings()
    logging.root.setLevel(getattr(logging, settings.get("logging_level", "INFO")))

    logging.info(f"File and console logging initialized.")

globals = Globals()
