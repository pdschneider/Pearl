# Utils/startup.py
import logging, threading
import tkinter as tk
import customtkinter as ctk
from Connections.ollama import ollama_test, load_model, get_loaded_models
from Managers.sound_manager import kokoro_test
from Utils.hardware import get_hardware_stats

def startup(globals):
    """
    Starts up the program with a progress bar.
    
            Parameters:
                    globals: Global variables
    """
    tasks_done = threading.Event()

    def startup_tasks(globals, tasks_done):
        """Tests dependencies and sets flags."""
        try:
            ollama_success = ollama_test()
            if ollama_success:
                globals.ollama_active = True
                loaded_models = get_loaded_models()
                if globals.active_model not in loaded_models:
                    logging.debug(f"Attempting to load initial model....")
                    load_model(globals.active_model)  # Loads the active model before startup
            kokoro_success = kokoro_test()
            if kokoro_success:
                globals.kokoro_active = True
        except:
            logging.error(f"Initial Ollama/Kokoro setup failed.")

        # Query for hardware stats
        try:
            get_hardware_stats()
        except Exception as e:
            logging.warning(f"Hardware stats query failed due to: {e}")

        tasks_done.set()

    # Perform startup tasks
    thread = threading.Thread(target=startup_tasks, args=(globals, tasks_done), daemon=True)
    thread.start()

    # Wait up to 1 second for quick completion
    thread.join(1.0)
    if tasks_done.is_set():
        return

    # Create the loading window
    globals.startup_root = ctk.CTk()
    globals.startup_root.title("Loading Pearl...")
    globals.startup_root.geometry("300x100")

    # Create progress bar
    progress_bar = ctk.CTkProgressBar(globals.startup_root, mode="indeterminate")
    progress_bar.pack(padx=10, pady=10, fill="x")
    progress_bar.start()

    # Callback to destroy the window when tasks are done
    def close_startup_window():
        """Closes the progress bar window."""
        progress_bar.stop()
        globals.startup_root.destroy()
        globals.startup_root = None

    def check_if_done():
        """Periodically checks to see if loading is finished."""
        if tasks_done.is_set():
            close_startup_window()
        else:
            globals.startup_root.after(100, check_if_done)

    # Set up polling loop
    globals.startup_root.after(100, check_if_done)

    # Destroy loading screen
    try:
        globals.startup_root.mainloop()
    except tk.TclError:
        pass  #  Ignores callback errors
