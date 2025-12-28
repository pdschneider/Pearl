# Interface/model_settings.py
import logging, time
from tkinter import messagebox
import customtkinter as ctk
from CTkToolTip import CTkToolTip
from Connections.ollama import get_all_models, get_loaded_models, load_model
from Utils.hardware import get_ram_info
from config import save_settings
from Interface.Components.selector import Treeview

def create_models_tab(globals, models_frame):
    """
    Creates the Models tab frame and initializes widgets.

            Parameters:
                    globals: Global variables
                    models_frame: The main frame of the models settings tab
    """

    model_selector = Treeview(globals, models_frame, get_dir=lambda: get_all_models())

    def load_selected():
        """Loads selected model into memory"""
        logging.debug(f"Initiating model load...")
        available_ram = get_ram_info()
        sel = model_selector.selection()
        if not sel:
            logging.warning(f"No model selected.")
            return
        if available_ram != {}:
            if available_ram["avail_ram_gb"] < 1.0:
                logging.warning(f"Cannot load models with less than 1GB of available RAM.")
                messagebox.showerror(title="Not Enough RAM",
                                    message="Must have more than 1GB of available RAM to load models.",
                                    parent=models_frame,)
                return
            model_name = sel[0]
            if model_name not in get_loaded_models():
                logging.debug(f"Attempting to load {model_name}...")
                load_model(model_name)
                time.sleep(2)
                refresh_tree()
            else:
                logging.debug(f"{model_name} is already loaded!")

    def set_selected():
        """Sets selected model as active model"""
        logging.debug(f"Attempting to select model...")
        sel = model_selector.selection()
        if not sel:
            logging.warning(f"No model selected.")
            return
        available_ram = get_ram_info()
        model_name = sel[0]
        if available_ram != {}:
            if available_ram["avail_ram_gb"] < 1.0 and model_name not in get_loaded_models():
                logging.warning(f"Cannot load models with less than 1GB of available RAM.")
                messagebox.showerror(title="Not Enough RAM",
                                    message="Must have more than 1GB of available RAM to load models.",
                                    parent=models_frame,)
                return
        if globals.active_model != model_name:
            globals.active_model = model_name
            save_settings(active_model=model_name)
            if model_name not in get_loaded_models():
                load_selected()
                time.sleep(2)
                refresh_tree()
        else:
            logging.debug(f"{globals.active_model} is already the selected model.")
    
    def set_context():
        """Sets the context model for context detection and more."""
        logging.debug(f"Attempting to select context model...")
        sel = model_selector.selection()
        if not sel:
            logging.warning(f"No model selected.")
            return
        available_ram = get_ram_info()
        model_name = sel[0]
        if available_ram != {}:
            if available_ram["avail_ram_gb"] < 1.0 and model_name not in get_loaded_models():
                logging.warning(f"Cannot load models with less than 1GB of available RAM.")
                messagebox.showerror(title="Not Enough RAM",
                                    message="Must have more than 1GB of available RAM to load models.",
                                    parent=models_frame,)
                return
        if globals.context_model != model_name:
            globals.context_model = model_name
            save_settings(context_model=model_name)
            if model_name not in get_loaded_models():
                load_selected()
                time.sleep(2)
                refresh_tree()
        else:
            logging.debug(f"{globals.context_model} is already the context model.")


    # Buttons
    buttons_frame = ctk.CTkFrame(models_frame, bg_color="transparent", fg_color="transparent")
    buttons_frame.pack(padx=5, pady=5)

    load_button = ctk.CTkButton(buttons_frame, text="Load", command=load_selected)
    load_button.grid(row=0, column=0, padx=5)
    CTkToolTip(load_button, message="Loads a model\n into memory", delay=1.0, follow=True, padx=10, pady=5)
    select_button = ctk.CTkButton(buttons_frame, text="Select", command=set_selected)
    select_button.grid(row=0, column=1, padx=5)
    CTkToolTip(select_button, message="Selects a model\n to be used", delay=1.0, follow=True, padx=10, pady=5)
    context_button = ctk.CTkButton(buttons_frame, text="Set Context Model", command=set_context)
    context_button.grid(row=0, column=2, padx=5)
    CTkToolTip(context_button, message="Selects the context model\n which is used for dynamic\n prompt switching and more", delay=1.0, follow=True, padx=10, pady=5)

    def refresh_tree():
        if globals.ollama_active:
            try:
                model_selector.refresh()
            except Exception as e:
                logging.error(f"Could not refresh tree due to: {e}.")

    refresh_tree()
