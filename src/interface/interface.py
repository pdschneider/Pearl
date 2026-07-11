# Interface/interface.py
import tkinter as tk
import customtkinter as ctk
import logging
from src.interface.settings.settings import create_settings
from src.interface.chat_window import create_chat_tab
from src.interface.components.top_bar import create_top_bar
from src.interface.setup.setup_window import create_setup_tab
from src.interface.components.sidebar import create_sidebar
from src.interface.changelog import create_changelog_tab
from src.utils.load import load_data_path
from config import apply_theme
from src.utils.vars import create_vars


def create_interface(globs):
    """
    Creates the core GUI interface.

            Parameters:
                    globs: Global variables
    """
    # Set up main window
    logging.debug(f"Building GUI...")
    globs.root.withdraw()
    globs.root.title("Pearl")

    # Kill startup window if still present
    if globs.startup_root:
        globs.startup_root.quit()
        globs.startup_root.destroy()

    def draw_window():
        screen_width = globs.root.winfo_screenwidth()
        screen_height = globs.root.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 850) // 2
        globs.root.geometry(f"900x850+{x}+{y}")

    if globs.saved_width and globs.saved_height and globs.saved_x and globs.saved_y:
        try:
            globs.root.geometry(
                f"{globs.saved_width}x{globs.saved_height}+{globs.saved_x}+{globs.saved_y}")
        except:
            draw_window()
    else:
        draw_window()

    globs.root.minsize(width=750, height=675)

    # Get Icon
    try:
        globs.icon = load_data_path("config", "assets/Pearl_Sparkle.png")
        icon_image = tk.PhotoImage(file=str(globs.icon))
        globs.root.iconphoto(False, icon_image)
    except Exception as e:
        logging.warning(f"Failed to load icon at {globs.icon}")

    # String Vars
    globs.chat_message = tk.StringVar()
    globs.chat_message.set("")

    # Configure theme
    apply_theme(globs.active_theme)
    globs.root.configure(fg_color=globs.theme_dict["CTkFrame"]["fg_color"])

    # Add Navigation
    create_top_bar(globs)
    create_sidebar(globs)

    # Main Frame
    globs.main_frame = ctk.CTkFrame(globs.root)
    globs.main_frame.pack(side="left", fill="both", expand=True)

    # Window Frames
    globs.settings_page = ctk.CTkFrame(globs.main_frame)
    globs.changelog = ctk.CTkFrame(globs.main_frame)
    globs.chat_page = ctk.CTkFrame(globs.main_frame)
    globs.setup_page = ctk.CTkFrame(globs.main_frame)

    globs.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
    if not globs.ollama_active:
        globs.chat_page.pack_forget()
        globs.app_title.configure(text="Welcome to Pearl!")

    globs.setup_page.pack(fill="both", expand=True, padx=10, pady=0)
    if globs.ollama_active:
        globs.setup_page.pack_forget()
        globs.app_title.configure(text="Pearl at your service!")

    globs.changelog.pack_forget()
    globs.settings_page.pack_forget()

    # Initiate Tabs
    def create_tabs():
        """Initiates critical UI functionality."""
        create_vars(globs)

        # Create tabs
        create_chat_tab(globs, globs.chat_page)
        create_settings(globs, globs.settings_page)
        create_setup_tab(globs, globs.setup_page)
        create_changelog_tab(globs, globs.changelog)

        # Display window after widgets have built
        globs.root.after(1500, lambda: [  # 1.5 seconds
        globs.root.update_idletasks(),
        globs.root.deiconify(),
        globs.root.focus_set()])

    # Create tabs then show the window
    create_tabs()
