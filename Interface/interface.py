# Interface/interface.py
import tkinter as tk
import customtkinter as ctk
import logging
from Interface.Settings.settings import create_settings
from Interface.chat_window import create_chat_tab
from Interface.Components.top_bar import create_top_bar
from Interface.Setup.setup_window import create_setup_tab
from Interface.Components.sidebar import create_sidebar
from Interface.changelog import create_changelog_tab
from Utils.load_settings import load_data_path
from config import apply_theme
from Utils.vars import create_vars


def create_interface(globals):
    """
    Creates the core GUI interface.

            Parameters:
                    globals: Global variables
    """
    # Set up main window
    logging.debug(f"Building GUI...")
    globals.root.withdraw()
    globals.root.title("Pearl")

    def draw_window():
        screen_width = globals.root.winfo_screenwidth()
        screen_height = globals.root.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 850) // 2
        globals.root.geometry(f"900x850+{x}+{y}")

    if globals.saved_width and globals.saved_height and globals.saved_x and globals.saved_y:
        try:
            globals.root.geometry(
                f"{globals.saved_width}x{globals.saved_height}+{globals.saved_x}+{globals.saved_y}")
        except:
            draw_window()
    else:
        draw_window()

    globals.root.minsize(width=750, height=675)

    # Get Icon
    try:
        globals.icon = load_data_path("config", "assets/Pearl_Sparkle.png")
        icon_image = tk.PhotoImage(file=str(globals.icon))
        globals.root.iconphoto(False, icon_image)
    except Exception as e:
        logging.warning(f"Failed to load icon at {globals.icon}")

    # String Vars
    globals.chat_message = tk.StringVar()
    globals.chat_message.set("")

    # Configure theme
    apply_theme(globals.active_theme)
    globals.root.configure(fg_color=globals.theme_dict["CTkFrame"]["fg_color"])

    # Add Navigation
    create_top_bar(globals)
    create_sidebar(globals)

    # Main Frame
    globals.main_frame = ctk.CTkFrame(globals.root)
    globals.main_frame.pack(side="left", fill="both", expand=True)

    # Window Frames
    globals.settings_page = ctk.CTkFrame(globals.main_frame)
    globals.changelog = ctk.CTkFrame(globals.main_frame)
    globals.chat_page = ctk.CTkFrame(globals.main_frame)
    globals.setup_page = ctk.CTkFrame(globals.main_frame)

    globals.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
    if not globals.ollama_active:
        globals.chat_page.pack_forget()
        globals.app_title.configure(text="Welcome to Pearl!")

    globals.setup_page.pack(fill="both", expand=True, padx=10, pady=0)
    if globals.ollama_active:
        globals.setup_page.pack_forget()
        globals.app_title.configure(text="Pearl at your service!")

    globals.changelog.pack_forget()
    globals.settings_page.pack_forget()

    # Initiate Tabs
    def create_tabs():
        """Initiates critical UI functionality."""
        create_vars(globals)

        # Create tabs
        create_chat_tab(globals, globals.chat_page)
        create_settings(globals, globals.settings_page)
        create_setup_tab(globals, globals.setup_page)
        create_changelog_tab(globals, globals.changelog)

        # Display window after widgets have built
        globals.root.after(1500, lambda: [  # 1.5 seconds
        globals.root.update_idletasks(),
        globals.root.deiconify(),
        globals.root.focus_set()
    ])

    # Create tabs then show the window
    create_tabs()
