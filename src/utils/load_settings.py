# utils/load_settings.py
import os
import logging
import shutil
import json
import platform
import sys

def load_data_path(direct=None, filename=None, default=False):
    """
    Get the path to a writable data folder or a specific file,
    copying bundled default files if needed.
    """
    # ==================== DEFAULT FILES ====================
    default_files = ["settings.json",
                     "context.json",
                     "prompts.json",
                     "ollama_install.sh",
                     "docker_debian.sh",
                     "docker_ubuntu.sh",
                     "docker_install.ps1",
                     "kokoro_install.ps1",
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
                     "assets/operations.png",
                     "assets/tag.png",
                     "themes/cosmic_sky.json",
                     "themes/pastel_green.json",
                     "themes/blazing_red.json",
                     "themes/dark_cloud.json",
                     "themes/soft_light.json"]

    # ==================== DETECT RUN MODE ====================
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller
        is_bundled = True
        bundle_root = sys._MEIPASS

    elif "__compiled__" in globals():
        # Nuitka (onefile or standalone)
        is_bundled = True
        try:
            module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # src/utils/
            bundle_root = os.path.dirname(module_dir)                 # root (where defaults/ lives)
        except Exception:
            bundle_root = os.path.dirname(sys.executable)

    else:
        # === DEVELOPMENT MODE ===
        is_bundled = False
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # src/utils/
        dev_base_dir = os.path.dirname(base_dir)                # project root

    # ==================== SET bundled_dir and data_dir ====================
    if is_bundled:
        bundled_dir = os.path.normpath(os.path.join(bundle_root, "defaults"))

        # Persistent directory for user data
        if direct == "config":
            if platform.system() == "Windows":
                persistent_dir = os.path.normpath(os.path.join(os.getenv("APPDATA"), "Pearl"))
            else:
                persistent_dir = os.path.normpath(os.path.expanduser("~/.config/Pearl"))
        elif direct == "local":
            if platform.system() == "Windows":
                persistent_dir = os.path.normpath(os.path.join(os.getenv("LOCALAPPDATA"), "Pearl"))
            else:
                persistent_dir = os.path.normpath(os.path.expanduser("~/.local/share/Pearl"))
            default_files = []
        else:  # cache or main
            if platform.system() == "Windows":
                persistent_dir = os.path.normpath(
                    os.path.join(os.getenv("LOCALAPPDATA"), "Pearl", "Cache"))
            else:
                persistent_dir = os.path.normpath(os.path.expanduser("~/.cache/Pearl"))
            default_files = []

        data_dir = persistent_dir

        # Create persistent dir + subdirs
        try:
            os.makedirs(persistent_dir, exist_ok=True)
            if any(f.startswith("assets/") for f in default_files):
                os.makedirs(os.path.join(persistent_dir, "assets"), exist_ok=True)
            if any(f.startswith("themes/") for f in default_files):
                os.makedirs(os.path.join(persistent_dir, "themes"), exist_ok=True)
            if not os.access(persistent_dir, os.W_OK):
                raise PermissionError(f"No write permission for {persistent_dir}")
        except Exception as e:
            logging.error(f"Error creating persistent directory: {e}")
            raise

    else:
        # === DEVELOPMENT ===
        data_dir = os.path.normpath(os.path.join(dev_base_dir, "data"))
        bundled_dir = os.path.normpath(os.path.join(dev_base_dir, "defaults"))

        # Create dev data dir + subdirs
        try:
            os.makedirs(data_dir, exist_ok=True)
            if any(f.startswith("assets/") for f in default_files):
                os.makedirs(os.path.join(data_dir, "assets"), exist_ok=True)
            if any(f.startswith("themes/") for f in default_files):
                os.makedirs(os.path.join(data_dir, "themes"), exist_ok=True)
            if not os.access(data_dir, os.W_OK):
                raise PermissionError(f"No write permission for {data_dir}")
        except Exception as e:
            logging.error(f"Error creating data directory: {e}")
            raise

    # ==================== COPY DEFAULT FILES IF MISSING ====================
    for default_file in default_files:
        src = os.path.normpath(os.path.join(bundled_dir, default_file))
        dst = os.path.normpath(os.path.join(data_dir, default_file))
        if os.path.exists(src) and not os.path.exists(dst):
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                logging.info(f"Copied default file: {default_file}")
            except Exception as e:
                logging.error(f"Failed to copy {default_file}: {e}")

    # ==================== RETURN REQUESTED PATH ====================
    if default:
        return os.path.normpath(os.path.join(bundled_dir, filename)) if filename else bundled_dir
    else:
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


def load_ollama_sh():
    """Loads the Ollama install bash script for Linux users."""
    try:
        with open(load_data_path("config", "ollama_install.sh"), encoding="utf-8") as f:
            logging.debug(f"Successfully loaded Ollama Linux install file.")
            return f.read()
    except Exception as e:
        logging.warning(f"Unable to read Ollama install file for Linux due to: {e}")
        return ""


def load_docker_debian():
    """Loads the Docker install bash script for Debian users."""
    try:
        with open(load_data_path("config", "docker_debian.sh"), encoding="utf-8") as f:
            logging.debug(f"Successfully loaded Docker Debian install file.")
            return f.read()
    except Exception as e:
        logging.warning(f"Unable to read Docker install file for Debian due to: {e}")
        return ""


def load_docker_ubuntu():
    """Loads the Docker install bash script for Ubuntu users."""
    try:
        with open(load_data_path("config", "docker_ubuntu.sh"), encoding="utf-8") as f:
            logging.debug(f"Successfully loaded Docker Ubuntu install file.")
            return f.read()
    except Exception as e:
        logging.warning(f"Unable to read Docker install file for Ubuntu due to: {e}")
        return ""


def load_docker_windows():
    """Loads the Docker install PowerShell script for Windows users."""
    try:
        path = load_data_path("config", "docker_install.ps1")
        return path
    except Exception as e:
        logging.warning(f"Unable to load Docker install path for Windows due to: {e}")
        return ""


def load_kokoro_windows():
    """Loads the Kokoro install PowerShell script for Windows users."""
    try:
        path = load_data_path("config", "kokoro_install.ps1")
        return path
    except Exception as e:
        logging.warning(f"Unable to load Kokoro install path for Windows due to: {e}")
        return ""
