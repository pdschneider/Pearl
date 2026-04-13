# config.py
import customtkinter as ctk
import os
import json
import sys
import logging
import platform
import pyttsx3
import threading
from PySide6.QtWidgets import QApplication, QMainWindow
from version import __version__
from src.utils.load_settings import (load_prompts,
                                 load_settings,
                                 load_context,
                                 load_data_path,
                                 load_ollama_sh,
                                 load_docker_debian,
                                 load_docker_ubuntu,
                                 load_docker_windows,
                                 load_kokoro_windows)


class Globals:
    """Class to store global variables"""
    def __init__(self):
        """Initializes settings variables from refresh_globals."""

        # Information loaded from files
        self.all_prompts = load_prompts()
        self.ollama_sh = load_ollama_sh()
        self.docker_debian = load_docker_debian()
        self.docker_ubuntu = load_docker_ubuntu()
        self.docker_windows = load_docker_windows()
        self.kokoro_windows = load_kokoro_windows()
        self.refresh_globals()

        # Current Version
        self.current_version = __version__
        self.latest_version = None
        self.ollama_version = None
        self.docker_version = None

        # PySide6 Widgets
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.qt_mode = None

        # Thread Locks
        self.speaking_lock = threading.Lock()
        self.prompt_lock = threading.Lock()

        # Tkinter Vars
        self.theme_var = None
        self.logging_var = None
        self.tts_var = None
        self.kokoro_active_voice_var = None
        self.default_active_voice_var = None
        self.tts_source_var = None
        self.save_chats_var = None
        self.sink_var = None
        self.github_check_var = None
        self.language_var = None
        self.ollama_chat_path_var = None
        self.ollama_context_path_var = None
        self.ollama_title_path_var = None
        self.enable_context_var = None
        self.generate_titles_var = None

        # Custom Tkinter Widgets
        self.send_button = None
        self.file_button = None
        self.entry_box = None

        # UI variables
        self.root = ctk.CTk()
        self.app_title = "Pearl at your service!"
        self.startup_root = None
        self.ui_elements = None
        self.attach_tip = None
        self.widget_rows = []
        self.hamburger = None

        # Wizard Buttons
        self.ollama_interactive_download_button = None
        self.ollama_web_download_button = None
        self.docker_interactive_download_button = None
        self.docker_web_download_button = None
        self.kokoro_interactive_download_button = None
        self.kokoro_web_download_button = None

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
        self.chats_icon = None
        self.config_icon = None
        self.notification_icon = None
        self.docker_icon = None
        self.kokoro_icon = None
        self.en_language_icon = None
        self.pearl_icon = None
        self.no_sound_icon = None
        self.stats_icon = None
        self.operations_icon = None
        self.title_icon = None

        # Pages
        self.main_frame = None
        self.chat_page = None
        self.setup_page = None
        self.settings_page = None
        self.tabview = None
        self.model_tree = None
        self.changelog = None
        self.sidebar = None
        self.top_bar = None

        # Miscellaneous
        self.active_prompt = "Assistant"
        self.assistant_label = None
        self.theme_path = None
        self.theme_dict = None
        self.last_message_time = 0.0

        # Tooltips
        self.ollama_web_download_tooltip = None
        self.ollama_interactive_download_tooltip = None
        self.docker_web_download_tooltip = None
        self.docker_interactive_download_tooltip = None
        self.kokoro_download_tooltip = None

        # Chat Variables
        self.chat_history = []
        self.system_prompt = self.all_prompts[f"{self.active_prompt}"]["prompt"]
        self.chat_history.append({"role": "system",
                                  "content":
                                  self.all_prompts.get(self.active_prompt,
                                                       {}).get("prompt", "")})
        self.chat_message = None
        self.assistant_message = ""
        self.file_attachment = None
        self.attachment_path = None
        self.markdown_components = ["***", "___", "**", "__", "~~", "#####", "####", "###"]
        self.conversation_history = []
        self.conversation_id = None
        self.created_at = None
        self.message_start_time = None
        self.message_end_time = None
        self.chat_count = 0

        # Flags
        self.ollama_active = None
        self.docker_active = None
        self.kokoro_active = None
        self.ram_found = None
        self.cpu_found = None
        self.gpu_found = None
        self.sidebar_open = False
        self.is_new_conversation = True
        self.still_streaming = False
        self.is_speaking = False
        self.new_chat = True

        # Sound
        self.source_options = ["Default"]
        self.speakers_frame = None
        self.engine = pyttsx3.init()
        self.sink_list = None

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
        self.kokoro_active_voice = settings.get("kokoro_active_voice", "af_heart")
        self.default_active_voice = settings.get("default_active_voice", "")
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
        self.github_check = settings.get("github_check", False)
        self.language = settings.get("language", "English")
        self.ollama_chat_path = settings.get("ollama_chat_path", "http://localhost:11434/")
        self.ollama_context_path = settings.get("ollama_context_path", "http://localhost:11434/")
        self.ollama_title_path = settings.get("ollama_title_path", "http://localhost:11434/")
        self.enable_context = settings.get("enable_context", True)
        self.generate_titles = settings.get("generate_titles", True)
        self.title_gen_model = settings.get("title_gen_model", "llama3.2:3b")

def apply_theme(name: str) -> None:
    """Loads the user's chosen theme and applies it to ctk widgets."""
    try:
        globals.theme_path = os.path.normpath(
            os.path.join(load_data_path(direct="config"),
                         f"themes/{globals.active_theme}.json"))
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
