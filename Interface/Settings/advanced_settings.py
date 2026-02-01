# Interface/Settings/advanced_settings.py
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from Utils.save_settings import save_all_settings
import Utils.fonts as fonts
from CTkToolTip import CTkToolTip
from Utils.save_settings import load_data_path
import subprocess, os, logging

def create_advanced_tab(globals, advanced_frame):
    """
    Creates the advanced tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    about_frame: The main frame of the about tab
    """

    # Get Icons
    globals.preferences_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/preferences.png")),
    dark_image=Image.open(load_data_path("config", "assets/preferences.png")),
    size=(40, 40))

    globals.note_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/note.png")),
    dark_image=Image.open(load_data_path("config", "assets/note.png")),
    size=(40, 40))

    ctk.CTkLabel(advanced_frame, 
             text="Advanced Settings", 
             font=fonts.title_font,
             anchor="center").pack(fill="x", pady=20, padx=10)

    # Options Frame
    options_frame = ctk.CTkFrame(advanced_frame, bg_color="transparent", fg_color="transparent")
    options_frame.pack(anchor="w", pady=5)

    ctk.CTkLabel(options_frame, text=None, image=globals.preferences_icon).grid(row=0, column=0, padx=6, sticky="w")

    logging_label = ctk.CTkLabel(options_frame, 
             text="Logging Level", font=fonts.heading_font)
    logging_label.grid(row=0, column=1, padx=5, sticky="w")
    CTkToolTip(logging_label, message="Sets Logging Level\nDebug: Very Verbose\nInfo: General Info & Failures\nWarning: Warnings/Errors/Failures\nError: Errors/System Failures\nCritical: Only System Failures", delay=0.6, follow=True, padx=10, pady=5)

    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    col = 2
    for level in levels:
        ctk.CTkRadioButton(options_frame, 
                       text=level, 
                       value=level, 
                       variable=globals.logging_var).grid(row=0, column=col, padx=0, sticky="w")
        col += 1

    # Logs Frame
    logs_frame = ctk.CTkFrame(advanced_frame, bg_color="transparent", fg_color="transparent")
    logs_frame.pack(anchor="w", pady=5)

    def open_logs():
        """Opens the logs folder."""
        if globals.os_name.startswith("Windows"):
            logging.debug(f"Opening logs folder on Windows...")
            os.startfile(load_data_path("cache", "logs"))
        else:
            logging.debug(f"Opening logs folder on Linux...")
            subprocess.run(['xdg-open', load_data_path("cache", "logs")], check=True)

    ctk.CTkLabel(logs_frame, text=None, image=globals.note_icon).pack(side="left", padx=6, pady=0)

    ctk.CTkLabel(logs_frame, 
                text="Open Logs",
                font=fonts.heading_font).pack(side="left", padx=(0, 12))

    logs_button = ctk.CTkButton(logs_frame, 
                                    text="Logs", 
                                    width=20,
                                    command=lambda: open_logs())
    logs_button.pack(side="left", padx=(0, 12))

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(advanced_frame, bg_color="transparent", fg_color="transparent")
    save_button_frame.pack(pady=10)

    ctk.CTkButton(save_button_frame, 
               text="Save Settings", 
               command=lambda: save_all_settings(globals)).pack()
