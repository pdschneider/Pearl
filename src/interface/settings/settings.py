# Interface/Settings/settings.py
import customtkinter as ctk
from src.interface.settings.general_settings import create_general_settings_tab
from src.interface.settings.model_settings import create_models_tab
from src.interface.settings.sound_settings import create_sound_tab
from src.interface.settings.about_settings import create_about_tab
from src.interface.settings.advanced_settings import create_advanced_tab
from src.interface.settings.network_settings import create_networking_tab


def create_settings(globs, settings_frame):
    """
    Creates the settings tab and initializes widgets.

            Parameters:
                    globs: Global variables
                    settings_frame: The main frame which
                    holds the settings Tabview
    """

    # Notebook tabs for settings
    globs.settings_notebook = ctk.CTkTabview(settings_frame)
    globs.settings_notebook.pack(fill="both", expand=True, padx=20, pady=20)

    def create_settings_tabs():
        """Initiates the settings Tabview and passes global variables."""
        general_tab = globs.settings_notebook.add("General")
        models_tab = globs.settings_notebook.add("Models")
        speech_tab = globs.settings_notebook.add("Sound")
        networking_tab = globs.settings_notebook.add("Networking")
        advanced_tab = globs.settings_notebook.add("Advanced")
        about_tab = globs.settings_notebook.add("About")
        create_general_settings_tab(globs, general_tab)
        create_models_tab(globs, models_tab)
        create_sound_tab(globs, speech_tab)
        create_networking_tab(globs, networking_tab)
        create_advanced_tab(globs, advanced_tab)
        create_about_tab(globs, about_tab)

    create_settings_tabs()
