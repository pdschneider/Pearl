# Interface/Components/top_bar.py
import customtkinter as ctk
from CTkToolTip import CTkToolTip
from tkinter import messagebox
from PySide6.QtWidgets import QMessageBox
from src.interface.components.sidebar import create_sidebar
from src.managers.chat_history import start_new_conversation
from src.utils.load import load_data_path
from src.utils.refresher import refresh_gui
import sounddevice as sd
import logging
import webbrowser
import urllib.parse


def create_top_bar(globs):
    """
    Creates the top bar for navigation.

            Parameters:
                    globs: Global variables

            Returns:
                    top_bar: The top_bar frame and its child widgets
    """
    def toggle_settings():
        """Shows and hides the settings window when the button is clicked."""
        # Ensure Ollama is active
        refresh_gui(globs)

        # Map settings page
        if globs.settings_page.winfo_ismapped():
            globs.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
            globs.settings_page.pack_forget()
        else:
            app_pages = [globs.chat_page, globs.setup_page, globs.changelog]
            for page in app_pages:
                if page:
                    page.pack_forget()
            globs.settings_page.pack(fill="both", expand=True, padx=10, pady=0)

    def reset_to_new_chat():
        """Resets to a new conversation and clears the chat frame."""
        # Stop sound, trigger flags, health check, and raise chat page
        sd.stop()
        start_new_conversation(globs)
        refresh_gui(globs)
        globs.app_title.configure(text="Pearl at your service!")

        # Clear the current chat bubbles
        for widget in globs.chat_frame.winfo_children():
            widget.destroy()
        globs.chat_frame._parent_canvas.yview_moveto(0.0)
        globs.root.update_idletasks()

        # Map chat page
        app_pages = [globs.chat_page, globs.setup_page, globs.settings_page, globs.changelog]
        for page in app_pages:
            if page:
                page.pack_forget()
        globs.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
        logging.info(f"Started new chat from the top bar button.")

    def report_bug(globs):
        """Opens the default mail application to report a bug."""

        if not globs.legacy_mode:
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
                f" | Pearl Version: {globs.current_version} | OS: {globs.os_name}"
                encoded_body = urllib.parse.quote(body)
                mailto = f"mailto:{to}?subject={subject}&body={encoded_body}"
                webbrowser.open(mailto)
        else:
            reply = messagebox.askyesno(
                parent=globs.root,
                title="Report Bug?",
                message=f"Open the default email application to report a bug?")
            
            if reply:
                logging.debug(f"Bug Report button clicked.")
                to = "bugs@phillipplays.com"
                subject = "Bug Report for Pearl"
                body = f"Thank you very much for making a report! " \
                f"Let me know what problem occurred, the behavior your expected, " \
                f"and feel free to also include any logs or screenshots that may help! " \
                f" | Pearl Version: {globs.current_version} | OS: {globs.os_name}"
                encoded_body = urllib.parse.quote(body)
                mailto = f"mailto:{to}?subject={subject}&body={encoded_body}"
                webbrowser.open(mailto)

    # Main top bar
    top_bar = ctk.CTkFrame(globs.root, height=55, corner_radius=0)
    globs.top_bar = top_bar
    top_bar.pack(side="top", fill="x")
    top_bar.pack_propagate(False)

    # Hamburger button (left)
    hamburger = ctk.CTkButton(
        top_bar,
        image=globs.hamburger_icon,
        text=None,
        width=45,
        height=45,
        command=lambda: create_sidebar(globs))
    hamburger.pack(side="left", padx=10, pady=5)
    globs.hamburger = hamburger
    CTkToolTip(hamburger,
               message="Chat History",
               delay=0.6,
               follow=True,
               padx=10,
               pady=5)

    # New Chat Button (left)
    topbar_new_chat = ctk.CTkButton(
        top_bar,
        image=globs.new_chat_icon,
        text=None,
        width=45,
        height=45,
        command=lambda: reset_to_new_chat())
    topbar_new_chat.pack(side="left", padx=0, pady=5)
    CTkToolTip(topbar_new_chat,
               message="New Chat",
               delay=0.6,
               follow=True,
               padx=10,
               pady=5)

    # Title (center)
    globs.app_title = ctk.CTkLabel(
        top_bar,
        text="Pearl at your service!",
        font=ctk.CTkFont(size=20, weight="bold"))
    globs.app_title.pack(side="left", expand=True)

    # Settings Gear (right)
    settings = ctk.CTkButton(
        top_bar,
        image=globs.settings_icon,
        text=None,
        width=45,
        height=45)
    settings.pack(side="right", padx=10, pady=5)
    settings.configure(command=toggle_settings)
    CTkToolTip(settings,
               message="Settings",
               delay=0.6,
               follow=True,
               padx=10,
               pady=5)

    # Bug Report (right)
    bug_report = ctk.CTkButton(
        top_bar,
        image=globs.bug_icon,
        text=None,
        width=45,
        height=45)
    bug_report.pack(side="right", padx=0, pady=5)
    bug_report.configure(command=lambda: report_bug(globs))
    CTkToolTip(bug_report,
               message="Report a bug",
               delay=0.6,
               follow=True,
               padx=10,
               pady=5)

    return top_bar
