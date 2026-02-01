# Interface/Components/top_bar.py
import customtkinter as ctk
from customtkinter import CTkImage
from CTkToolTip import CTkToolTip
from Interface.Components.sidebar import create_sidebar
from Managers.chat_history import start_new_conversation
from Utils.load_settings import load_data_path
import sounddevice as sd
from PIL import Image
import logging, textwrap
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
        try:
            if globals.setup_page.winfo_ismapped() or globals.changelog.winfo_ismapped():
                globals.greeting = "Welcome!"
                return
        except:
            pass
        if globals.chat_page.winfo_ismapped():
            globals.chat_page.pack_forget()
        else:
            globals.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
        if globals.settings_overlay.winfo_ismapped():
            globals.settings_overlay.pack_forget()
        else:
            globals.settings_overlay.pack(fill="both", expand=True, padx=10, pady=0)
            globals.settings_overlay.tkraise()

    def reset_to_new_chat():
        """Resets to a new conversation and clears the chat frame."""
        sd.stop()
        start_new_conversation(globals)

        # Clear the current chat bubbles
        for widget in globals.ui_elements["chat_frame"].winfo_children():
            widget.destroy()
        globals.ui_elements["scroll_to_bottom"]()
        globals.root.update_idletasks()
        logging.info(f"Started new chat from the top bar button.")

    def report_bug():
        to="bugs@phillipplays.com"
        subject="Bug Report for Pearl"
        raw_body="""Thank you very much for making a report!
                    Let me know what problem occurred, your OS, the version of Pearl you are using, 
                    and feel free to also include any logs or screenshots that may help!"""
        body=textwrap.dedent(raw_body).strip()
        encoded_body=urllib.parse.quote(body)
        mailto = f"mailto:{to}?subject={subject}&body={encoded_body}"
        webbrowser.open(mailto)

    # Get Icons
    globals.hamburger_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/hamburger.png")),
    dark_image=Image.open(load_data_path("config", "assets/hamburger.png")),
    size=(35, 35))

    globals.settings_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/settings.png")),
    dark_image=Image.open(load_data_path("config", "assets/settings.png")),
    size=(35, 35))

    globals.bug_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/bug-2.png")),
    dark_image=Image.open(load_data_path("config", "assets/bug-2.png")),
    size=(35, 35))

    globals.new_chat_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/pencil.png")),
    dark_image=Image.open(load_data_path("config", "assets/pencil.png")),
    size=(35, 35))

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
    CTkToolTip(hamburger, message="Chat History", delay=0.6, follow=True, padx=10, pady=5)

    # New Chat Button (left)
    topbar_new_chat = ctk.CTkButton(
        top_bar,
        image=globals.new_chat_icon,
        text=None,
        width=45,
        height=45,
        command=lambda: reset_to_new_chat())
    topbar_new_chat.pack(side="left", padx=0, pady=5)
    CTkToolTip(topbar_new_chat, message="New Chat", delay=0.6, follow=True, padx=10, pady=5)

    # Title (center)
    title = ctk.CTkLabel(
        top_bar,
        text=globals.greeting,
        font=ctk.CTkFont(size=20, weight="bold"))
    title.pack(side="left", expand=True)

    # Settings Gear (right)
    settings = ctk.CTkButton(
        top_bar,
        image=globals.settings_icon,
        text=None,
        width=45,
        height=45)
    settings.pack(side="right", padx=10, pady=5)
    settings.configure(command=toggle_settings)
    CTkToolTip(settings, message="Settings", delay=0.6, follow=True, padx=10, pady=5)

    # Bug Report (right)
    bug_report = ctk.CTkButton(
        top_bar,
        image=globals.bug_icon,
        text=None,
        width=45,
        height=45)
    bug_report.pack(side="right", padx=0, pady=5)
    bug_report.configure(command=report_bug)
    CTkToolTip(bug_report, message="Report a bug", delay=0.6, follow=True, padx=10, pady=5)

    return top_bar
