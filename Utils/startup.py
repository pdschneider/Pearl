# Utils/startup.py
import logging
import threading
import os
import json
import hashlib
import sys
from logging.handlers import TimedRotatingFileHandler
import tkinter as tk
import customtkinter as ctk
from Connections.ollama import ollama_test, load_model, get_loaded_models
from Utils.hardware import get_hardware_stats
from Utils.load_settings import load_data_path, load_settings
from Connections.docker import docker_check
from Connections.kokoro import kokoro_test
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
        logging.getLogger('comtypes').setLevel(logging.WARNING)
        logging.getLogger('pyttsx3').setLevel(logging.WARNING)

        logs_dir = os.path.join(load_data_path(direct="cache"), "logs")  # Sets up logs folder
        os.makedirs(logs_dir, exist_ok=True)  # Creates the logs folder if it doesn't exist

        # Sets up logging to files
        logfile_handler = TimedRotatingFileHandler(os.path.join(logs_dir, "pearl.log"), when="midnight", backupCount=50)
        logfile_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logging.getLogger().addHandler(logfile_handler)

        # Captures general warnings to logs
        logging.captureWarnings(True)

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
        """Ensure the settings files is present and has conforming values."""
        try:
            settings = load_data_path("config", "settings.json")
            with open(settings, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logging.debug(f"Settings loaded successfully from {settings}!")

            changed = False

            # Accepted string values
            accepted_logging_values = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            accepted_themes = ["cosmic_sky", "pastel_green", "blazing_red", "dark_cloud", "soft_light"]
            accepted_languages = ["English", "Spanish", "French", "Russian"]

            # Check to make sure keys are present and the correct type
            if "active_model" not in data or not isinstance(data["active_model"], str):
                data["active_model"] = "llama3.2:latest"
                changed = True
                logging.info(f"Added missing or nonconforming 'active_model' key to settings.json")
            if "kokoro_active_voice" not in data or not isinstance(data["kokoro_active_voice"], str):
                data["kokoro_active_voice"] = "af_heart"
                changed = True
                logging.info(f"Added missing or nonconforming 'kokoro_active_voice' key to settings.json")
            if "default_active_voice" not in data or not isinstance(data["default_active_voice"], str):
                data["default_active_voice"] = ""
                changed = True
                logging.info(f"Added missing or nonconforming 'default_active_voice' key to settings.json")
            if "tts_enabled" not in data or not isinstance(data["tts_enabled"], bool):
                data["tts_enabled"] = False
                changed = True
                logging.info(f"Added missing or nonconforming 'tts_enabled' key to settings.json")
            if "tts_source" not in data or not isinstance(data["tts_source"], str):
                data["tts_source"] = "Default"
                changed = True
                logging.info(f"Added missing or nonconforming 'tts_source' key to settings.json")
            if "dynamic_mode" not in data or not isinstance(data["dynamic_mode"], bool):
                data["dynamic_mode"] = False
                changed = True
                logging.info(f"Added missing or nonconforming 'dynamic_mode' key to settings.json")
            if "logging_level" not in data or not isinstance(data["logging_level"], str) or data["logging_level"] not in accepted_logging_values:
                data["logging_level"] = "INFO"
                changed = True
                logging.info(f"Added missing or nonconforming 'logging_level' key to settings.json")
            if "active_theme" not in data or not isinstance(data["active_theme"], str) or data["active_theme"] not in accepted_themes:
                data["active_theme"] = "dark_cloud"
                changed = True
                logging.info(f"Added missing or nonconforming 'active_theme' key to settings.json")
            if "save_chats" not in data or not isinstance(data["save_chats"], bool):
                data["save_chats"] = False
                changed = True
                logging.info(f"Added missing or nonconforming 'save_chats' key to settings.json")
            if "default_sink" not in data or not isinstance(data["default_sink"], str):
                data["default_sink"] = "Default"
                changed = True
                logging.info(f"Added missing or nonconforming 'default_sink' key to settings.json")
            if "context_model" not in data or not isinstance(data["context_model"], str):
                data["context_model"] = "llama3.2:latest"
                changed = True
                logging.info(f"Added missing or nonconforming 'context_model' key to settings.json")
            if "saved_width" not in data or not isinstance(data["saved_width"], int):
                data["saved_width"] = 0
                changed = True
                logging.info(f"Added missing or nonconforming 'saved_width' key to settings.json")
            if "saved_height" not in data or not isinstance(data["saved_height"], int):
                data["saved_height"] = 0
                changed = True
                logging.info(f"Added missing or nonconforming 'saved_height' key to settings.json")
            if "saved_x" not in data or not isinstance(data["saved_x"], int):
                data["saved_x"] = 0
                changed = True
                logging.info(f"Added missing or nonconforming 'saved_x' key to settings.json")
            if "saved_y" not in data or not isinstance(data["saved_y"], int):
                data["saved_y"] = 0
                changed = True
                logging.info(f"Added missing or nonconforming 'saved_y' key to settings.json")
            if "github_check" not in data or not isinstance(data["github_check"], bool):
                data["github_check"] = False
                changed = True
                logging.info(f"Added missing or nonconforming 'github_check' key to settings.json")
            if "language" not in data or not isinstance(data["language"], str) or data["language"] not in accepted_languages:
                data["language"] = "English"
                changed = True
                logging.info(f"Added missing key 'language' to settings.json")

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
            logging.error(f"Unable to sanitize settings due to: {e}")

    def setup_themes():
        """Replaces theme files if they are different from the current version."""
        try:
            themes = ["themes/cosmic_sky.json",
                      "themes/pastel_green.json",
                      "themes/blazing_red.json",
                      "themes/dark_cloud.json",
                      "themes/soft_light.json"]
            theme_directory = os.path.normpath(load_data_path("config", "themes"))
            logging.debug(f"Theme Directory: {theme_directory}")

            for theme in themes:
                try:
                    # Read the contents of the default path and hash it
                    default_theme_path = load_data_path("config", theme, default=True)
                    with open(default_theme_path, 'r', encoding='utf-8') as f:
                        default_theme_file = f.read()
                    hashed_default_theme_file = hashlib.md5(default_theme_file.encode()).hexdigest()
                    if not hashed_default_theme_file:
                        logging.warning(f"No hash for default {theme} found.")

                    # Read the contents of the current user's path and hash it
                    user_theme_path = load_data_path("config", theme)
                    with open(user_theme_path, 'r', encoding='utf-8') as f:
                        user_theme_file = f.read()
                    hashed_user_theme_file = hashlib.md5(user_theme_file.encode()).hexdigest()
                    if not hashed_user_theme_file:
                        logging.warning(f"No has for user's {theme} found.")

                except Exception as e:
                    logging.warning(f"Unable to hash {theme} due to: {e}")
                    return

                # Compare hashes, remove and replace old file if different
                if hashed_default_theme_file != hashed_user_theme_file:
                    try:
                        if os.path.isfile(load_data_path("config", theme)):
                            logging.debug(f"Removing old {theme}...")
                            os.remove(load_data_path("config", theme))
                        logging.info(f"Updating {theme}...")
                        load_data_path("config", theme, default=True)

                    except Exception as e:
                        logging.warning(f"Unable to update {theme} to: {e}")
                        return

        except Exception as e:
            logging.error(f"Could not hash theme files due to: {e}")
            return

    def ollama_install_check():
        """Checks if bundled ollama_install.sh is different from user's ollama_install.sh, change if so."""
        try:
            # Read the contents of the default path and hash it
            default_ollama_path = load_data_path("config", "ollama_install.sh", default=True)
            with open(default_ollama_path, 'r', encoding='utf-8') as f:
                default_ollama_file = f.read()
            hashed_default_ollama_sh = hashlib.md5(default_ollama_file.encode()).hexdigest()
            if not hashed_default_ollama_sh:
                logging.warning(f"No hash for default ollama_install.sh found.")

            # Read the contents of the current user's path and hash it
            user_ollama_path = load_data_path("config", "ollama_install.sh")
            with open(user_ollama_path, 'r', encoding='utf-8') as f:
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
                logging.warning(f"Unable to update ollama_install.sh due to: {e}")

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

    def setup_context():
        """Makes sure the context file is updated and usable."""

        try:
            # Read the contents of the default path and hash it
            default_context_path = load_data_path("config", "context.json", default=True)
            with open(default_context_path, 'r', encoding='utf-8') as f:
                default_context_file = f.read()
            hashed_default_context_file = hashlib.md5(default_context_file.encode()).hexdigest()
            if not hashed_default_context_file:
                logging.warning(f"No hash for default context.json found.")

            # Read the contents of the current user's path and hash it
            user_context_path = load_data_path("config", "context.json")
            with open(user_context_path, 'r', encoding='utf-8') as f:
                user_context_file = f.read()
            hashed_user_context_file = hashlib.md5(user_context_file.encode()).hexdigest()
            if not hashed_user_context_file:
                logging.warning(f"No has for user's context.json found.")

        except Exception as e:
            logging.warning(f"Unable to hash context.json due to: {e}")
            return

        # Compare hashes, remove and replace old file if different
        if hashed_default_context_file != hashed_user_context_file:
            try:
                if os.path.isfile(load_data_path("config", "context.json")):
                    logging.debug(f"Hash mismatch. Removing old context.json...")
                    os.remove(load_data_path("config", "context.json"))
                logging.info(f"Updating dontext.json...")
                load_data_path("config", "context.json", default=True)

            except Exception as e:
                logging.warning(f"Unable to update context.json due to: {e}")

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

        logging.debug("Startup tasks completed!")
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
    screen_width = globals.startup_root.winfo_screenwidth()
    screen_height = globals.startup_root.winfo_screenheight()
    x = (screen_width - 900) // 2
    y = (screen_height - 850) // 2
    globals.startup_root.geometry(f"300x100+{x}+{y}")

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
