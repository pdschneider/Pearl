# Interface/Settings/advanced_settings.py
import customtkinter as ctk
from Utils.save_settings import save_all_settings
import Utils.fonts as fonts

def create_advanced_tab(globals, advanced_frame):
    """
    Creates the advanced tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    about_frame: The main frame of the about tab
    """

    ctk.CTkLabel(advanced_frame, 
             text="Advanced Settings", 
             font=fonts.title_font,
             anchor="center").pack(fill="x", pady=20, padx=10)

    # Options Frame
    options_frame = ctk.CTkFrame(advanced_frame, bg_color="transparent", fg_color="transparent")
    options_frame.pack(anchor="w", pady=5)

    ctk.CTkLabel(options_frame, 
             text="Logging Level:").grid(row=2, column=0, padx=5, sticky="w")

    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    col = 1
    for level in levels:
        ctk.CTkRadioButton(options_frame, 
                       text=level, 
                       value=level, 
                       variable=globals.logging_var).grid(row=2, column=col, padx=5, sticky="w")
        col += 1

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(advanced_frame, bg_color="transparent", fg_color="transparent")
    save_button_frame.pack(pady=10)

    ctk.CTkButton(save_button_frame, 
               text="Save Settings", 
               command=lambda: save_all_settings(globals)).pack()
