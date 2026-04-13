# Utils/docker.py
import subprocess
import logging
from PySide6.QtWidgets import QMessageBox
from tkinter import messagebox
from src.utils.hardware import get_disk_space, get_ram_info, get_os_info
from src.utils.toast import show_toast


def docker_version_check(globals):
    """Tests only dockers version."""
    try:
            # Set if Docker version has already been displayed
            print_version = True if not globals.docker_version else False

            # Run docker --version in terminal
            version_test = subprocess.run("docker --version",
                                          shell=True,
                                          capture_output=True,
                                          timeout=2)
            if version_test.returncode == 0:
                globals.docker_version = version_test.stdout.decode('utf-8').strip().replace(',', '').split()[2]
                if print_version:
                    logging.info(f"Docker Version: {globals.docker_version}")
                return True
            else:
                logging.warning(
                     f"Docker not installed. Enhanced TTS is unavailable.")
                globals.docker_active = False
                return False

    # Gracefully return false on exceptions
    except Exception as e:
        logging.error(
            f"Ollama not installed or not active. Chat features unavailable. Error: {e}")
        globals.ollama_active = False
        
        return False

def docker_check(globals):
        """Tests to see if Docker is up and running"""
        try:
            # Set if Docker version has already been displayed
            print_success = True if not globals.docker_active else False

            # Simple version test to start
            version = docker_version_check(globals)
            if not version:
                return False

            # If Docker is installed
            basic_test = subprocess.run("docker ps",
                                        shell=True,
                                        capture_output=True,
                                        timeout=4)

            # Return true if return code is 0
            if basic_test.returncode == 0:
                if print_success:
                    logging.debug(f"'docker ps' command succeeded. Docker is up and running!")
                globals.docker_active = True
                return True

            # Warn user if return code is not 0
            else:
                logging.warning(
                     f"Docker is installed but not running. Enhanced TTS is unavailable.")
                globals.docker_active = False
                return False

        # Gracefully return false on exceptions
        except Exception as e:
            logging.error(
                f"Docker not installed or not active. Enhanced TTS is unavailable. Error: {e}")
            globals.docker_active = False
            return False


def docker_installation(globals):
    """Installs Docker via the terminal."""
    # Do an initial check to see if Docker is already installed.
    docker_check(globals)

    # Gracefully exit if Docker is already installed
    if globals.docker_active:
        logging.warning(f"Docker is already active and running. No need to install.")
        if globals.qt_mode:
            QMessageBox.warning(
                        None,
                        "Docker Already Installed",
                        f"Docker is already active and running. No need to install!",
                        QMessageBox.StandardButton.Ok,
                        QMessageBox.StandardButton.Ok)
            return
        else:
            messagebox.showwarning(
                parent=globals.root,
                title="Docker Already Installed!",
                message=f"Docker is already active and running. No need to install!")
            return

    # Check disk space to ensure at least 1GB
    free_space = get_disk_space()['free_disk']
    if free_space < 1:
        logging.warning(f"Free disk space must be at least 1GB to install Docker.")
        show_toast(globals, message="Must have 1GB of free disk space to install Docker", _type="error")
        return

    # Check available RAM to ensure at least 1GB
    free_ram = get_ram_info()['avail_ram_gb']
    if free_ram < 1:
        logging.warning(f"Available RAM must be at least 1GB to install Docker.")
        show_toast(globals, message="Must have 1GB of available RAM to install Docker", _type="error")
        return

    try:
        # Install Docker on Linux
        if globals.os_name.startswith("Linux"):
            is_ubuntu = get_os_info()["UBUNTU_CODENAME"]
            logging.debug(f"Ubuntu? : {is_ubuntu}")
            if not is_ubuntu:
                subprocess.Popen([
                    "gnome-terminal",
                    "--",
                    "bash", "-i", "-c",
                    f"{globals.docker_debian}"
                ])
            else:
                subprocess.Popen([
                    "gnome-terminal",
                    "--",
                    "bash", "-i", "-c",
                    f"{globals.docker_ubuntu}"
                ])

        # Install Docker on Windows
        elif globals.os_name.startswith("Windows"):
            cmd_line = (
                'start "" powershell.exe '
                '-NoProfile '
                '-ExecutionPolicy Bypass '
                f'-File "{globals.docker_windows}"')
            
            subprocess.Popen(cmd_line, shell=True)

        # Warning for MAC users
        else:
            logging.warning(f"Only Linux and Windows are supported for Docker interactive install.")
            if globals.qt_mode:
                QMessageBox.warning(
                            None,
                            "OS Not Supported",
                            f"Only Linux and Windows are supported for interactive install of Docker. Use the web installer instead.",
                            QMessageBox.StandardButton.Ok,
                            QMessageBox.StandardButton.Ok)
            else:
                messagebox.showwarning(
                    parent=globals.root,
                    title="OS Not Supported",
                    message=f"Only Linux is supported for interactive install of Docker. Use the web installer instead.")

    except Exception as e:
        logging.error(f"Unable to install Docker due to: {e}")

    # Test again to see if it worked
    test = docker_check(globals)
    if test:
        logging.info(f"Docker was successfully installed!")


def uninstall_docker(globals):
    """Uninstall Docker."""
    # Test if Docker is actually installed
    docker_installed = docker_check(globals)
    print(f"Docker Installed? {docker_installed}")

    # If Docker is not installed, skip
    if not docker_installed:
        logging.warning(f"Docker not installed — no need to uninstall.")
        show_toast(globals, message="Docker not installed — no need to uninstall")
        return

    if globals.os_name.startswith("Linux"):
        uninstall_cmd = (
            """
            echo "Uninstalling Docker..."
            sudo apt purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras

            sudo rm -rf /var/lib/docker
            sudo rm -rf /var/lib/containerd

            sudo rm /etc/apt/sources.list.d/docker.sources
            sudo rm /etc/apt/keyrings/docker.asc

            sudo rm /etc/apt/sources.list.d/docker.sources
            rm -f ~/.docker/config.json

            # Remove credential helpers
            sudo rm -f /usr/bin/docker-credential-* /usr/local/bin/docker-credential-*

            # Remove the docker group if no longer needed
            sudo groupdel docker 2>/dev/null || true

            echo "Uninstall complete. Log out and back in (or reboot) for full effect..."
            read -r dummy
            exit 0
            """)
        subprocess.Popen([
            "gnome-terminal",
            "--",
            "bash", "-c",
            f"{uninstall_cmd}"
        ])
    elif globals.os_name.startswith("Windows"):
        logging.debug(f"Opening Windows uninstall program window...")
        subprocess.run("start appwiz.cpl", shell=True)
    else:
        logging.warning(f"Uninstall only supported on Linux and Windows.")
        show_toast(globals, message="Uninstall only supported on Linux and Windows.", _type="error")
