# Connections/github.py
import requests
import logging
import webbrowser
import tkinter as tk
from tkinter import messagebox


def version_check(globals):
    """Checks to see which version is most recent."""
    repo = "pdschneider/Pearl"
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"Accept": "application/vnd.github+json"}

    try:
        # Query github for the version
        response = requests.get(url, headers=headers, timeout=10)

        # Gracefully exit if status code is not 200
        if response.status_code != 200:
            logging.warning(
                f"Unable to fetch latest version | Status Code: {response.status_code}")
            return

        # Parse just the version number from data
        data = response.json()
        globals.latest_version = data["tag_name"].replace('v', '')
        latest_version_url = data["html_url"]

        # print(f"{data}")  <-- Prints entire output

        # Gracefully exit if the latest version is still not found
        if not globals.latest_version:
            logging.warning(f"Latest version not found.")
            return

        # Check if this is the latest version
        if globals.current_version < globals.latest_version:
            logging.info(
                f"An update to Pearl is available! Latest Version: {globals.latest_version}")
            
            # Create a messagebox and prompt for download
            root = tk.Tk()
            root.withdraw()
            update = messagebox.askyesno(
                parent=root,
                title="Update Available",
                message="Would you like to download the latest version of Pearl?")
            if update:
                webbrowser.open(url=latest_version_url)
            root.destroy()

    except Exception as e:
        logging.error(f"An error occurred while checking for updates: {e}")
