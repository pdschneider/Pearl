# Interface/Components/top_bar.py
import customtkinter as ctk
from CTkToolTip import CTkToolTip
from Interface.Components.sidebar import create_sidebar
from Managers.chat_history import start_new_conversation
import sounddevice as sd
import logging

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

    # Main top bar
    top_bar = ctk.CTkFrame(globals.root, height=55, corner_radius=0)
    globals.top_bar = top_bar
    top_bar.pack(side="top", fill="x")
    top_bar.pack_propagate(False)

    # Hamburger button (left)
    hamburger = ctk.CTkButton(
        top_bar,
        text="☰",
        width=45,
        height=45,
        command=lambda: create_sidebar(globals))
    hamburger.pack(side="left", padx=10, pady=5)
    globals.hamburger = hamburger
    CTkToolTip(hamburger, message="Chat History", delay=0.6, follow=True, padx=10, pady=5)

    # New Chat Button
    topbar_new_chat = ctk.CTkButton(
        top_bar,
        text="✎",
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

    # Settings gear (right)
    settings = ctk.CTkButton(
        top_bar,
        text="⚙",
        width=45,
        height=45)
    settings.pack(side="right", padx=10, pady=0)
    settings.configure(command=toggle_settings)
    CTkToolTip(settings, message="Settings", delay=0.6, follow=True, padx=10, pady=5)

    return top_bar
