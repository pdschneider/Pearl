# Utils/kokoro.py
import subprocess
import logging
import os
import shutil
import requests
import socket
from Utils.hardware import get_disk_space, get_ram_info
from Utils.toast import show_toast
from Utils.load_settings import load_data_path
from Connections.docker import docker_check


# Kokoro
def kokoro_test(globals):
    """Tests Kokoro to set flag for active/inactive."""
    print_success = True if not globals.kokoro_active else False
    print_failure = True if globals.kokoro_active else False
    # Set Kokoro flag to true upon success
    try:
        socket.create_connection(("localhost", 8880), timeout=2).close()
        if print_success:
            logging.info(f"Kokokro found!")
        globals.kokoro_active = True
        return True
    # Set Kokoro flag to false upon error
    except Exception as e:
        if print_failure:
            logging.error(
                f"Kokoro not installed. TTS features will be unavailable.")
        globals.kokoro_active = False
        return False


def fetch_tts_models(globals):
    """loads possible Kokoro models"""
    if globals.kokoro_active:
        try:
            logging.debug(f"Attempting to load Kokoro voice list...")
            voices = requests.get("http://localhost:8880/v1/audio/voices")
            if voices.status_code == 200:
                return voices.json()["voices"]
            else:
                logging.error(
                    f"Kokoro voices fetch failed. Status code: {voices.status_code}. Returning empty dictionary.")
                return {}
        except Exception as e:
            logging.error(
                f"Failed to load voices due to {e}. Returning empty dictionary.")
            return {}


def fetch_current_language_models(globals):
    """loads Kokoro models of the current language selection."""
    if globals.kokoro_active:
        try:
            english_voices = ["af_", "am_", "bf_", "bm_"]
            voice_list = fetch_tts_models(globals)
            remove_list = []

            # Make a list of off-language voices
            for voice in voice_list:
                if not any(voice.strip().startswith(lang) for lang in english_voices):
                    remove_list.append(voice)

            # Remove out of language voices
            for removal in remove_list:
                voice_list.remove(removal)

            # Remove prefixes
            ...

            return voice_list
        except Exception as e:
            logging.error(
                f"Failed to load voices due to {e}. Returning empty dictionary.")
            return {}


def install_kokoro(globals):
    """Installs Kokoro via the terminal."""
    test = docker_check(globals)

    # If Docker is not installed, exit
    if not test:
        logging.warning(f"Docker must be installed and running before downloading Kokoro.")
        show_toast(globals, message="Docker must be installed before downloading Kokoro", _type="error")
        return

    # Check disk space to ensure at least 8GB
    free_space = get_disk_space()['free_disk']
    logging.debug(f"Free disk space: {free_space}")
    if free_space < 8:
        logging.warning(f"Free disk space must be at least 8GB to install Kokoro.")
        show_toast(globals, message="Must have at least 8GB of free disk space to install Kokoro", _type="error")
        return

    # Check available RAM to ensure at least 7GB
    free_ram = get_ram_info()['avail_ram_gb']
    logging.debug(f"RAM: get_ram_info()['avail_ram_gb']")
    if free_ram < 7:
        logging.warning(f"Available RAM must be at least 7GB to install Kokoro.")
        show_toast(globals, message="Must have at least 7GB of available RAM to install Kokoro", _type="error")
        return

    # Get path for Kokoro install
    try:
        path = load_data_path("config")
        # Exit if spaces are present in path, would break command otherwise
        if " " in path:
            logging.warning(f"Path may not include spaces: {path}")
            show_toast(globals, message=f"Path may not include spaces: {path}", _type="error")
            return
        # Create path if it doesn't already exist
        elif not os.path.isdir(path):
            logging.warning(f"Path not found, creating: {path}")
            os.mkdir(path)
    except Exception as e:
        logging.error(f"Could not load configuration data path.")
        return

    # Install Docker on Linux
    if globals.os_name.startswith("Linux"):
        cmd = """
            echo "Press Enter to Install Kokoro..."
            read -r dummy

            # Clone the repository
            cd FULL_PATH
            git clone https://github.com/remsky/Kokoro-FastAPI.git
            cd Kokoro-FastAPI
            cd docker/cpu

            # Start with CPU
            docker compose build
            docker compose up -d --build --force-recreate --remove-orphans
            docker compose ps -q | xargs -r docker update --restart=unless-stopped
            """
        cmd = cmd.replace("FULL_PATH", path)
        try:
            subprocess.Popen([
                "gnome-terminal",
                "--",
                "bash", "-i", "-c",
                f"{cmd}"
            ])
        except Exception as e:
            logging.error(f"Could not install Kokoro due to: {e}")

    # Warning for non-Linux users
    else:
        logging.warning(f"Only Linux is supported for Kokoro's interactive install.")


