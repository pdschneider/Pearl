# src/interface/chat_window.py
import tkinter as tk
import customtkinter as ctk
from CTkToolTip import CTkToolTip
from src.managers.chat_manager import send_message
from src.managers.attachments import attach_file
import src.utils.fonts as fonts
import logging
import time
from src.interface.components.widgets import ButtonWidgets


def create_chat_tab(globs, chat_tab):
    """
    Creates the chat frame for talking with the LLM.

            Parameters:
                    globs: Global variables
                    chat_tab: The main frame of the chat window
    """

    # Menu for Bubbles
    right_click_menu = tk.Menu(chat_tab, tearoff=False)
    right_click_menu.add_command(
        label="Copy",
        command=lambda: copy_bubble_text(current_label[0]))

    current_label = [None]

    globs.chat_frame = ctk.CTkScrollableFrame(chat_tab)
    globs.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Entry Box
    entry_frame = ctk.CTkFrame(chat_tab, fg_color="transparent")
    entry_frame.pack(fill="both", padx=10, pady=5)

    globs.input_box = ctk.CTkTextbox(entry_frame,
                              font=fonts.body_font,
                              wrap="word",
                              state="normal",
                              corner_radius=16,
                              height=100)
    globs.input_box.pack(side="left", padx=5, pady=5, fill="x", expand=True)
    globs.input_box.focus_set()

    # Send Button
    globs.send_button = ctk.CTkButton(entry_frame,
                                image=globs.send_icon,
                                text=None,
                                state="normal",
                                height=50,
                                width=40,
                                corner_radius=20,
                                command=lambda: send_message(globs, ui_elements))
    globs.send_button.pack(side="top", padx=5, pady=5)
    CTkToolTip(globs.send_button,
               message="Send",
               delay=1.0,
               follow=True,
               padx=10,
               pady=5)

    # File Button
    file_button = ctk.CTkButton(entry_frame,
                                image=globs.attach_icon,
                                text=None,
                                state="normal",
                                height=50,
                                width=40,
                                corner_radius=20,
                                command=lambda: attach_file(globs))
    globs.file_button = file_button
    globs.file_button.pack(side="bottom", padx=5, pady=5)
    globs.attach_tip = CTkToolTip(file_button,
                            message="Attach",
                            delay=1.0,
                            follow=True,
                            padx=10,
                            pady=5)

    # Chat Functions
    def add_bubble(globs, role="user", text="", model=None, prompt=None, tokens=0):
        """Appends messages to the chat box."""
        try:
            bubble_frame = ctk.CTkFrame(globs.chat_frame, corner_radius=6)

            # Configure and pack chat bubble frame
            if role == "user":
                bubble_frame.configure(
                    fg_color=globs.theme_dict["CTk"]["fg_color"],
                    bg_color=globs.theme_dict["CTk"]["fg_color"],
                    border_color=globs.theme_dict["CTk"]["fg_color"],
                    corner_radius=6)
            else:
                bubble_frame.configure(
                    fg_color=globs.theme_dict["CTk"]["fg_color"],
                    bg_color=globs.theme_dict["CTk"]["fg_color"],
                    border_color=globs.theme_dict["CTk"]["fg_color"],
                    corner_radius=6)

                # Create and pack assistant name only for assistant messages
                name_label = ctk.CTkLabel(globs.chat_frame,
                                        text="Pearl",
                                        font=fonts.heading_font)
                name_label.pack(side="top",
                                anchor="w",
                                padx=20,
                                pady=0)
            bubble_frame.pack(side="top",
                            anchor="e" if role == "user" else "w", padx=20, pady=0)
        except Exception as e:
            logging.error(f"Could not create chat bubble frame due to: {e}")

        # Add text to message box
        try:
            label = ctk.CTkLabel(bubble_frame,
                                text=text,
                                wraplength=600,
                                font=fonts.message_font,
                                justify="right" if role == "user" else "left",
                                padx=15,
                                pady=10,
                                anchor="w" if role != "user" else "e")
            label.pack(fill="both", expand=True)
        except Exception as e:
            logging.error(f"Could not add text to chat bubble frame due to: {e}")

        # Pack widgets underneath messages
        widgets_row = ButtonWidgets(parent=bubble_frame,
                                    globs=globs,
                                    label=label,
                                    copy_callback=copy_bubble_text,
                                    model=model,
                                    attachment=globs.file_attachment,
                                    prompt=globs.active_prompt,
                                    tokens=tokens,
                                    role=role,
                                    text=text,
                                    message_index=len(globs.conversation_history))
        widgets_row.pack(fill="x")
        widgets_row.hide_buttons()
        globs.widget_rows.append(widgets_row)

        # Widget events
        def on_enter(event):
            """Show widgets when the mouse hovers over a message."""
            widgets_row.show_buttons()

        def on_leave(event):
            """Hide widgets when the mouse leaves a message."""
            hide_all_buttons()

        def on_right_click(event, lbl=label):
            current_label[0] = lbl
            right_click_menu.tk_popup(event.x_root, event.y_root)

        # Shows the widget buttons on mouse hover
        label.bind("<Enter>", on_enter)
        widgets_row.bind("<Enter>", on_enter)
        bubble_frame.bind("<Enter>", on_enter)

        # Hides widget buttons when mouse leaves
        label.bind("<Leave>", on_leave)
        bubble_frame.bind("<Leave>", on_leave)
        entry_frame.bind("<Enter>", on_leave)
        globs.chat_frame.bind("<Leave>", on_leave)

        # Shows menu on right click
        label.bind("<Button-3>", on_right_click)

        globs.chat_frame._parent_canvas.after(
            100,
            lambda: globs.chat_frame._parent_canvas.yview_moveto(1.0))

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
        """Triggers send message and prevents additional
        lines in the entry box upon pressing enter."""
        if globs.still_streaming:
            logging.debug(f"Enter button pressed.")
            if globs.input_box.get("1.0", "end").strip():
                if time.time() - globs.last_message_time >= 2:
                    globs.cancel_event.set() if globs.cancel_event else None
                send_message(globs, ui_elements)
            else:
                return "break"
        else:
            logging.debug(f"Enter button pressed.")
            send_message(globs, ui_elements)
        return "break"

    def upon_shift_enter():
        """Ensures Shift+Enter creates a new line
        in the entry box and nothing more."""
        globs.input_box.insert(tk.INSERT, "\n")
        return "break"

    globs.input_box.bind("<Return>", lambda e: upon_enter() if not e.state & 1 else "break")
    globs.input_box.bind("<Shift-Return>", lambda e: upon_shift_enter())

    def hide_all_buttons():
        """Hide all widget buttons."""
        for row in globs.widget_rows:
            row.hide_buttons()

    ui_elements = {
        "add_bubble": lambda *args, **kwargs: add_bubble(*args, **kwargs)}

    globs.ui_elements = ui_elements
