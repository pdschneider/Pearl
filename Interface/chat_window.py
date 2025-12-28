# Interface/chat_window.py
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from CTkToolTip import CTkToolTip
from Managers.chat_manager import send_message
import Utils.fonts as fonts
import logging
from Interface.Components.widgets import ButtonWidgets

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

    # Menu for Bubbles
    right_click_menu = tk.Menu(chat_tab, tearoff=False)
    right_click_menu.add_command(label="Copy", command=lambda: copy_bubble_text(current_label[0]))

    current_label = [None]

    chat_frame = ctk.CTkScrollableFrame(chat_tab)
    chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

    entry_frame = ctk.CTkFrame(chat_tab, fg_color="transparent")
    entry_frame.pack(fill="both", padx=10, pady=5)

    entrybox = ctk.CTkTextbox(entry_frame,
              font=fonts.body_font,
              wrap="word",
              state=widget_state,
              corner_radius=16,
              height=100)
    entrybox.pack(side="left", padx=5, pady=5, fill="x", expand=True)
    entrybox.focus_set()

    send_button = ctk.CTkButton(entry_frame,  # Send button
               text="➤",
               state=widget_state,
               height=50,
               width=40,
               corner_radius=35,
               command=lambda: send_message(globals, ui_elements))
    send_button.pack(side="top", padx=5, pady=5)
    CTkToolTip(send_button, message="Send", delay=1.0, follow=True, padx=10, pady=5)

    file_button = ctk.CTkButton(entry_frame,  # Send button
               text="📎",
               state=widget_state,
               height=50,
               width=40,
               corner_radius=35,
               command=lambda: attach_file())
    globals.file_button = file_button
    globals.file_button.pack(side="bottom", padx=5, pady=5)
    attach_tip = CTkToolTip(file_button, message="Attach", delay=1.0, follow=True, padx=10, pady=5)
    globals.attach_tip = attach_tip

    # Chat Functions
    def add_bubble(role, text=""):
        """Appends messages to the chat box."""
        bubble_frame = ctk.CTkFrame(chat_frame, corner_radius=6)

        if role == "user":
            bubble_frame.configure(fg_color=globals.theme_dict["CTk"]["fg_color"],
                                corner_radius=6)
        else:
            bubble_frame.configure(fg_color=globals.theme_dict["CTk"]["fg_color"],
                                   corner_radius=6)
            name_label = ctk.CTkLabel(chat_frame, text="Pearl", font=fonts.heading_font)
            name_label.pack(side="top",anchor="w", padx=20, pady=0)
        bubble_frame.pack(side="top", anchor="e" if role == "user" else "w", padx=20, pady=0)

        label = ctk.CTkLabel(bubble_frame, text=text, wraplength=600, font=fonts.message_font, justify="right" if role == "user" else "left",
                             padx=15, pady=10, anchor="w" if role != "user" else "e")
        label.pack(fill="both", expand=True)

        # Pack widgets underneath messages
        widgets_row = ButtonWidgets(parent=bubble_frame,
                                    globals=globals,
                                 label=label,
                                 copy_callback=copy_bubble_text)
        widgets_row.pack(fill="x")
        widgets_row.hide_buttons()

        def on_enter(event):
            widgets_row.show_buttons()

        def on_leave(event):
            widgets_row.hide_buttons()

        def on_right_click(event, lbl=label):
            current_label[0] = lbl
            right_click_menu.tk_popup(event.x_root, event.y_root)

        label.bind("<Enter>", on_enter) #  Shows the widget buttons on mouse hover

        widgets_row.bind("<Enter>", on_enter)

        bubble_frame.bind("<Enter>", on_enter)

        label.bind("<Button-3>", on_right_click) #  Shows menu on right click

        chat_frame._parent_canvas.after(100, lambda: chat_frame._parent_canvas.yview_moveto(1.0))

        return label

    def copy_bubble_text(lbl):
        """Creates a menu option for copying message text."""
        if lbl is None:
            return
        full_text = lbl.cget("text")
        chat_tab.clipboard_clear()
        chat_tab.clipboard_append(full_text.strip())
        chat_tab.update()

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

    accepted_filetypes = [".txt", ".csv", ".json"
                          ".py", ".pyw", ".spec", 
                          ".log", ".ini", ".cfg", ".xml", 
                          ".sh", ".bat", ".ps1", 
                          ".md", ".tsv", ".toml", ".yaml", 
                          ".html", ".css"]

    def attach_file():
        file = filedialog.askopenfilename(parent=globals.file_button, 
                                                             title="Select Attachment", 
                                                             filetypes=(("All files", "*.*"), 
                                                                        ("Text files", "*.txt"), 
                                                                        ("CSV files", "*.csv"),
                                                                        ("Python files", "*.py")))
        if not file:
            return
        try:
            for i in accepted_filetypes:
                if file.endswith(i):
                    with open(file, "r") as f:
                        globals.file_attachment = f.read()
            if not globals.file_attachment:
                logging.warning(f"File type not supported: {file}")
                messagebox.showwarning(parent=file_button, title="Unsupported File Type", message=f"File type not supported: {file}")
                return
        except Exception as e:
            logging.warning(f"Could not attach file due to: {e}")
            messagebox.showwarning(parent=file_button, title="Attachment Not Supported", message=f"Could not attach file due to: {e}. Likely an unsupported file type with the wrong extension.")
            return
        if globals.file_attachment:
            file_button.configure(state="disabled")
            attach_tip.configure(message="File Already Attached")
        logging.debug(f"File attachment: {file}")
