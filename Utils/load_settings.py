# Utils/load_settings.py
import os
import logging
import shutil
import json
import platform
import sys

def load_data_path(direct=None, filename=None, default=False):
    """
    Get the path to a writable data folder or a specific file,
    copying bundled files if needed.

    Parameters:
        direct = The file type to specify its directory,
        either configuration, persistent user data, or logs
        filename = The file name being accessed
    """
    os_name = platform.platform()
    default_files = ["settings.json",
                     "context.json",
                     "prompts.json",
                     "ollama_install.sh",
                     "docker_debian.sh",
                     "docker_ubuntu.sh",
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
                     "assets/docker.png",
                     "assets/fastapi.png",
                     "assets/en-language.png",
                     "assets/es-language.png",
                     "assets/fr-language.png",
                     "assets/ru-language.png",
                     "assets/no-sound.png",
                     "assets/column-chart.png",
                     "themes/cosmic_sky.json",
                     "themes/pastel_green.json",
                     "themes/blazing_red.json",
                     "themes/dark_cloud.json",
                     "themes/soft_light.json"]

    # Get base dir from __file__
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dev_base_dir = os.path.dirname(base_dir)

    # Running in development
    if os.path.exists(os.path.join(dev_base_dir, 'pearl.py')):
        data_dir = os.path.normpath(os.path.join(dev_base_dir, "data"))
        bundled_dir = os.path.normpath(os.path.join(dev_base_dir, "defaults"))

        # Checks if any file has themes/ or assets/ path
        try:
            os.makedirs(data_dir, exist_ok=True)
            if any("themes/" in f for f in default_files):
                themes_dir = os.path.join(data_dir, "themes")
                os.makedirs(themes_dir, exist_ok=True)
            if any("assets/" in f for f in default_files):
                assets_dir = os.path.join(data_dir, "assets")
                os.makedirs(assets_dir, exist_ok=True)
            if not os.access(data_dir, os.W_OK):
                raise PermissionError(f"No write permission for {data_dir}")
        except Exception as e:
            logging.error(f"Error creating data directory: {e}")
            raise

    # Running as bundled executable
    else:
        # Determine bundle root
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # PyInstaller
            bundle_root = sys._MEIPASS
        else:
            # Nuitka or other - assume similar to dev, go up from base_dir
            bundle_root = os.path.dirname(base_dir)  # Adjust this if deeper nesting (e.g., add another dirname)

            # Safety check: climb up until we find a likely root (e.g., where 'defaults' might be)
            max_climb = 5  # Prevent infinite loop
            climb_count = 0
            while not os.path.exists(os.path.join(bundle_root, "defaults")) and climb_count < max_climb:
                bundle_root = os.path.dirname(bundle_root)
                climb_count += 1
            if climb_count == max_climb:
                logging.warning("Could not find bundle root automatically - defaults may not copy.")

        bundled_dir = os.path.normpath(os.path.join(bundle_root, "defaults"))

        # Set persistent_dir based on direct
        if direct == "config":
            if os_name.startswith("Windows"):
                persistent_dir = os.path.normpath(os.path.join(os.getenv("APPDATA"), "Pearl"))
            else:
                persistent_dir = os.path.normpath(os.path.expanduser("~/.config/Pearl"))
                if not os_name.startswith("Linux"):
                    logging.warning("OS not found. Defaulting to Linux paths.")
        elif direct == "local":
            if os_name.startswith("Windows"):
                persistent_dir = os.path.normpath(os.path.join(os.getenv("LOCALAPPDATA"), "Pearl"))
            else:
                persistent_dir = os.path.normpath(os.path.expanduser("~/.local/share/Pearl"))
                if not os_name.startswith("Linux"):
                    logging.warning("OS not found. Defaulting to Linux paths.")
            default_files = []  # No defaults for local?
        else:  # cache
            if os_name.startswith("Windows"):
                persistent_dir = os.path.normpath(os.path.join(os.getenv("LOCALAPPDATA"), "Pearl", "Cache"))
            else:
                persistent_dir = os.path.normpath(os.path.expanduser("~/.cache/Pearl"))
                if not os_name.startswith("Linux"):
                    logging.warning("OS not found. Defaulting to Linux paths.")
            default_files = []  # No defaults for cache?

        # Create persistent dir and subdirs
        try:
            os.makedirs(persistent_dir, exist_ok=True)
            if any("themes/" in f for f in default_files):
                themes_dir = os.path.join(persistent_dir, "themes")
                os.makedirs(themes_dir, exist_ok=True)
            if any("assets/" in f for f in default_files):
                assets_dir = os.path.join(persistent_dir, "assets")
                os.makedirs(assets_dir, exist_ok=True)
            if not os.access(persistent_dir, os.W_OK):
                raise PermissionError(f"No write permission for {persistent_dir}")
        except Exception as e:
            logging.error(f"Error creating persistent data directory: {e}")
            raise

        data_dir = persistent_dir

    # Copy defaults (common to both dev and bundled)
    for default_file in default_files:
        bundled_file = os.path.normpath(os.path.join(bundled_dir, default_file))
        persistent_file = os.path.normpath(os.path.join(data_dir, default_file))
        if os.path.exists(bundled_file) and not os.path.exists(persistent_file):
            try:
                os.makedirs(os.path.dirname(persistent_file), exist_ok=True)  # Ensure subdirs like assets/themes
                logging.info(f"Copying {default_file} from {bundled_file} to {persistent_file}")
                shutil.copy(bundled_file, persistent_file)
            except Exception as e:
                logging.error(f"Error copying {default_file}: {e}")

    if not default:
        return os.path.normpath(os.path.join(data_dir, filename)) if filename else data_dir
    else:
        return os.path.normpath(os.path.join(bundled_dir, filename)) if filename else bundled_dir


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


def load_ollama_sh():
    """Loads the Ollama install bash script for Linux users."""
    try:
        with open(load_data_path("config", "ollama_install.sh")) as f:
            logging.debug(f"Successfully loaded Ollama Linux install file.")
            return f.read()
    except:
        return ""


def load_docker_debian():
    """Loads the Docker install bash script for Debian users."""
    try:
        with open(load_data_path("config", "docker_debian.sh")) as f:
            logging.debug(f"Successfully loaded Docker Debian install file.")
            return f.read()
    except:
        return ""


def load_docker_ubuntu():
    """Loads the Docker install bash script for Ubuntu users."""
    try:
        with open(load_data_path("config", "docker_ubuntu.sh")) as f:
            logging.debug(f"Successfully loaded Docker Ubuntu install file.")
            return f.read()
    except:
        return ""
