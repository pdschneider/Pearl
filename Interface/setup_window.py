# Interface/setup_window.py
import webbrowser
import customtkinter as ctk
from tktooltip import ToolTip
import Utils.fonts as fonts

def create_setup_tab(globals, setup_tab):
    """
    Creates the tab to display setup instructions for new users.

            Parameters:
                    globals: Global variables
                    setup_tab: The main frame of the setup window
    """
    setup_frame = ctk.CTkFrame(setup_tab)
    setup_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Ollama Frame
    ollama_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    ollama_frame.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(ollama_frame, 
                text="Installation Instructions", 
                font=fonts.title_font,
                anchor="center").pack(fill="x", pady=20, padx=10)

    ctk.CTkLabel(ollama_frame, 
                 justify="center", 
                 text=f"To use Pearl's chat feature, Ollama must be installed.\n\n" \
                        f"Head to https://ollama.com/download and follow the instructions for your OS.\n\n" \
                        f"After installing Ollama, you'll need to also download a compatible model.\n\n" \
                        f"There are many models to choose from,\nbut the recommended starting model is " \
                        f"llama3.2:latest.\n\n" \
                        f"Find models here: https://ollama.com/search\n\n" \
                        f"Have fun!").pack(fill="both", expand=True, padx=10, pady=10)

    # Ollama Buttons
    ollama_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    ollama_buttons_frame.pack(padx=10, pady=10)

    ollama_download_button = ctk.CTkButton(ollama_buttons_frame, 
                  text="Download Ollama", 
                  state=globals.ollama_download_state,
                  command= lambda: webbrowser.open("https://ollama.com/download"))
    ollama_download_button.grid(row=0, column=0, padx=5, sticky="ew")

    models_download_button = ctk.CTkButton(ollama_buttons_frame, 
                    state="normal",
                    text="Download Models", 
                    command= lambda: webbrowser.open("https://ollama.com/search"))
    models_download_button.grid(row=0, column=2, padx=5, sticky="ew")

    # Kokoro Frame
    kokoro_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    kokoro_frame.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(kokoro_frame, 
                 justify="center", 
                 text=f"For enhanced Text to Speech, you may install Kokoro (this is optional).\n\n" \
                        f"Head to https://github.com/remsky/Kokoro-FastAPI and follow the instructions for your OS.\n\n" \
                        f"After installing Kokoro, you'll need to also install and set up Docker.\n\n").pack(fill="both", expand=True, padx=10, pady=10)

    # Kokoro Buttons
    kokoro_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    kokoro_buttons_frame.pack(padx=10, pady=10)

    kokoro_download_button = ctk.CTkButton(kokoro_buttons_frame, 
                  text="Download Kokoro", 
                  state=globals.kokoro_download_state,
                  command= lambda: webbrowser.open("https://github.com/remsky/Kokoro-FastAPI"))
    kokoro_download_button.grid(row=0, column=0, padx=5, sticky="ew")

    docker_download_button = ctk.CTkButton(kokoro_buttons_frame, 
                text="Download Docker", 
                command= lambda: webbrowser.open("https://www.docker.com/get-started/"))
    docker_download_button.grid(row=0, column=1, padx=5, sticky="ew")
 
    # Buttons Frame
    buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    buttons_frame.pack(fill="x", padx=10, pady=10)

    ctk.CTkButton(buttons_frame, 
                text="Continue", 
                command= lambda: continue_to_chat()).pack(padx=5, pady=5)

    def refresh_button_states():
        """Refreshes button states and adds/removes tooltips"""
        if globals.ollama_active:
            globals.ollama_download_state = "disabled"
            globals.ollama_download_tooltip = ToolTip(ollama_download_button, msg="Ollama already installed!", delay=0.3, follow=True, fg="white", bg="gray20", padx=10, pady=5)
        else:
            globals.ollama_download_state = "normal"
            globals.ollama_download_tooltip = None
        if globals.kokoro_active:
            globals.kokoro_download_state = "disabled"
            globals.kokoro_download_tooltip = ToolTip(kokoro_download_button, msg="Kokoro already installed!", delay=0.3, follow=True, fg="white", bg="gray20", padx=10, pady=5)
        else:
            globals.kokoro_download_state = "normal"
            globals.kokoro_download_tooltip = None

    refresh_button_states()

    def continue_to_chat():
        """Forgets setup and settings pages to return the user to a clean chat page"""
        globals.settings_overlay.pack_forget()
        globals.setup_page.pack_forget()
        globals.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
