# config.py
import customtkinter as ctk
import os, json, sys, logging, platform
from Utils.load_settings import load_prompts, load_settings, load_context, load_data_path

pyinstaller_bundle = getattr(sys, 'frozen', False)
if pyinstaller_bundle:
    logging.info(f"Application built with Pyinstaller.")

class Globals:
    """Class to store global variables"""
    def __init__(self):
        """Initializes settings variables from refresh_globals."""
        self.all_prompts = load_prompts()
        self.refresh_globals()

        # Current Version
        self.current_version = "v0.1.12"

        # Tkinter Variables
        self.theme_var = None
        self.logging_var = None
        self.tts_var = None
        self.active_voice_var = None
        self.tts_source_var = None
        self.save_chats_var = None
        self.sink_var = None

        # UI variables
        self.root = None
        self.ui_elements = None
        self.file_button = None
        self.attach_tip = None

        # Icons
        self.hamburger_icon = None
        self.settings_icon = None
        self.new_chat_icon = None
        self.send_icon = None
        self.stop_icon = None
        self.attach_icon = None
        self.bug_icon = None
        self.delete_icon = None
        self.chat_icon = None
        self.chats_icon = None
        self.curve_up_icon = None
        self.location_icon = None
        self.ollama_icon = None
        self.phone_icon = None
        self.sound_high_icon = None
        self.sound_low_icon = None
        self.speaker_icon = None
        self.theme_icon = None
        self.preferences_icon = None

        # Pages
        self.main_frame = None
        self.startup_root = None
        self.chat_page = None
        self.tabview = None
        self.model_tree = None
        self.settings_overlay = None
        self.changelog = None
        self.sidebar = None

        # Miscellaneous
        self.active_prompt = "Assistant"
        self.setup_page = None
        self.top_bar = None
        self.hamburger = None
        self.assistant_label = None
        self.theme_path = None
        self.theme_dict = None
        self.greeting = "Pearl at your service!"
        self.sink_list = None
        self.conversation_history = []
        self.conversation_id = None
        self.created_at = None
        self.message_start_time = None
        self.message_end_time = None

        # Tooltips
        self.ollama_download_tooltip = None
        self.kokoro_download_tooltip = None

        # Chat Variables
        self.chat_history = []
        self.system_prompt = self.all_prompts[f"{self.active_prompt}"]["prompt"]
        self.chat_history.append({"role": "system", "content": self.all_prompts.get(self.active_prompt, {}).get("prompt", "")})
        self.chat_message = None
        self.assistant_message = ""
        self.file_attachment = None
        self.attachment_path = None

        # Flags
        self.ollama_active = None
        self.kokoro_active = None
        self.ram_found = None
        self.cpu_found = None
        self.gpu_found = None
        self.ollama_download_state = None
        self.kokoro_download_state = None
        self.sidebar_open = False
        self.is_new_conversation = True
        self.still_streaming = False

        # Miscellaneous Variables
        self.icon = None
        self.cancel_event = None
        self.current_response_id = None
        self.os_name = platform.system()

    def refresh_globals(self):
        """Reloads all settings from disk and updates the class."""
        settings = load_settings()
        self.all_prompts = load_prompts()
        self.all_context = load_context()

        # Variables from settings
        self.active_model = settings.get("active_model", "llama3.2:3b")
        self.active_voice = settings.get("active_voice", "af_heart")
        self.tts_enabled = settings.get("tts_enabled", False)
        self.tts_source = settings.get("tts_source", "default")
        self.dynamic_mode = settings.get("dynamic_mode", False)
        self.active_theme = settings.get("active_theme", "cosmic_sky")
        self.logging_level = settings.get("logging_level", "INFO")
        self.save_chats = settings.get("save_chats", False)
        self.default_sink = settings.get("default_sink", "Default")
        self.context_model = settings.get("context_model", "llama3.2:3b")
        self.saved_width = settings.get("saved_width", 850)
        self.saved_height = settings.get("saved_height", 850)
        self.saved_x = settings.get("saved_x", -1)
        self.saved_y = settings.get("saved_y", -1)

def apply_theme(name: str) -> None:
    """Loads the user's chosen theme and applies it to ctk widgets."""
    try:
        globals.theme_path = os.path.normpath(os.path.join(load_data_path(direct="config"), f"themes/{globals.active_theme}.json"))
        try:
            with open(globals.theme_path, 'r') as f:
                globals.theme_dict = json.load(f)
        except:
            logging.warning(f"Unable to load theme into dictionary.")
        ctk.set_default_color_theme(globals.theme_path)
        logging.debug(f"CTk theme found at: {globals.theme_path}")
    except Exception as e:
        logging.warning(f"Could not retrieve CTk active theme due to: {e}")

globals = Globals()
