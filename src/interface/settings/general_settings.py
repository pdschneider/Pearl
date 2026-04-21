# Interface/Settings/general_settings.py
from PySide6.QtWidgets import QMessageBox
from tkinter import messagebox
import shutil
import customtkinter as ctk
import src.utils.fonts as fonts
from CTkToolTip import CTkToolTip
import subprocess
import sys
from src.utils.save_settings import save_all_settings
from src.utils.load_settings import load_data_path
from src.utils.toast import show_toast


def create_general_settings_tab(globals, general_frame):
    """
    Creates the general settings tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    general_frame: The main frame
                    of the general settings window
    """

    ctk.CTkLabel(general_frame,
                 text="General Settings",
                 font=fonts.title_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)

    # Save_Chats Frame
    save_chats_frame = ctk.CTkFrame(general_frame,
                                 bg_color="transparent",
                                 fg_color="transparent")
    save_chats_frame.pack(fill="x", padx=10, pady=10)

    # Save Chats
    ctk.CTkLabel(save_chats_frame,
                 text=None,
                 image=globals.chat_icon).pack(side="left", padx=6, pady=0)

    save_chats_label = ctk.CTkLabel(save_chats_frame,
                                    text="Save Chats",
                                    font=fonts.heading_font)
    save_chats_label.pack(side="left", padx=(0, 12))
    CTkToolTip(save_chats_label,
               message="When on, chats are saved \nand can be accessed via \nchat history",
               delay=1.0,
               follow=True,
               padx=10,
               pady=5)

    ctk.CTkCheckBox(save_chats_frame,
                    variable=globals.save_chats_var,
                    onvalue=True,
                    text=None,
                    offvalue=False).pack(side="left", padx=5)

    # Language
    language_frame = ctk.CTkFrame(general_frame,
                                  bg_color="transparent",
                                  fg_color="transparent")
    language_frame.pack(fill="x", pady=10, padx=10)

    ctk.CTkLabel(language_frame,
                 text=None,
                 image=globals.en_language_icon).pack(side="left", padx=6, pady=0)

    language_label = ctk.CTkLabel(language_frame,
                                    text="Language",
                                    font=fonts.heading_font)
    language_label.pack(side="left", padx=(0, 12))
    CTkToolTip(language_label,
               message="Choose your language",
               delay=0.8,
               follow=True,
               padx=10,
               pady=5)

    ctk.CTkComboBox(language_frame,
                    variable=globals.language_var,
                    values=["English"],
                    state="readonly",
                    width=150).pack(side="left")

    # Theme Frame
    theme_frame = ctk.CTkFrame(general_frame,
                               bg_color="transparent",
                               fg_color="transparent")
    theme_frame.pack(fill="x", pady=10, padx=10)

    # Theme List
    themes_dict = [{"label": "Cosmic Sky", "theme": "cosmic_sky"},
                   {"label": "Pastel Green", "theme": "pastel_green"},
                   {"label": "Blazing Red", "theme": "blazing_red"},
                   {"label": "Dark Cloud", "theme": "dark_cloud"},
                   {"label": "Soft Light", "theme": "soft_light"}]
    theme_labels = [entry["label"] for entry in themes_dict]
    theme_names = [entry["theme"] for entry in themes_dict]
    label_to_theme = {entry["label"]: entry["theme"] for entry in themes_dict}

    label_var = ctk.StringVar()

    def update_theme_var(*args):
        selected_label = label_var.get()
        theme_name = label_to_theme.get(selected_label, "Cosmic Sky")
        globals.theme_var.set(theme_name)

    label_var.trace("w", update_theme_var)

    initial_theme = globals.theme_var.get()
    initial_label = next(
        (label for label, theme in label_to_theme.items() if theme == initial_theme), "Cosmic Sky")
    label_var.set(initial_label)

    ctk.CTkLabel(theme_frame,
                 text=None,
                 image=globals.theme_icon).pack(side="left", padx=6, pady=0)

    ctk.CTkLabel(theme_frame,
                 text="Theme",
                 font=fonts.heading_font).pack(side="left", padx=(0, 12))

    ctk.CTkComboBox(theme_frame,
                    variable=label_var,
                    values=theme_labels,
                    state="readonly",
                    width=150).pack(side="left")
    
    ctk.CTkLabel(theme_frame,
                 text="*Requires restart",
                 font=fonts.body_font).pack(side="left", padx=6, pady=0)

    # Version Check
    version_frame = ctk.CTkFrame(general_frame,
                                 bg_color="transparent",
                                 fg_color="transparent")
    version_frame.pack(fill="x", pady=10, padx=10)

    ctk.CTkLabel(version_frame,
                 text=None,
                 image=globals.notification_icon).pack(side="left", padx=6, pady=0)

    version_check_label = ctk.CTkLabel(version_frame,
                                    text="Check for Updates",
                                    font=fonts.heading_font)
    version_check_label.pack(side="left", padx=(0, 12))
    CTkToolTip(version_check_label,
               message="When on, pings github for the\nthe latest version of Pearl\non startup",
               delay=0.8,
               follow=True,
               padx=10,
               pady=5)

    ctk.CTkCheckBox(version_frame,
                    variable=globals.github_check_var,
                    onvalue=True,
                    text=None,
                    width=0,
                    offvalue=False).pack(side="left")
    
    ctk.CTkLabel(version_frame,
                 text="*Requires restart",
                 font=fonts.body_font).pack(side="left", padx=6, pady=0)
    
    # Beta Version
    beta_frame = ctk.CTkFrame(general_frame,
                              bg_color="transparent",
                              fg_color="transparent")
    beta_frame.pack(fill="x", pady=10, padx=10)

    ctk.CTkLabel(beta_frame,
                 text=None,
                 image=None,
                 width=40).pack(side="left", padx=6, pady=0)

    beta_check_label = ctk.CTkLabel(beta_frame,
                                    text="Include Beta Updates",
                                    font=fonts.heading_font)
    beta_check_label.pack(side="left", padx=(0, 12))
    CTkToolTip(beta_check_label,
               message="Inclides beta releases in version check",
               delay=0.8,
               follow=True,
               padx=10,
               pady=5)

    ctk.CTkCheckBox(beta_frame,
                    variable=globals.beta_var,
                    onvalue=True,
                    text=None,
                    width=0,
                    offvalue=False).pack(side="left")
    
    ctk.CTkLabel(beta_frame,
                 text="*Requires restart",
                 font=fonts.body_font).pack(side="left", padx=6, pady=0)

    # Context Detection
    context_frame = ctk.CTkFrame(general_frame,
                                  bg_color="transparent",
                                  fg_color="transparent")
    context_frame.pack(fill="x", pady=10, padx=10)

    ctk.CTkLabel(context_frame,
                 text=None,
                 image=globals.operations_icon).pack(side="left", padx=6, pady=0)

    context_label = ctk.CTkLabel(context_frame,
                                    text="Context Detection",
                                    font=fonts.heading_font)
    context_label.pack(side="left", padx=(0, 12))
    CTkToolTip(context_label,
               message="Turns on/off context detection",
               delay=0.8,
               follow=True,
               padx=10,
               pady=5)

    ctk.CTkCheckBox(context_frame,
                    variable=globals.enable_context_var,
                    onvalue=True,
                    text=None,
                    offvalue=False).pack(side="left", padx=5)
    
    # Title Generation
    title_gen_frame = ctk.CTkFrame(general_frame,
                                  bg_color="transparent",
                                  fg_color="transparent")
    title_gen_frame.pack(fill="x", pady=10, padx=10)

    ctk.CTkLabel(title_gen_frame,
                 text=None,
                 image=globals.title_icon).pack(side="left", padx=6, pady=0)

    context_label = ctk.CTkLabel(title_gen_frame,
                                    text="Generate Chat Titles",
                                    font=fonts.heading_font)
    context_label.pack(side="left", padx=(0, 12))
    CTkToolTip(context_label,
               message="Turns on/off title generation",
               delay=0.8,
               follow=True,
               padx=10,
               pady=5)

    ctk.CTkCheckBox(title_gen_frame,
                    variable=globals.generate_titles_var,
                    onvalue=True,
                    text=None,
                    offvalue=False).pack(side="left", padx=5)

    # Deletion Frame
    deletion_frame = ctk.CTkFrame(general_frame,
                                  bg_color="transparent",
                                  fg_color="transparent")
    deletion_frame.pack(fill="x", pady=10, padx=10)

    def delete_chats():
        # Create a messagebox asking for confirmation
        if globals.qt_mode:
            reply = QMessageBox.question(
                None,
                "Delete Chats",
                f"Are you sure you would like to delete all conversations?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes)
            if reply == QMessageBox.StandardButton.Yes:
                shutil.rmtree(load_data_path("local", "chats"))
                show_toast(globals, "Conversations deleted!")
        else:
            reply = messagebox.askyesno(
                globals.root,
                title="Delete Chats?",
                message="Would you like to delete all saved chats?")
            if reply:
                shutil.rmtree(load_data_path("local", "chats"))
                show_toast(globals, "Conversations deleted!")

    ctk.CTkLabel(deletion_frame,
                 text=None,
                 image=globals.delete_icon).pack(side="left", padx=6, pady=0)

    ctk.CTkLabel(deletion_frame,
                 text="Delete All Chats",
                 font=fonts.heading_font).pack(side="left", padx=(0, 12))

    delete_chats_button = ctk.CTkButton(deletion_frame,
                                        text="Delete",
                                        width=25,
                                        command=lambda: delete_chats())
    delete_chats_button.configure(fg_color="#d62828", hover_color="#ff3b30")
    delete_chats_button.pack(side="left")

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(general_frame,
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
