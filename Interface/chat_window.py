# Interface/chat_window.py
import tkinter as tk
import customtkinter as ctk
from Managers.chat_manager import send_message
import Utils.fonts as fonts

def create_chat_tab(globals, chat_tab):
    """
    Creates the chat frame for talking with the LLM.

            Parameters:
                    globals: Global variables
                    chat_tab: The main frame of the chat window
    """
    # Sets tkinter widgets to inactive status if Ollama isn't found
    widget_state = None
    if globals.ollama_active:
        widget_state = "normal"
    else:
        widget_state = "disabled"

    chat_frame = ctk.CTkScrollableFrame(chat_tab)
    chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

    entry_frame = ctk.CTkFrame(chat_tab, fg_color="transparent")
    entry_frame.pack(fill="both", padx=10, pady=5)

    entrybox = ctk.CTkTextbox(entry_frame,
              font=fonts.body_font,
              wrap="word",
              fg_color="white",
              state=widget_state,
              corner_radius=16,
              height=100)
    entrybox.pack(side="left", padx=5, pady=5, fill="x", expand=True)
    entrybox.focus_set()

    send_button = ctk.CTkButton(entry_frame, #  Send button
               text="➤",
               state=widget_state,
               height=50,
               width=40,
               corner_radius=35,
               command=lambda: send_message(globals, ui_elements))
    send_button.pack(side="left", padx=5, pady=5)

    # Chat Functions
    def add_bubble(role, text=""):
        """Appends messages to the chat box."""
        bubble_frame = ctk.CTkFrame(chat_frame, corner_radius=6)

        if role == "user":
            bubble_frame.configure(corner_radius=6)
        else:
            bubble_frame.configure(fg_color=globals.theme_dict["CTkScrollableFrame"]["border_color"],
                                corner_radius=20, width=650)
        bubble_frame.pack(side="top", anchor="e" if role == "user" else "w", padx=20, pady=6)

        label = ctk.CTkLabel(bubble_frame, text=text, wraplength=600, justify="right" if role == "user" else "left",
                             padx=15, pady=10, anchor="w" if role != "user" else "e")
        label.pack(fill="both", expand=True)

        chat_frame._parent_canvas.after(100, lambda: chat_frame._parent_canvas.yview_moveto(1.0))

        return label

    def upon_enter():
        """Triggers send message and prevents additional lines in the entry box upon pressing enter."""
        if globals.still_streaming:
            globals.cancel_event.set() if globals.cancel_event else None
        else:
            send_message(globals, ui_elements)
        return "break"

    def upon_shift_enter():
        """Ensures Shift+Enter creates a new line in the entry box and nothing more."""
        entrybox.insert(tk.INSERT, "\n")
        return "break"

    entrybox.bind("<Return>", lambda e: upon_enter() if not e.state & 1 else "break")
    entrybox.bind("<Shift-Return>", lambda e: upon_shift_enter())

    ui_elements = {
        "entrybox": entrybox,
        "chat_frame": chat_frame,
        "add_bubble": add_bubble,
        "send_button": send_button,
        "scroll_to_bottom": lambda: chat_frame._parent_canvas.yview_moveto(1.0)}

    globals.ui_elements = ui_elements
