# Utils/docker.py
import subprocess
import logging


def docker_check(globals):
        """Tests to see if Docker is up and running"""
        try:
            # Simple version test to start
            version_test = subprocess.run("docker --version",
                                          shell=True,
                                          capture_output=True,
                                          timeout=4)
            if version_test.returncode == 0:
                globals.docker_version = version_test.stdout.decode('utf-8').strip().replace(',', '').split()[2]
                logging.info(f"Docker Version: {globals.docker_version}")
            else:
                logging.warning(
                     f"Docker not installed. Enhanced TTS is unavailable.")
                return False

            # If Docker is installed, test if active
            basic_test = subprocess.run("docker ps",
                                        shell=True,
                                        capture_output=True,
                                        timeout=4)
            if basic_test.returncode == 0:
                logging.info(f"Docker is up and running!")
                return True
            else:
                logging.warning(
                     f"Docker is installed but not running. Enhanced TTS is unavailable.")
                return False
        # Gracefully return false on exceptions
        except Exception as e:
            logging.error(
                f"Docker not installed or not active. Enhanced TTS is unavailable. Error: {e}")
            return False
