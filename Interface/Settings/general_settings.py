# Interface/Settings/general_settings.py
import tkinter as tk
from tkinter import messagebox
import shutil
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import Utils.fonts as fonts
from CTkToolTip import CTkToolTip
from Utils.save_settings import save_all_settings
from Utils.load_settings import load_data_path
from Utils.toast import show_toast

def create_general_settings_tab(globals, general_frame):
    """
    Creates the general settings tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    general_frame: The main frame of the general settings window
    """

    # Get Icons
    globals.chat_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/chat.png")),
    dark_image=Image.open(load_data_path("config", "assets/chat.png")),
    size=(40, 40))

    globals.theme_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/theme.png")),
    dark_image=Image.open(load_data_path("config", "assets/theme.png")),
    size=(40, 40))

    globals.delete_icon = CTkImage(
    light_image=Image.open(load_data_path("config", "assets/cancel.png")),
    dark_image=Image.open(load_data_path("config", "assets/cancel.png")),
    size=(40, 40))

    ctk.CTkLabel(general_frame, 
             text="General Settings", 
             font=fonts.title_font,
             anchor="center").pack(fill="x", pady=20, padx=10)

    # Options Frame
    options_frame = ctk.CTkFrame(general_frame, bg_color="transparent", fg_color="transparent")
    options_frame.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(options_frame, text=None, image=globals.chat_icon).pack(side="left", padx=6, pady=0)

    save_chats_label = ctk.CTkLabel(options_frame,
              text="Save Chats",
              font=fonts.heading_font)
    save_chats_label.pack(side="left", padx=(0, 12))
    CTkToolTip(save_chats_label, message="When on, chats are saved \nand can be accessed via \nchat history", delay=1.0, follow=True, padx=10, pady=5)

    ctk.CTkCheckBox(options_frame,
                    variable=globals.save_chats_var,
                    onvalue=True,
                    text=None,
                    offvalue=False).pack(side="left", padx=5)

    # Theme Frame
    theme_frame = ctk.CTkFrame(general_frame, bg_color="transparent", fg_color="transparent")
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

    label_var = tk.StringVar()

    def update_theme_var(*args):
        selected_label = label_var.get()
        theme_name = label_to_theme.get(selected_label, "Cosmic Sky")
        globals.theme_var.set(theme_name)

    label_var.trace("w", update_theme_var)

    initial_theme = globals.theme_var.get()
    initial_label = next((label for label, theme in label_to_theme.items() if theme == initial_theme), "Cosmic Sky")
    label_var.set(initial_label)

    ctk.CTkLabel(theme_frame, text=None, image=globals.theme_icon).pack(side="left", padx=6, pady=0)

    ctk.CTkLabel(theme_frame, 
                text="Theme",
                font=fonts.heading_font).pack(side="left", padx=(0, 12))

    ctk.CTkComboBox(theme_frame,
        variable=label_var,
        values=theme_labels,
        state="readonly",
        width=150).pack(side="left")

    # Deletion Frame
    deletion_frame = ctk.CTkFrame(general_frame, bg_color="transparent", fg_color="transparent")
    deletion_frame.pack(fill="x", pady=10, padx=10)

    def delete_chats():
        root = tk.Tk()
        root.withdraw()
        answer = messagebox.askyesno(parent=root, 
                title="Delete Chats", 
                message= f"Are you sure you would like to delete all conversations?",
                icon="error")
        if answer:
            shutil.rmtree(load_data_path("local", "chats"))
            show_toast(globals, "Conversations deleted!")
        root.destroy()

    ctk.CTkLabel(deletion_frame, text=None, image=globals.delete_icon).pack(side="left", padx=6, pady=0)

    ctk.CTkLabel(deletion_frame, 
                text="Delete All Chats:",
                font=fonts.heading_font).pack(side="left", padx=(0, 12))

    delete_chats_button = ctk.CTkButton(deletion_frame,
                  text="Delete",
                  width=25,
                  command=lambda: delete_chats())
    delete_chats_button.configure(fg_color="#d62828", hover_color="#ff3b30")
    delete_chats_button.pack(side="left")

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(general_frame, bg_color="transparent", fg_color="transparent")
    save_button_frame.pack(pady=10)

    ctk.CTkButton(save_button_frame, 
               text="Save Settings", 
               command=lambda: save_all_settings(globals)).pack()
