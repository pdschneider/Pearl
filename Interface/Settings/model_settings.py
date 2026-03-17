# Interface/model_settings.py
import logging
import time
import customtkinter as ctk
from CTkToolTip import CTkToolTip
from Connections.ollama import get_all_models, get_loaded_models, load_model
from Utils.hardware import get_ram_info
from Utils.save_settings import save_settings
from Utils.toast import show_toast
from Interface.Components.selector import Treeview
from PySide6.QtWidgets import QMessageBox


def create_models_tab(globals, models_frame):
    """
    Creates the Models tab frame and initializes widgets.

            Parameters:
                    globals: Global variables
                    models_frame: The main frame of the models settings tab
    """

    model_selector = Treeview(globals,
                              models_frame,
                              get_dir=lambda: get_all_models(globals, globals.ollama_chat_path))

    def load_selected(globals):
        """Loads selected model into memory"""
        logging.debug(f"Initiating model load...")
        available_ram = get_ram_info()
        sel = model_selector.selection()

        # Return if no model is selected
        if not sel:
            logging.warning(f"No model selected.")
            return

        if available_ram != {}:
            # Return early with a warning if RAM is less than 1GB
            if available_ram["avail_ram_gb"] < 1.0:
                logging.warning(
                    f"Cannot load models with less than 1GB of available RAM.")
                # Display a messagebox letting the user know they need more RAM
                QMessageBox.warning(
                    None,
                    "Not Enough RAM",
                    f"You must have at least 1GB of available RAM to load models.",
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok)
                return

            model_name = sel[0]
            if model_name not in get_loaded_models(globals, globals.ollama_chat_path):
                logging.debug(f"Attempting to load {model_name}...")
                load_model(globals, model_name)
                time.sleep(2)
                refresh_tree()
            else:
                logging.debug(f"{model_name} is already loaded!")

    def set_selected(globals):
        """Sets selected model as active model"""
        logging.debug(f"Attempting to select model...")
        sel = model_selector.selection()

        # Returns early if nothing selected
        if not sel:
            logging.warning(f"No model selected.")
            return

        available_ram = get_ram_info()
        model_name = sel[0]

        # Display a warning letting the user know they need more available RAM
        if available_ram != {}:
            if available_ram["avail_ram_gb"] < 1.0 and model_name not in get_loaded_models(globals, globals.ollama_chat_path):
                logging.warning(
                    f"Cannot load models with less than 1GB of available RAM.")
                QMessageBox.warning(
                    None,
                    "Not Enough RAM",
                    f"You must have more than 1GB of available RAM to load models.",
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok)
                return

        # Set chosen model as active model and save settings
        if globals.active_model != model_name:
            globals.active_model = model_name
            save_settings(active_model=model_name)
            show_toast(globals, message=f"{model_name} set as active model")

            # Sleep for 2 seconds, then refresh, ensuring model is loaded
            if model_name not in get_loaded_models(globals, globals.ollama_chat_path):
                load_selected(globals)
                time.sleep(2)
                refresh_tree()
        else:
            logging.debug(
                f"{globals.active_model} is already the selected model.")

    def set_context(globals):
        """Sets the model for context detection."""
        logging.debug(f"Attempting to select context model...")
        sel = model_selector.selection()

        # Return early of no model is selected
        if not sel:
            logging.warning(f"No model selected.")
            return

        available_ram = get_ram_info()
        model_name = sel[0]

        # Display a warning letting the user know they need more RAM
        if available_ram != {}:
            if available_ram["avail_ram_gb"] < 1.0 and model_name not in get_loaded_models(globals, globals.ollama_chat_path):
                logging.warning(
                    f"Cannot load models with less than 1GB of available RAM.")
                QMessageBox.warning(
                    None,
                    "Not Enough RAM",
                    f"You must have more than 1GB of available RAM to load models.",
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok)
                return

        # Set chosen model as context model and save settings
        if globals.context_model != model_name:
            globals.context_model = model_name
            save_settings(context_model=model_name)
            show_toast(globals, message=f"{model_name} set as context model")

            # Sleep for 2 seconds, then refresh, ensuring model is loaded
            if model_name not in get_loaded_models(globals, globals.ollama_chat_path):
                load_selected(globals)
                time.sleep(2)
                refresh_tree()
        else:
            logging.debug(
                f"{globals.context_model} is already the context model.")
    
    def set_title_gen(globals):
        """Sets the model for generating titles."""
        logging.debug(f"Attempting to select title gen model...")
        sel = model_selector.selection()

        # Return early of no model is selected
        if not sel:
            logging.warning(f"No model selected.")
            return

        available_ram = get_ram_info()
        model_name = sel[0]

        # Display a warning letting the user know they need more RAM
        if available_ram != {}:
            if available_ram["avail_ram_gb"] < 1.0 and model_name not in get_loaded_models(globals, globals.ollama_chat_path):
                logging.warning(
                    f"Cannot load models with less than 1GB of available RAM.")
                QMessageBox.warning(
                    None,
                    "Not Enough RAM",
                    f"You must have more than 1GB of available RAM to load models.",
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok)
                return

        # Set chosen model as context model and save settings
        if globals.title_gen_model != model_name:
            globals.title_gen_model = model_name
            save_settings(title_gen_model=model_name)
            show_toast(globals, message=f"{model_name} set as title generation model")

            # Sleep for 2 seconds, then refresh, ensuring model is loaded
            if model_name not in get_loaded_models(globals, globals.ollama_chat_path):
                load_selected(globals)
                time.sleep(2)
                refresh_tree()
        else:
            logging.debug(
                f"{globals.title_gen_model} is already the title generation model.")

    # Buttons
    buttons_frame = ctk.CTkFrame(models_frame,
                                 bg_color="transparent",
                                 fg_color="transparent")
    buttons_frame.pack(padx=5, pady=5)

    # Load button
    load_button = ctk.CTkButton(buttons_frame,
                                text="Load",
                                command=lambda: load_selected(globals))
    load_button.grid(row=0, column=0, padx=5)
    CTkToolTip(load_button,
               message="Loads a model\n into memory",
               delay=1.0,
               follow=True,
               padx=10,
               pady=5)
    
    # Select button
    select_button = ctk.CTkButton(buttons_frame,
                                  text="Select Chats Model",
                                  command=lambda: set_selected(globals))
    select_button.grid(row=0, column=1, padx=5)
    CTkToolTip(select_button,
               message="Selects a model\n to be used",
               delay=1.0,
               follow=True,
               padx=10,
               pady=5)
    
    # Context set button
    context_button = ctk.CTkButton(buttons_frame,
                                   text="Set Context Model",
                                   command=lambda: set_context(globals))
    context_button.grid(row=0, column=2, padx=5)
    CTkToolTip(context_button,
               message="Selects the context model\n which is used for dynamic\n prompt switching",
               delay=1.0,
               follow=True,
               padx=10,
               pady=5)
    
    # Title Generation set button
    title_gen_button = ctk.CTkButton(buttons_frame,
                                   text="Set Title Gen Model",
                                   command=lambda: set_title_gen(globals))
    title_gen_button.grid(row=0, column=3, padx=5)
    CTkToolTip(title_gen_button,
               message="Selects the model\n which is used for\n generating titles",
               delay=1.0,
               follow=True,
               padx=10,
               pady=5)

    def refresh_tree():
        if globals.ollama_active:
            try:
                model_selector.refresh()
            except Exception as e:
                logging.error(f"Could not refresh tree due to: {e}.")

    refresh_tree()
