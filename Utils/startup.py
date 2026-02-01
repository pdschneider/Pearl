# Utils/startup.py
import logging, threading, os, json, shutil
from logging.handlers import TimedRotatingFileHandler
import tkinter as tk
import customtkinter as ctk
from Connections.ollama import ollama_test, load_model, get_loaded_models
from Managers.sound_manager import kokoro_test
from Utils.hardware import get_hardware_stats
from Utils.load_settings import load_data_path, load_settings

def startup(globals):
    """
    Starts up the program with a progress bar.
    
            Parameters:
                    globals: Global variables
    """
    tasks_done = threading.Event()

    def setup_logging():
        """Sets up logging for both the log file as well as standard console output."""
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

        logging.info(f"File and console logging initialized.")

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
                logging.warning(f"Current type of value for aved_y: {type(data["saved_y"])}")
                data["saved_y"] = 0
                changed = True
                logging.info(f"Sanitizing incorrect type 'saved_y'")

            # Check to make sure logging level and theme are acceptable values
            accepted_logging_values = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            accepted_themes = ["cosmic_sky", "pastel_green", "blazing_red", "dark_cloud", "soft_light"]
            if data["logging_level"] not in accepted_logging_values:
                data["logging_level"] = "INFO"
                changed = True
                logging.info("Fixed nonconforming value for 'logging_level' key in settings.json")
            if data["active_theme"] not in accepted_themes:
                data["active_theme"] = "cosmic_sky"
                changed = True
                logging.info(f"Adding missing 'active_theme' key to settings.json")
            
            # Write to file
            if changed:
                with open(settings, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

        # Sanitiza on exceptions
        except json.JSONDecodeError as e:
            logging.error(f"Invalid json synatax {e}. Replacing corrupted file with default.")
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
            logging.error(f"Invalid json synatax: {e} | Replacing corrupted theme files with defaults.")
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

    def startup_tasks(globals, tasks_done):
        """Tests dependencies and sets flags."""
        setup_logging()
        setup_settings()
        setup_themes()
        try:
            ollama_success = ollama_test()
            if ollama_success:
                globals.ollama_active = True
                loaded_models = get_loaded_models()
                if globals.active_model not in loaded_models:
                    logging.debug(f"Attempting to load initial model....")
                    load_model(globals.active_model)  # Loads the active model before startup
            kokoro_success = kokoro_test()
            if kokoro_success:
                globals.kokoro_active = True
        except:
            logging.error(f"Initial Ollama/Kokoro setup failed.")

        # Query for hardware stats
        try:
            get_hardware_stats()
        except Exception as e:
            logging.warning(f"Hardware stats query failed due to: {e}")

        tasks_done.set()

    # Perform startup tasks
    thread = threading.Thread(target=startup_tasks, args=(globals, tasks_done), daemon=True)
    thread.start()

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
        globals.startup_root.destroy()
        globals.startup_root = None

    def check_if_done():
        """Periodically checks to see if loading is finished."""
        if tasks_done.is_set():
            close_startup_window()
        else:
            globals.startup_root.after(100, check_if_done)

    # Set up polling loop
    globals.startup_root.after(100, check_if_done)

    # Destroy loading screen
    try:
        globals.startup_root.mainloop()
    except tk.TclError:
        pass  #  Ignores callback errors
