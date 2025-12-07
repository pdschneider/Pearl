# Interface/Settings/settings.py
import customtkinter as ctk
from Interface.Settings.general_settings import create_general_settings_tab
from Interface.Settings.model_settings import create_models_tab
from Interface.Settings.speech_settings import create_speech_tab
from Interface.Settings.about_settings import create_about_tab

def create_settings(globals, settings_frame):
    """
    Creates the settings tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    settings_frame: The main frame which holds the settings Tabview
    """

    # Notebook tabs for settings
    globals.settings_notebook = ctk.CTkTabview(settings_frame)
    globals.settings_notebook.pack(fill="both", expand=True, padx=20, pady=20)

    def create_settings_tabs():
        """Initiates the settings Tabview and passes global variables."""
        general_tab = globals.settings_notebook.add("General")
        models_tab = globals.settings_notebook.add("Models")
        speech_tab = globals.settings_notebook.add("Speech")
        about_tab = globals.settings_notebook.add("About")
        create_general_settings_tab(globals, general_tab)
        create_models_tab(globals, models_tab)
        create_speech_tab(globals, speech_tab)
        create_about_tab(globals, about_tab)

    create_settings_tabs()
