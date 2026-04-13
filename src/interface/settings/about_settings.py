# Interface/Settings/about_settings.py
import customtkinter as ctk
import src.utils.fonts as fonts
import webbrowser
import logging
from tkinter import messagebox
from PySide6.QtWidgets import QMessageBox
import urllib.parse
from CTkToolTip import CTkToolTip
from src.utils.refresher import refresh_gui
from src.interface.setup.setup_wizard import create_wizard


def create_about_tab(globals, about_frame):
    """
    Creates the about tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    about_frame: The main frame of the about tab
    """

    ctk.CTkLabel(about_frame,
                 text="About",
                 font=fonts.title_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)

    readme_frame = ctk.CTkScrollableFrame(about_frame, fg_color="transparent")
    readme_frame.pack(fill="both", expand=True, padx=10, pady=0)

    ctk.CTkLabel(
        readme_frame,
        justify="left",
        text=
"""
Pearl — Personal Everything Assistant Running Locally

Pearl is your friendly, fully local AI companion. 
Everything stays on your computer — no cloud, no tracking, no surprises.

She chats with you privately, switches context smartly based on keywords, 
supports file uploads, remembers chats only if you want, 
and looks good doing it with 5 built-in themes.

Fully offline after setup if you choose. Your data, your rules.

Key Features
• Completely private AI conversations
• Dynamic context switching (no manual prompts needed)
• Optional chat saving — delete anytime
• File uploads
• 5 beautiful themes
• Optional Kokoro TTS voice output

Requirements
• Ollama running locally (llama3.2:latest recommended for best compatibility)
• Kokoro Fast-API server (optional for TTS)
• Linux (Ubuntu 18.04+) or Windows 10/11
• Minimum: 4-core CPU, 8 GB RAM, 50 GB+ free space recommended

Icon by Twoeliz

Disclaimer — Third-Party AI Models
Pearl lets you use open-source AI models of your choice. 
The developer is not responsible for the accuracy, legality, appropriateness, 
or safety of any AI-generated content. Outputs are provided AS-IS with no warranties. 
You are fully responsible for choosing models, configuring safeguards, 
and any consequences from their use. By running Pearl you accept this.

Have fun!
""").pack(padx=5, pady=5)

    ctk.CTkLabel(about_frame,
                 text=f"Current Version: {globals.current_version}",
                 anchor="center").pack(fill="x", pady=20, padx=10)

    buttons_frame = ctk.CTkFrame(about_frame, fg_color="transparent")
    buttons_frame.pack(padx=10, pady=10)

    ctk.CTkButton(buttons_frame,
                  text="View Setup Page",
                  command=lambda: bring_back_setup(globals)).grid(
                      row=0, column=0, padx=5)
    
    ctk.CTkButton(buttons_frame,
                  text="Open Wizard",
                  command=lambda: create_wizard(globals)).grid(
                      row=0, column=1, padx=5)

    ctk.CTkButton(buttons_frame,
                  text="View Changelog",
                  command=lambda: show_changelog(globals)).grid(
                      row=0, column=2, padx=5)

    ctk.CTkButton(buttons_frame,
                  text="Report a Bug",
                  command=lambda: report_bug(globals)).grid(
                      row=0, column=3, padx=5)

    github_button = ctk.CTkButton(buttons_frame,
                                  text="View Github",
                                  command=lambda: webbrowser.open(
                                      url="https://github.com/pdschneider/Pearl"))
    github_button.grid(row=0, column=4, padx=5)

    CTkToolTip(github_button,
               message="Opens in default web browser",
               delay=0.6,
               follow=True,
               padx=10,
               pady=5)

    def bring_back_setup(globals):
        """Reinitiates the setup window."""
        refresh_gui(globals)
        globals.app_title.configure(text="Welcome to Pearl!")
        globals.settings_page.pack_forget()
        globals.setup_page.pack(fill="both", expand=True, padx=10, pady=0)

    def show_changelog(globals):
        """Brings up the changelog window."""
        refresh_gui(globals)
        globals.app_title.configure(text="Changelog")
        globals.settings_page.pack_forget()
        globals.chat_page.pack_forget()
        globals.changelog.pack(fill="both", expand=True, padx=10, pady=0)

    def report_bug(globals):
        """Opens the default mail application to report a bug."""

        if globals.qt_mode:
            # Display a messagebox first
            reply = QMessageBox.question(
                None,
                "Report Bug?",
                f"Would you like to open your default email application for a bug report?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes)
            
            # Opens up the default email application
            if reply == QMessageBox.StandardButton.Yes:
                logging.debug(f"Bug Report button clicked.")
                to = "bugs@phillipplays.com"
                subject = "Bug Report for Pearl"
                body = f"Thank you very much for making a report! " \
                f"Let me know what problem occurred, the behavior your expected, " \
                f"and feel free to also include any logs or screenshots that may help! " \
                f" | Pearl Version: {globals.current_version} | OS: {globals.os_name}"
                encoded_body = urllib.parse.quote(body)
                mailto = f"mailto:{to}?subject={subject}&body={encoded_body}"
                webbrowser.open(mailto)
        else:
            reply = messagebox.askyesno(
                parent=globals.root,
                title="Report Bug?",
                message=f"Open the default email application to report a bug?")
            
            if reply:
                logging.debug(f"Bug Report button clicked.")
                to = "bugs@phillipplays.com"
                subject = "Bug Report for Pearl"
                body = f"Thank you very much for making a report! " \
                f"Let me know what problem occurred, the behavior your expected, " \
                f"and feel free to also include any logs or screenshots that may help! " \
                f" | Pearl Version: {globals.current_version} | OS: {globals.os_name}"
                encoded_body = urllib.parse.quote(body)
                mailto = f"mailto:{to}?subject={subject}&body={encoded_body}"
                webbrowser.open(mailto)
