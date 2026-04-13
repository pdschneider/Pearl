# Interface/Settings/network_settings.py
import customtkinter as ctk
import src.utils.fonts as fonts
from src.utils.save_settings import save_all_settings, save_settings


def create_networking_tab(globals, networking_frame):
    """
    Creates the about tab and initializes widgets.

            Parameters:
                    globals: Global variables
                    networking_frame: The main frame of the networking tab
    """

    ctk.CTkLabel(networking_frame,
                 text="Networking",
                 font=fonts.title_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)

    # Chats path selection
    chats_frame = ctk.CTkFrame(networking_frame, fg_color="transparent")
    chats_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(chats_frame,
                 text="Chats: ",
                 font=fonts.body_font).pack(side="left", padx=6, pady=0)
    
    ctk.CTkEntry(chats_frame,
                 placeholder_text="http://localhost:11434/",
                 width=200,
                 textvariable=globals.ollama_chat_path_var).pack(side="left", padx=6, pady=0)
    
    ctk.CTkButton(chats_frame,
                  text="Restore Default",
                  command=lambda: restore_localhost(globals, "chat")).pack(side="left", padx=6, pady=0)

    # Context path selection
    context_chats_frame = ctk.CTkFrame(networking_frame, fg_color="transparent")
    context_chats_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(context_chats_frame,
                 text="Context Detection: ",
                 font=fonts.body_font).pack(side="left", padx=6, pady=0)
    
    ctk.CTkEntry(context_chats_frame,
                 placeholder_text="http://localhost:11434/",
                 width=200,
                 textvariable=globals.ollama_context_path_var).pack(side="left", padx=6, pady=0)
    
    ctk.CTkButton(context_chats_frame,
                  text="Restore Default",
                  command=lambda: restore_localhost(globals, "context")).pack(side="left", padx=6, pady=0)
    
    # Title path selection
    title_chats_frame = ctk.CTkFrame(networking_frame, fg_color="transparent")
    title_chats_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(title_chats_frame,
                 text="Chat Titles: ",
                 font=fonts.body_font).pack(side="left", padx=6, pady=0)
    
    ctk.CTkEntry(title_chats_frame,
                 placeholder_text="http://localhost:11434/",
                 width=200,
                 textvariable=globals.ollama_title_path_var).pack(side="left", padx=6, pady=0)
    
    ctk.CTkButton(title_chats_frame,
                  text="Restore Default",
                  command=lambda: restore_localhost(globals, "title")).pack(side="left", padx=6, pady=0)

    explanation_frame = ctk.CTkFrame(networking_frame, fg_color="transparent")
    explanation_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(master=explanation_frame,
                 text=
"""
Networking is an advanced feature which utilizes other computers on the Local Area Network (LAN)
to process AI tasks in parallel. This allows you to use one device for main chats while another
handles context detection and title generation, freeing up available resources for faster or more
powerful models to be used for the main chat while retaining full functionality.

This process requires setting up Ollama on the host computer as well as ensuring access via
your firewall.

If you do not know how to set up multiple computers for use with AI, you can simply ignore this
page and keep the default endpoints.
""",
                 font=fonts.body_font).pack(side="left", padx=6, pady=0)

    # Save Button Frame
    save_button_frame = ctk.CTkFrame(networking_frame,
                                     bg_color="transparent",
                                     fg_color="transparent")
    save_button_frame.pack(pady=10)

    ctk.CTkButton(save_button_frame,
                  text="Save Settings",
                  command=lambda: save_all_settings(globals)).pack()

    def restore_localhost(globals, type):
        """Restores the address to localhost."""
        if type == "chat":
            globals.ollama_chat_path_var.set("http://localhost:11434/")
            globals.ollama_chat_path = "http://localhost:11434/"
            save_settings(ollama_chat_path="http://localhost:11434/")
        elif type == "context":
            globals.ollama_context_path_var.set("http://localhost:11434/")
            globals.ollama_context_path = "http://localhost:11434/"
            save_settings(ollama_context_path="http://localhost:11434/")
        elif type == "title":
            globals.ollama_title_path_var.set("http://localhost:11434/")
            globals.ollama_title_path = "http://localhost:11434/"
            save_settings(ollama_title_path="http://localhost:11434/")
