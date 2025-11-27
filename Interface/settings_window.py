# Interface/settings_window.py
from tkinter import ttk, messagebox
import logging
import config

def create_settings_tab(globals):
    """Creates the settings tab and initializes widgets."""
    settings_frame = ttk.Frame(globals.notebook)
    globals.notebook.add(settings_frame, text="Settings")

    ttk.Label(settings_frame, 
             text="App Settings", 
             style="TLabel").pack(pady=20, fill="x", anchor="center", padx=10)

    # Theme Frame
    theme_frame = ttk.Frame(settings_frame)
    theme_frame.pack(fill="x", pady=10, padx=10)

    ttk.Label(theme_frame, 
    text="Theme:",
    style="TLabel").pack(side="left", padx=(0, 12))

    ttk.Combobox(theme_frame,
        textvariable=globals.theme_var,
        values=["cosmic_sky", "pastel_green"],
        style="TCombobox",
        state="readonly",
        width=18).pack(side="left")
    
    advanced_frame = ttk.Frame(settings_frame)
    advanced_frame.pack(anchor="w", pady=5)

    ttk.Label(advanced_frame, 
             text="Logging Level:", 
             style="TLabel").grid(row=1, column=0, padx=5, sticky="w")
    
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    col = 1
    for level in levels:
        ttk.Radiobutton(advanced_frame, 
                       text=level, 
                       value=level, 
                       variable=globals.logging_var, 
                       style="TRadiobutton").grid(row=1, column=col, padx=5, sticky="w")
        col += 1

    # Save Button Frame
    save_button_frame = ttk.Frame(settings_frame)
    save_button_frame.pack(pady=10)

    ttk.Button(save_button_frame, 
               text="Save Settings", 
               command=lambda: save_all_settings(globals), 
               style="TButton").pack()

def save_all_settings(globals):
    """
    Save all settings to JSON files and update globals.

    Args:
        globals (Globals): The global configuration object containing UI variables and settings.
    """

    # Load current settings to get saved_logging_level and current dev_mode
    settings = config.load_settings()
    current_logging_level = globals.logging_var.get()
    saved_logging_level = settings.get("saved_logging_level", "INFO")
    current_active_theme = globals.theme_var.get()

    # Handle logging level based on dev mode change
    logging_level = current_logging_level
    saved_logging_level = current_logging_level  # Update saved_logging_level to match

    # Save settings with updated logging levels
    config.save_settings(
    logging_level=logging_level,
    saved_logging_level=saved_logging_level,
    active_theme=current_active_theme)
    
    # Reload settings to update globals
    settings = config.load_settings()
    globals.logging_var.set(settings["logging_level"])
    globals.theme_var.set(settings["active_theme"])

    # Update logging
    logging.root.setLevel(getattr(logging, settings["logging_level"]))

    # Apply new theme
    config.apply_theme(current_active_theme)

    messagebox.showinfo("Settings Saved", "Settings saved successfully.")
    logging.info(f"Settings saved successfully.")