# Interface/interface.py
import tkinter as tk
import customtkinter as ctk
from Interface.Settings.settings import create_settings
from Interface.chat_window import create_chat_tab
from Interface.Components.top_bar import create_top_bar
from Interface.setup_window import create_setup_tab
from Interface.Components.sidebar import create_sidebar
from Interface.changelog import create_changelog_tab
from config import apply_theme, get_data_path

def create_interface(globals):
    """
    Creates the core GUI interface.

            Parameters:
                    globals: Global variables
    """
    # Set up main window
    globals.root = ctk.CTk()
    globals.root.title("Pearl")
    screen_width = globals.root.winfo_screenwidth()
    screen_height = globals.root.winfo_screenheight()
    x = (screen_width - 900) // 2
    y = (screen_height - 850) // 2
    globals.root.geometry(f"850x850+{x}+{y}")
    globals.root.minsize(width=750, height=675)

    # Get Icon
    globals.icon = get_data_path("config", "assets/Pearl_Sparkle.png")
    icon_image = tk.PhotoImage(file=str(globals.icon))
    globals.root.iconphoto(False, icon_image)

    # String Vars
    globals.chat_message = tk.StringVar()
    globals.chat_message.set("")

    # Configure theme
    apply_theme(globals.active_theme)

    # Add Navigation
    create_top_bar(globals)
    create_sidebar(globals)

    # Main Frame
    globals.main_frame = ctk.CTkFrame(globals.root)
    globals.main_frame.pack(side="left", fill="both", expand=True)

    # Window Frames
    globals.settings_overlay = ctk.CTkFrame(globals.main_frame)
    globals.settings_overlay.pack_forget()

    globals.chat_page = ctk.CTkFrame(globals.main_frame)
    globals.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
    if not globals.ollama_active:
        globals.chat_page.pack_forget()

    globals.setup_page = ctk.CTkFrame(globals.main_frame)
    globals.setup_page.pack(fill="both", expand=True, padx=10, pady=0)
    if globals.ollama_active:
        globals.setup_page.pack_forget()

    globals.changelog = ctk.CTkFrame(globals.main_frame)
    globals.changelog.pack_forget()

    # Initiate Tabs
    def create_tabs():
        """Initiates critical UI functionality."""
        globals.logging_var = tk.StringVar(value=globals.logging_level)
        globals.theme_var = tk.StringVar(value=globals.active_theme)
        globals.tts_var = tk.BooleanVar(value=globals.tts_enabled)
        globals.active_voice_var = tk.StringVar(value=globals.active_voice)
        globals.tts_source_var = tk.StringVar(value=globals.tts_source)
        globals.save_chats_var = tk.BooleanVar(value=globals.save_chats)
        globals.sink_var = tk.StringVar(value=globals.default_sink)

        create_chat_tab(globals, globals.chat_page)
        create_settings(globals, globals.settings_overlay)
        create_setup_tab(globals, globals.setup_page)
        create_changelog_tab(globals, globals.changelog)

    create_tabs()
