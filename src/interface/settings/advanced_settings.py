# Interface/Settings/advanced_settings.py
import customtkinter as ctk
from src.utils.save_settings import save_all_settings
import src.utils.fonts as fonts
from CTkToolTip import CTkToolTip
from tkinter import messagebox
from PySide6.QtWidgets import QMessageBox
from src.utils.save_settings import load_data_path
from src.connections.ollama import uninstall_ollama
from src.connections.docker import uninstall_docker
from src.connections.kokoro import uninstall_kokoro
from src.utils.factory_reset import total_factory_reset
import subprocess
import os
import logging
import sys


def create_advanced_tab(globals, advanced_frame):
    """
    Creates the advanced tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    advanced_frame: The main frame of the advanced tab
    """

    ctk.CTkLabel(advanced_frame,
                 text="Advanced",
                 font=fonts.title_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)

    # Options Frame
    options_frame = ctk.CTkFrame(advanced_frame,
                                 bg_color="transparent",
                                 fg_color="transparent")
    options_frame.pack(anchor="w", pady=5)

    ctk.CTkLabel(options_frame,
                 text=None,
                 image=globals.preferences_icon).grid(
                     row=0, column=0, padx=6, sticky="w")

    logging_label = ctk.CTkLabel(options_frame,
                                 text="Logging Level", font=fonts.heading_font)
    logging_label.grid(row=0, column=1, padx=5, sticky="w")

    CTkToolTip(logging_label,
               message="Sets Logging Level\nDebug: Very Verbose\nInfo: General Info & Failures\nWarning: Warnings/Errors/Failures\nError: Errors/System Failures\nCritical: Only System Failures",
               delay=0.6,
               follow=True,
               padx=10,
               pady=5)

    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    col = 2
    for level in levels:
        ctk.CTkRadioButton(options_frame,
                           text=level,
                           value=level,
                           variable=globals.logging_var).grid(
                               row=0, column=col, padx=0, sticky="w")
        col += 1

    # Folders Frame
    folders_frame = ctk.CTkFrame(advanced_frame,
                              bg_color="transparent",
                              fg_color="transparent")
    folders_frame.pack(anchor="w", pady=5)

    def open_logs():
        """Opens the logs folder."""
        if globals.os_name.startswith("Windows"):
            logging.debug(f"Opening logs folder on Windows...")
            os.startfile(load_data_path("cache", "logs"))
        else:
            logging.debug(f"Opening logs folder on Linux...")
            subprocess.run(
                ['xdg-open', load_data_path("cache", "logs")], check=True)
    
    def open_chats():
        """Opens the chats folder."""
        if globals.os_name.startswith("Windows"):
            logging.debug(f"Opening chats folder on Windows...")
            os.startfile(load_data_path("local", "chats"))
        else:
            logging.debug(f"Opening chats folder on Linux...")
            subprocess.run(
                ['xdg-open', load_data_path("local", "chats")], check=True)
    
    def open_config():
        """Opens the settings folder."""
        if globals.os_name.startswith("Windows"):
            logging.debug(f"Opening settings folder on Windows...")
            os.startfile(load_data_path("config"))
        else:
            logging.debug(f"Opening settings folder on Linux...")
            subprocess.run(
                ['xdg-open', load_data_path("config")], check=True)

    ctk.CTkLabel(folders_frame,
                 text=None,
                 image=globals.note_icon).pack(side="left", padx=6, pady=0)

    ctk.CTkLabel(folders_frame,
                 text="Open Logs",
                 font=fonts.heading_font).pack(side="left", padx=(0, 12))

    logs_button = ctk.CTkButton(folders_frame,
                                text="Logs",
                                width=20,
                                command=lambda: open_logs())
    logs_button.pack(side="left", padx=(0, 12))

    ctk.CTkLabel(folders_frame,
                 text=None,
                 image=globals.chats_icon).pack(side="left", padx=6, pady=0)

    ctk.CTkLabel(folders_frame,
                 text="Open Chats",
                 font=fonts.heading_font).pack(side="left", padx=(0, 12))
    
    open_chats_button = ctk.CTkButton(folders_frame,
                                text="Chats",
                                width=20,
                                command=lambda: open_chats())
    open_chats_button.pack(side="left", padx=(0, 12))

    ctk.CTkLabel(folders_frame,
                 text=None,
                 image=globals.config_icon).pack(side="left", padx=6, pady=0)

    ctk.CTkLabel(folders_frame,
                 text="Open Config",
                 font=fonts.heading_font).pack(side="left", padx=(0, 12))
    
    open_config_button = ctk.CTkButton(folders_frame,
                                text="Config",
                                width=20,
                                command=lambda: open_config())
    open_config_button.pack(side="left", padx=(0, 12))

    # Deletion
    ctk.CTkLabel(advanced_frame,
                text="DANGER ZONE",
                font=fonts.title_font,
                fg_color="#d62828",
                anchor="center").pack(fill="x", pady=20, padx=10)

    top_deletion_frame = ctk.CTkFrame(advanced_frame,
                            bg_color="transparent",
                            fg_color="transparent")
    top_deletion_frame.pack(anchor="w", pady=5)

    ctk.CTkLabel(top_deletion_frame,
                text=None,
                image=globals.pearl_icon).pack(side="left", padx=6, pady=0)

    ctk.CTkLabel(top_deletion_frame,
                text="Factory Reset",
                font=fonts.heading_font).pack(side="left", padx=(0, 12))
    
    reset_pearl_button = ctk.CTkButton(top_deletion_frame,
                                text="Reset",
                                width=20,
                                command=lambda: total_factory_reset(globals))
    reset_pearl_button.pack(side="left", padx=(0, 12))
    reset_pearl_button.configure(fg_color="#d62828", hover_color="#ff3b30")

    if globals.ollama_active:
        ctk.CTkLabel(top_deletion_frame,
                    text=None,
                    image=globals.ollama_icon).pack(side="left", padx=6, pady=0)

        ctk.CTkLabel(top_deletion_frame,
                    text="Uninstall Ollama",
                    font=fonts.heading_font).pack(side="left", padx=(0, 12))
        
        uninstall_ollama_button = ctk.CTkButton(top_deletion_frame,
                                    text="Uninstall",
                                    width=20,
                                    command=lambda: uninstall_ollama(globals))
        uninstall_ollama_button.pack(side="left", padx=(0, 12))
        uninstall_ollama_button.configure(fg_color="#d62828", hover_color="#ff3b30")

    bottom_deletion_frame = ctk.CTkFrame(advanced_frame,
                                bg_color="transparent",
                                fg_color="transparent")
    bottom_deletion_frame.pack(anchor="w", pady=5)

    if globals.docker_active:
        ctk.CTkLabel(bottom_deletion_frame,
                    text=None,
                    image=globals.docker_icon).pack(side="left", padx=6, pady=0)

        ctk.CTkLabel(bottom_deletion_frame,
                    text="Uninstall Docker",
                    font=fonts.heading_font).pack(side="left", padx=(0, 12))
        
        uninstall_docker_button = ctk.CTkButton(bottom_deletion_frame,
                                    text="Uninstall",
                                    width=20,
                                    command=lambda: uninstall_docker(globals))
        uninstall_docker_button.pack(side="left", padx=(0, 12))
        uninstall_docker_button.configure(fg_color="#d62828", hover_color="#ff3b30")

    if globals.kokoro_active and globals.os_name.startswith("Linux"):
        ctk.CTkLabel(bottom_deletion_frame,
                    text=None,
                    image=globals.kokoro_icon).pack(side="left", padx=6, pady=0)

        ctk.CTkLabel(bottom_deletion_frame,
                    text="Uninstall Kokoro",
                    font=fonts.heading_font).pack(side="left", padx=(0, 12))
        
        uninstall_kokoro_button = ctk.CTkButton(bottom_deletion_frame,
                                    text="Uninstall",
                                    width=20,
                                    command=lambda: uninstall_kokoro(globals))
        uninstall_kokoro_button.pack(side="left", padx=(0, 12))
        uninstall_kokoro_button.configure(fg_color="#d62828", hover_color="#ff3b30")

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(advanced_frame,
                                     bg_color="transparent",
                                     fg_color="transparent")
    save_button_frame.pack(pady=10)

    ctk.CTkButton(save_button_frame,
                  text="Save Settings",
                  command=lambda: save_button(globals)).pack()

    def save_button(globals):
        """Saves and prompts for restart if required."""
        prompt_restart = False
        if globals.github_check != globals.github_check_var.get():
            prompt_restart = True
        elif globals.active_theme != globals.theme_var.get():
            prompt_restart = True
        elif globals.beta != globals.beta_var.get():
            prompt_restart = True
        save_all_settings(globals)

        if prompt_restart:
            if globals.qt_mode:
                reply = QMessageBox.question(
                    None,
                    "Restart Pearl?",
                    f"Would you like to restart Pearl to apply all changes?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes)
                if reply == QMessageBox.StandardButton.Yes:
                    subprocess.Popen(globals.app_path)
                    sys.exit(0)
            else:
                    reply = messagebox.askyesno(
                        parent=globals.root,
                        title="Restart Pearl",
                        message="Would you like restart Pearl to apply all changes?")
                    if reply:
                        subprocess.Popen(globals.app_path)
                        sys.exit(0)
