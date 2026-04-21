# Interface/Components/top_bar.py
import customtkinter as ctk
from CTkToolTip import CTkToolTip
from tkinter import messagebox
from PySide6.QtWidgets import QMessageBox
from src.interface.components.sidebar import create_sidebar
from src.managers.chat_history import start_new_conversation
from src.utils.load_settings import load_data_path
from src.utils.refresher import refresh_gui
import sounddevice as sd
import logging
import webbrowser
import urllib.parse


def create_top_bar(globals):
    """
    Creates the top bar for navigation.

            Parameters:
                    globals: Global variables

            Returns:
                    top_bar: The top_bar frame and its child widgets
    """
    def toggle_settings():
        """Shows and hides the settings window when the button is clicked."""
        # Ensure Ollama is active
        refresh_gui(globals)

        # Map settings page
        if globals.settings_page.winfo_ismapped():
            globals.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
            globals.settings_page.pack_forget()
        else:
            app_pages = [globals.chat_page, globals.setup_page, globals.changelog]
            for page in app_pages:
                if page:
                    page.pack_forget()
            globals.settings_page.pack(fill="both", expand=True, padx=10, pady=0)

    def reset_to_new_chat():
        """Resets to a new conversation and clears the chat frame."""
        # Stop sound, trigger flags, health check, and raise chat page
        sd.stop()
        start_new_conversation(globals)
        refresh_gui(globals)
        globals.app_title.configure(text="Pearl at your service!")

        # Clear the current chat bubbles
        for widget in globals.chat_frame.winfo_children():
            widget.destroy()
        globals.chat_frame._parent_canvas.yview_moveto(0.0)
        globals.root.update_idletasks()

        # Map chat page
        app_pages = [globals.chat_page, globals.setup_page, globals.settings_page, globals.changelog]
        for page in app_pages:
            if page:
                page.pack_forget()
        globals.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
        logging.info(f"Started new chat from the top bar button.")

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

    # Main top bar
    top_bar = ctk.CTkFrame(globals.root, height=55, corner_radius=0)
    globals.top_bar = top_bar
    top_bar.pack(side="top", fill="x")
    top_bar.pack_propagate(False)

    # Hamburger button (left)
    hamburger = ctk.CTkButton(
        top_bar,
        image=globals.hamburger_icon,
        text=None,
        width=45,
        height=45,
        command=lambda: create_sidebar(globals))
    hamburger.pack(side="left", padx=10, pady=5)
    globals.hamburger = hamburger
    CTkToolTip(hamburger,
               message="Chat History",
               delay=0.6,
               follow=True,
               padx=10,
               pady=5)

    # New Chat Button (left)
    topbar_new_chat = ctk.CTkButton(
        top_bar,
        image=globals.new_chat_icon,
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
    globals.app_title = ctk.CTkLabel(
        top_bar,
        text="Pearl at your service!",
        font=ctk.CTkFont(size=20, weight="bold"))
    globals.app_title.pack(side="left", expand=True)

    # Settings Gear (right)
    settings = ctk.CTkButton(
        top_bar,
        image=globals.settings_icon,
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
        image=globals.bug_icon,
        text=None,
        width=45,
        height=45)
    bug_report.pack(side="right", padx=0, pady=5)
    bug_report.configure(command=lambda: report_bug(globals))
    CTkToolTip(bug_report,
               message="Report a bug",
               delay=0.6,
               follow=True,
               padx=10,
               pady=5)

    return top_bar
