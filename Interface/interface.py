# Interface/interface.py
import tkinter as tk
from tkinter import ttk
from Interface.settings_window import create_settings_tab
from Interface.chat_window import create_chat_tab
from Interface.models_window import create_models_tab
from themes import styles
from config import apply_theme

def create_interface(globals):
    """Creates the core GUI interface."""
    globals.root = tk.Tk()
    globals.root.title("Pearl")
    screen_width = globals.root.winfo_screenwidth()
    screen_height = globals.root.winfo_screenheight()
    x = (screen_width - 900) // 2
    y = (screen_height - 850) // 2
    globals.root.geometry(f"850x850+{x}+{y}")
    globals.root.minsize(width="750", height="675")

    # String Vars
    globals.chat_message = tk.StringVar()
    globals.chat_message.set("")

    # Configure styles
    style = ttk.Style()
    style.theme_use("clam")
    apply_theme(globals.active_theme)

    main_frame = ttk.Frame(globals.root)
    main_frame.pack(side="left", fill="both", expand=True)

    globals.notebook = ttk.Notebook(main_frame)
    globals.notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Initiate Tabs
    def create_tabs():
        """Initiates critical UI functionality."""
        globals.logging_var = tk.StringVar(value=globals.logging_level)
        globals.theme_var = tk.StringVar(value=globals.active_theme)
        globals.tts_var = tk.BooleanVar(value=globals.tts_enabled)
        globals.active_voice_var = tk.StringVar(value=globals.active_voice)
        globals.tts_source_var = tk.StringVar(value=globals.tts_source)
        globals.save_chats_var = tk.BooleanVar(value=globals.save_chats)

        create_chat_tab(globals)
        create_models_tab(globals)
        create_settings_tab(globals)
    
    create_tabs()