def uninstall_kokoro(globals):
    """Uninstalls Kokoro-FastAPI."""
    kokoro_installed = kokoro_test(globals)

    if not kokoro_installed:
        logging.warning(f"Kokoro not installed — no need to uninstall.")
        show_toast(globals, message="Kokoro not installed — no need to uninstall")
        return
    
    # Get Kokoro image and container ID's
    try:
        kokoro_container_id = subprocess.check_output("docker ps -a | grep kokoro",
                                        shell=True,
                                        timeout=4).decode('utf-8').strip().split()[0]
        kokoro_image_id = subprocess.check_output("docker images -a | grep kokoro",
                                        shell=True,
                                        timeout=4).decode('utf-8').strip().split()[1]
        logging.debug(f"Kokoro ID's: Container: {kokoro_container_id} | Image: {kokoro_image_id}")
        if not kokoro_container_id or not kokoro_image_id:
            logging.warning(f"Could not find one or more Kokoro ID's.")
            return
    except Exception as e:
        logging.error(f"Could not find Kokoro ID's due to: {e}")
        return

    if globals.os_name.startswith("Linux"):
        cmd = (
            """
            echo "Press Enter to uninstall Kokoro..."
            read -r dummy
            echo "Uninstalling Kokoro..."
            echo ""
            echo "Stopping current Kokoro container."
            docker stop KOKORO_CONTAINER_ID
            echo ""
            echo "Removing Kokoro container."
            echo ""
            docker rm KOKORO_CONTAINER_ID
            echo "Removing Kokoro image."
            docker rmi KOKORO_IMAGE_ID
            
            echo ""
            echo "Kokoro has been uninstalled!"
            read -r dummy
            exit 0
            """)
        cmd = cmd.replace("KOKORO_CONTAINER_ID", kokoro_container_id).replace("KOKORO_IMAGE_ID", kokoro_image_id)
        subprocess.Popen([
            "gnome-terminal",
            "--",
            "bash", "-c",
            f"{cmd}"
        ])
    elif globals.os_name.startswith("Windows"):
        logging.debug(f"Kokoro uninstall coming to Windows soon!")
        show_toast(globals, message="Kokoro uninstall coming to Windows soon!")
    else:
        logging.warning(f"Uninstall only supported on Linux and Windows.")
        show_toast(globals, message="Uninstall only supported on Linux and Windows.", _type="error")

    # Remove Kokoro from configuration
    try:
        path = load_data_path("config", "Kokoro-FastAPI")
        # Do not delete folder if path not found
        if not os.path.isdir(path):
            logging.info(f"Kokoro path not found.")
        # Delete folder if path found
        else:
            # Remove folder
            logging.debug(f"Removing Kokoro-FastAPI folder...")
            shutil.rmtree(path)
            # Veryfy that folder was removed
            path = load_data_path("config", "Kokoro-FastAPI")
            if os.path.isdir(path):
                logging.error(f"Unable to remove path.")
            else:
                logging.info(f"Successfully removed Kokoro-FastAPI folder!")
                show_toast(globals, message="Successfully removed Kokoro-FastAPI folder!")
    except Exception as e:
        logging.error(f"Could not load Kokoro-FastAPI directory path due to: {e}")
