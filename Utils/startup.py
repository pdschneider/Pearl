# Utils/startup.py
import logging
import threading
import os
import json
import shutil
import hashlib
import sys
from logging.handlers import TimedRotatingFileHandler
import tkinter as tk
import customtkinter as ctk
from Connections.ollama import ollama_test, load_model, get_loaded_models
from Utils.hardware import get_hardware_stats
from Utils.load_settings import load_data_path, load_settings
from Connections.docker import docker_check
from Managers.sound_manager import kokoro_test
from Connections.github import version_check


def startup(globals):
    """
    Starts up the program with a progress bar.

            Parameters:
                    globals: Global variables
    """
    tasks_done = threading.Event()

    def setup_logging():
        """Sets up logging for both the log file 
        as well as standard console output."""
        logging.getLogger().handlers.clear()  # Clears output destinations
        logging.basicConfig(level=logging.INFO, format='%(message)s')

        # Silence dependencies
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger('PIL').setLevel(logging.WARNING)

        logs_dir = os.path.join(load_data_path(direct="cache"), "logs")  # Sets up logs folder
        os.makedirs(logs_dir, exist_ok=True)  # Creates the logs folder if it doesn't exist

        # Sets up logging to files
        logfile_handler = TimedRotatingFileHandler(os.path.join(logs_dir, "pearl.log"), when="midnight", backupCount=50)
        logfile_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logging.getLogger().addHandler(logfile_handler)

        # Loads correct logging level from settings
        try:
            settings = load_settings()
            logging.root.setLevel(getattr(logging, settings.get("logging_level", "INFO")))
        except:
            logging.warning(f"logging level variable in settings file is unconforming. Sanitizing...")
            setup_settings()
            settings = load_settings()
            logging.root.setLevel(getattr(logging, settings.get("logging_level", "INFO")))

        logging.debug(f"File and console logging initialized successfully.")

    def setup_settings():
        try:
            settings = load_data_path("config", "settings.json")
            with open(settings, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logging.debug(f"Settings loaded successfully from {settings}!")

            changed = False

            # Check to make sure keys are present
            if "active_model" not in data:
                data["active_model"] = "llama3.2:latest"
                changed = True
                logging.info(f"Added missing 'active_model' key to settings.json")
            if "active_voice" not in data:
                data["active_voice"] = "af_heart"
                changed = True
                logging.info(f"Added missing 'active_voice' key to settings.json")
            if "tts_enabled" not in data:
                data["tts_enabled"] = False
                changed = True
                logging.info(f"Added missing 'tts_enabled' key to settings.json")
            if "tts_source" not in data:
                data["tts_source"] = "Default"
                changed = True
                logging.info(f"Added missing 'tts_source' key to settings.json")
            if "dynamic_mode" not in data:
                data["dynamic_mode"] = False
                changed = True
                logging.info(f"Added missing 'dynamic_mode' key to settings.json")
            if "logging_level" not in data:
                data["logging_level"] = "INFO"
                changed = True
                logging.info(f"Added missing 'logging_level' key to settings.json")
            if "active_theme" not in data:
                data["active_theme"] = "dark_cloud"
                changed = True
                logging.info(f"Added missing 'active_theme' key to settings.json")
            if "save_chats" not in data:
                data["save_chats"] = False
                changed = True
                logging.info(f"Added missing 'save_chats' key to settings.json")
            if "default_sink" not in data:
                data["default_sink"] = "Default"
                changed = True
                logging.info(f"Added missing 'default_sink' key to settings.json")
            if "context_model" not in data:
                data["context_model"] = "llama3.2:latest"
                changed = True
                logging.info(f"Added missing 'context_model' key to settings.json")
            if "saved_width" not in data:
                data["saved_width"] = 0
                changed = True
                logging.info(f"Added missing 'saved_width' key to settings.json")
            if "saved_height" not in data:
                data["saved_height"] = 0
                changed = True
                logging.info(f"Added missing 'saved_height' key to settings.json")
            if "saved_x" not in data:
                data["saved_x"] = 0
                changed = True
                logging.info(f"Added missing 'saved_x' key to settings.json")
            if "saved_y" not in data:
                data["saved_y"] = 0
                changed = True
                logging.info(f"Added missing 'saved_y' key to settings.json")
            if "github_check" not in data:
                data["github_check"] = False
                changed = True
                logging.info(f"Added missing key 'github_check' to settings.json")
            if "language" not in data:
                data["language"] = "English"
                changed = True
                logging.info(f"Added missing key 'language' to settings.json")

            # Check to make sure values are the correct type
            if not isinstance(data["active_model"], str):
                logging.warning(f"Current type of value for active_model: {type(data["active_model"])}")
                data["active_model"] = "llama3.2:latest"
                changed = True
                logging.info(f"Sanitizing incorrect type 'active_model'")
            if not isinstance(data["active_voice"], str):
                logging.warning(f"Current type of value for active_voice: {type(data["active_voice"])}")
                data["active_voice"] = "af_heart"
                changed = True
                logging.info(f"Sanitizing incorrect type 'active_voice'")
            if not isinstance(data["tts_enabled"], bool):
                logging.warning(f"Current type of value for tts_enabled: {type(data["tts_enabled"])}")
                data["tts_enabled"] = False
                changed = True
                logging.info(f"Sanitizing incorrect type 'tts_enabled'")
            if not isinstance(data["tts_source"], str):
                logging.warning(f"Current type of value for tts_source: {type(data["tts_source"])}")
                data["tts_source"] = "Default"
                changed = True
                logging.info(f"Sanitizing incorrect type 'tts_source'")
            if not isinstance(data["dynamic_mode"], bool):
                logging.warning(f"Current type of value for dynamic_mode: {type(data["dynamic_mode"])}")
                data["dynamic_mode"] = False
                changed = True
                logging.info(f"Sanitizing incorrect type 'dynamic_mode'")
            if not isinstance(data["logging_level"], str):
                logging.warning(f"Current type of value for logging_level: {type(data["logging_level"])}")
                data["logging_level"] = "INFO"
                changed = True
                logging.info(f"Sanitizing incorrect type 'logging_level'")
            if not isinstance(data["active_theme"], str):
                logging.warning(f"Current type of value for active_theme: {type(data["active_theme"])}")
                data["active_theme"] = "dark_cloud"
                changed = True
                logging.info(f"Sanitizing incorrect type 'active_theme'")
            if not isinstance(data["save_chats"], bool):
                logging.warning(f"Current type of value for save_chats: {type(data["save_chats"])}")
                data["save_chats"] = False
                changed = True
                logging.info(f"Sanitizing incorrect type 'save_chats'")
            if not isinstance(data["default_sink"], str):
                logging.warning(f"Current type of value for default_sink: {type(data["default_sink"])}")
                data["default_sink"] = "Default"
                changed = True
                logging.info(f"Sanitizing incorrect type 'default_sink'")
            if not isinstance(data["context_model"], str):
                logging.warning(f"Current type of value for context_model: {type(data["context_model"])}")
                data["context_model"] = "llama3.2:latest"
                changed = True
                logging.info(f"Sanitizing incorrect type 'context_model'")
            if not isinstance(data["saved_width"], int):
                logging.warning(f"Current type of value for saved_width: {type(data["saved_width"])}")
                data["saved_width"] = 0
                changed = True
                logging.info(f"Sanitizing incorrect type 'saved_width'")
            if not isinstance(data["saved_height"], int):
                logging.warning(f"Current type of value for saved_height: {type(data["saved_height"])}")
                data["saved_height"] = 0
                changed = True
                logging.info(f"Sanitizing incorrect type 'saved_height'")
            if not isinstance(data["saved_x"], int):
                logging.warning(f"Current type of value for saved_x: {type(data["saved_x"])}")
                data["saved_x"] = 0
                changed = True
                logging.info(f"Sanitizing incorrect type 'saved_x'")
            if not isinstance(data["saved_y"], int):
                logging.warning(f"Current type of value for saved_y: {type(data["saved_y"])}")
                data["saved_y"] = 0
                changed = True
                logging.info(f"Sanitizing incorrect type 'saved_y'")
            if not isinstance(data["github_check"], bool):
                logging.warning(f"Current value type for 'github_check': {type(data["github_check"])}")
                data["github_check"] = False
                changed = True
                logging.info(f"Sanitizing incorrect type 'github_check'")
            if not isinstance(data["language"], str):
                logging.warning(f"Current value type for 'language': {type(data["language"])}")
                data["language"] = "English"
                changed = True
                logging.info(f"Sanitizing incorrect type 'language'")

            # Check to make sure logging level and theme are acceptable values
            accepted_logging_values = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            accepted_themes = ["cosmic_sky", "pastel_green", "blazing_red", "dark_cloud", "soft_light"]
            accepted_languages = ["English", "Spanish", "French", "Russian"]
            if data["logging_level"] not in accepted_logging_values:
                data["logging_level"] = "INFO"
                changed = True
                logging.info("Fixed nonconforming value for 'logging_level' key in settings.json")
            if data["active_theme"] not in accepted_themes:
                data["active_theme"] = "cosmic_sky"
                changed = True
                logging.info(f"Fixed nonconforming 'active_theme' key to settings.json")
            if data["language"] not in accepted_languages:
                data["language"] = "English"
                changed = True
                logging.info(f"Fixed nonconforming 'language' key to settings.json")
            
            # Write to file
            if changed:
                with open(settings, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

        # Sanitize on exceptions
        except json.JSONDecodeError as e:
            logging.error(f"Invalid json syntax {e}. Replacing corrupted file with default.")
            os.remove(settings)
            load_data_path("config", "settings.json")
        except TypeError as e:
            logging.error(f"Invalid json structure: {e} | Replacing corrupted settings file with default.")
            os.remove(settings)
            load_data_path("config", "settings.json")
        except Exception as e:
            logging.error(f"Unable to load settings due to {e}")

    def setup_themes():
        try:
            themes = ["themes/cosmic_sky.json", 
                        "themes/pastel_green.json", 
                        "themes/blazing_red.json", 
                        "themes/dark_cloud.json", 
                        "themes/soft_light.json"]
            theme_directory = os.path.normpath(load_data_path("config", "themes"))
            logging.debug(f"Theme Directory: {theme_directory}")
            theme_keys = ["CTk", 
                        "CTkFont", 
                        "CTkFrame", 
                        "CTkLabel", 
                        "CTkButton", 
                        "CTkEntry", 
                        "CTkCheckBox", 
                        "CTkRadioButton", 
                        "CTkComboBox", 
                        "CTkTextbox", 
                        "CTkScrollbar", 
                        "CTkSegmentedButton", 
                        "CTkTabview", 
                        "DropdownMenu", 
                        "CTkScrollableFrame", 
                        "CTkToplevel",
                        "CTkSlider"]
            total_themes = []
            for theme in themes:
                current_theme = os.path.normpath(load_data_path("config", theme))
                with open(current_theme, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                total_themes.append(theme)
                for key in theme_keys:
                    if key not in data:
                        shutil.rmtree(theme_directory)
                        load_data_path("config", theme_directory)
                        logging.info(f"Theme missing {key}, loading default themes.")
                        return
            logging.debug(f"Successfully loaded themes: {total_themes}")
        except json.JSONDecodeError as e:
            logging.error(f"Invalid json syntax: {e} | Replacing corrupted theme files with defaults.")
            if os.path.isdir(theme_directory):
                logging.debug(f"Removing theme directory.")
                shutil.rmtree(theme_directory)
            logging.debug(f"Reloading theme directory from defaults.")
            theme_directory = os.path.normpath(load_data_path("config", "themes"))
        except TypeError as e:
            logging.error(f"Invalid json structure: {e} | Replacing corrupted theme files with defaults.")
            if os.path.isdir(theme_directory):
                logging.debug(f"Removing theme directory.")
                shutil.rmtree(theme_directory)
            logging.debug(f"Reloading theme directory from defaults.")
            theme_directory = os.path.normpath(load_data_path("config", "themes"))
        except FileNotFoundError as e:
            logging.error(f"Theme file not found due to: {e}.")
            if os.path.isdir(theme_directory):
                logging.debug(f"Removing theme directory.")
                shutil.rmtree(theme_directory)
            logging.debug(f"Reloading theme directory from defaults.")
            theme_directory = os.path.normpath(load_data_path("config", "themes"))
        except Exception as e:
            logging.error(f"Unable to load themes due to {e}")

    def ollama_install_check():
        """Checks if bundled ollama_install.sh is different from user's ollama_install.sh, change if so."""
        try:
            # Read the contents of the default path and hash it
            default_ollama_path = load_data_path("config", "ollama_install.sh", default=True)
            with open(default_ollama_path, 'r') as f:
                default_ollama_file = f.read()
            hashed_default_ollama_sh = hashlib.md5(default_ollama_file.encode()).hexdigest()
            if not hashed_default_ollama_sh:
                logging.warning(f"No hash for default ollama_install.sh found.")

            # Read the contents of the current user's path and hash it
            user_ollama_path = load_data_path("config", "ollama_install.sh")
            with open(user_ollama_path, 'r') as f:
                user_ollama_file = f.read()
            hashed_user_ollama_sh = hashlib.md5(user_ollama_file.encode()).hexdigest()
            if not hashed_user_ollama_sh:
                logging.warning(f"No has for user's ollama_install.sh found.")

        except Exception as e:
            logging.warning(f"Unable to hash ollama_install.sh due to: {e}")
            return

        # Compare hashes, remove and replace old file if different
        if hashed_default_ollama_sh != hashed_user_ollama_sh:
            try:
                if os.path.isfile(load_data_path("config", "ollama_install.sh")):
                    logging.debug(f"Removing old ollama_install.sh...")
                    os.remove(load_data_path("config", "ollama_install.sh"))
                logging.info(f"Updating ollama_install.sh...")
                load_data_path("config", "ollama_install.sh", default=True)

            except Exception as e:
                logging.warning(f"Unable to update company map due to: {e}")
        else:
            logging.debug(f"ollama_install.sh already at current version.")

    def docker_debian_check():
        """Checks if bundled docker_debian.sh is different from user's docker_debian.sh, change if so."""
        try:
            # Read the contents of the default path and hash it
            default_docker_debian_path = load_data_path("config", "docker_debian.sh", default=True)
            with open(default_docker_debian_path, 'r', encoding='utf-8') as f:
                default_docker_debian_file = f.read()
            hashed_default_docker_debian_sh = hashlib.md5(default_docker_debian_file.encode()).hexdigest()
            if not hashed_default_docker_debian_sh:
                logging.warning(f"No hash for default docker_debian.sh found.")

            # Read the contents of the current user's path and hash it
            user_docker_debian_path = load_data_path("config", "docker_debian.sh")
            with open(user_docker_debian_path, 'r', encoding='utf-8') as f:
                user_docker_debian_file = f.read()
            hashed_user_docker_debian_sh = hashlib.md5(user_docker_debian_file.encode()).hexdigest()
            if not hashed_user_docker_debian_sh:
                logging.warning(f"No has for user's docker_debian.sh found.")

        except Exception as e:
            logging.warning(f"Unable to hash docker_debian.sh due to: {e}")
            return

        # Compare hashes, remove and replace old file if different
        if hashed_default_docker_debian_sh != hashed_user_docker_debian_sh:
            try:
                if os.path.isfile(load_data_path("config", "docker_debian.sh")):
                    logging.debug(f"Hash mismatch. Removing old docker_debian.sh...")
                    os.remove(load_data_path("config", "docker_debian.sh"))
                logging.info(f"Updating docker_debian.sh...")
                load_data_path("config", "docker_debian.sh", default=True)

            except Exception as e:
                logging.warning(f"Unable to update docker_debian.sh due to: {e}")
        else:
            logging.debug(f"docker_debian.sh already at current version.")

    def docker_ubuntu_check():
        """Checks if bundled docker_ubuntu.sh is different from user's docker_ubuntu.sh, change if so."""
        try:
            # Read the contents of the default path and hash it
            default_docker_ubuntu_path = load_data_path("config", "docker_ubuntu.sh", default=True)
            with open(default_docker_ubuntu_path, 'r', encoding='utf-8') as f:
                default_docker_ubuntu_file = f.read()
            hashed_default_docker_ubuntu_sh = hashlib.md5(default_docker_ubuntu_file.encode()).hexdigest()
            if not hashed_default_docker_ubuntu_sh:
                logging.warning(f"No hash for default docker_ubuntu.sh found.")

            # Read the contents of the current user's path and hash it
            user_docker_ubuntu_path = load_data_path("config", "docker_ubuntu.sh")
            with open(user_docker_ubuntu_path, 'r', encoding='utf-8') as f:
                user_docker_ubuntu_file = f.read()
            hashed_user_docker_ubuntu_sh = hashlib.md5(user_docker_ubuntu_file.encode()).hexdigest()
            if not hashed_user_docker_ubuntu_sh:
                logging.warning(f"No has for user's docker_ubuntu.sh found.")

        except Exception as e:
            logging.warning(f"Unable to hash docker_ubuntu.sh due to: {e}")
            return

        # Compare hashes, remove and replace old file if different
        if hashed_default_docker_ubuntu_sh != hashed_user_docker_ubuntu_sh:
            try:
                if os.path.isfile(load_data_path("config", "docker_ubuntu.sh")):
                    logging.debug(f"Hash mismatch. Removing old docker_ubuntu.sh...")
                    os.remove(load_data_path("config", "docker_ubuntu.sh"))
                logging.info(f"Updating docker_ubuntu.sh...")
                load_data_path("config", "docker_ubuntu.sh", default=True)

            except Exception as e:
                logging.warning(f"Unable to update docker_ubuntu.sh due to: {e}")
        else:
            logging.debug(f"docker_ubuntu.sh already at current version.")

    def setup_context():
        """Makes sure the context file is usable."""
        try:
            context = load_data_path("config", "context.json")
            with open(context, 'r', encoding='utf-8') as f:
                data = json.load(f)

            changed = False

            if "Assistant" not in data or not isinstance(data["Assistant"], list):
                    data["Assistant"] = ["assist", "question", "info", "general", "assistant"]
                    changed = True
                    logging.info(f"Added missing or nonconforming 'Assistant' key to context.json")
            if "Therapist" not in data or not isinstance(data["Therapist"], list):
                    data["Therapist"] = ["feel", "emotion", "stress", "anxiety", "support", "sad", "happy", "kill", "kms"]
                    changed = True
                    logging.info(f"Added missing or nonconforming 'Therapist' key to context.json")
            if "Financial" not in data or not isinstance(data["Financial"], list):
                    data["Financial"] = ["budget", "money", "spend", "save", "invest", "debt", "finance", "finances"]
                    changed = True
                    logging.info(f"Added missing or nonconforming 'Financial' key to context.json")
            if "Storyteller" not in data or not isinstance(data["Storyteller"], list):
                    data["Storyteller"] = ["story", "tale", "adventure", "imagine", "narrative", "create", "fiction"]
                    changed = True
                    logging.info(f"Added missing or nonconforming 'Storyteller' key to context.json")
            if "Conspiracy" not in data or not isinstance(data["Conspiracy"], list):
                    data["Conspiracy"] = ["conspiracy", "truth", "hidden", "secret", "government", "plot", "theory", "bilderberg", "chemtrails"]
                    changed = True
                    logging.info(f"Added missing or nonconforming 'Conspiracy' key to context.json")
            if "Meditation" not in data or not isinstance(data["Meditation"], list):
                    data["Meditation"] = ["calm", "relax", "peace", "meditate", "breathe", "mindful", "zen", "mindfulness"]
                    changed = True
                    logging.info(f"Added missing or nonconforming 'Meditation' key to context.json")
            if "Motivation" not in data or not isinstance(data["Motivation"], list):
                    data["Motivation"] = ["motivate", "inspire", "encourage", "goal", "success", "push", "achieve", "motivation", "inspiration"]
                    changed = True
                    logging.info(f"Added missing or nonconforming 'Motivation' key to context.json")

            # Write to file
            if changed:
                with open(context, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

        # Sanitize on exceptions
        except json.JSONDecodeError as e:
            logging.error(f"Invalid json syntax {e}. Replacing corrupted file with default.")
            os.remove(context)
            load_data_path("config", "context.json")
        except TypeError as e:
            logging.error(f"Invalid json structure: {e} | Replacing corrupted settings file with default.")
            os.remove(context)
            load_data_path("config", "context.json")
        except Exception as e:
            logging.error(f"Unable to load context due to {e}")


    def startup_tasks(globals, tasks_done):
        """Tests dependencies and sets flags."""
        setup_logging()
        setup_settings()
        setup_themes()
        setup_context()
        ollama_install_check()
        docker_debian_check()
        docker_ubuntu_check()
        logging.info(f"Python Version: {sys.version}")
        logging.info(f"Pearl Version: {globals.current_version}")
        try:
            # Test for Ollama
            ollama_success = ollama_test(globals)
            if ollama_success:
                loaded_models = get_loaded_models(globals)
                if globals.active_model not in loaded_models:
                    logging.debug(f"Attempting to load initial model....")
                    # Loads the active model before GUI is built
                    load_model(globals, globals.active_model)
        except Exception as e:
            logging.error(f"Initial Ollama setup failed due to: {e}")

        # Test for Docker & Kokoro
        try:
            docker_success = docker_check(globals)
            if docker_success:
                kokoro_test(globals)
        except Exception as e:
            logging.error(f"Initial Docker + Kokoro setup failed due to {e}")

        # Query for hardware stats
        try:
            get_hardware_stats()
        except Exception as e:
            logging.warning(f"Hardware stats query failed due to: {e}")

        tasks_done.set()

    # Perform startup tasks
    thread = threading.Thread(target=startup_tasks, args=(globals, tasks_done), daemon=True)
    thread.start()

    # Check is version is most recent
    if globals.github_check:
        version_check(globals)

    # Wait up to 1 second for quick completion
    thread.join(1.0)
    if tasks_done.is_set():
        return

    # Create the loading window
    globals.startup_root = ctk.CTk()
    globals.startup_root.title("Loading Pearl...")
    globals.startup_root.geometry("300x100")

    # Create progress bar
    progress_bar = ctk.CTkProgressBar(globals.startup_root, mode="indeterminate")
    progress_bar.pack(padx=10, pady=10, fill="x")
    progress_bar.start()

    # Callback to destroy the window when tasks are done
    def close_startup_window():
        """Closes the progress bar window."""
        progress_bar.stop()
        if globals.startup_root:
            globals.startup_root.destroy()
        globals.startup_root = None

    def check_if_done():
        """Periodically checks to see if loading is finished."""
        if tasks_done.is_set():
            close_startup_window()
        else:
            if globals.startup_root:
                globals.startup_root.after(100, check_if_done)

    # Set up polling loop
    if globals.startup_root:
        globals.startup_root.after(100, check_if_done)

    # Destroy loading screen
    try:
        globals.startup_root.mainloop()
    except tk.TclError:
        pass #  Ignores callback errors
