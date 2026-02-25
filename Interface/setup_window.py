# Interface/setup_window.py
import webbrowser
import customtkinter as ctk
from tktooltip import ToolTip
import Utils.fonts as fonts
from Connections.ollama import ollama_installation, ollama_test


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
    ollama_frame.pack(fill="x", expand=False, padx=10, pady=10)

    ctk.CTkLabel(ollama_frame,
                 text="Welcome to Pearl!",
                 font=fonts.title_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)

    inner_width = 900
    ollama_text_container = ctk.CTkFrame(
        ollama_frame,
        width=inner_width,
        fg_color="transparent")
    ollama_text_container.pack(anchor="center", pady=5)

    ctk.CTkLabel(ollama_text_container,
                 justify="left",
                 anchor="w",
                 font=fonts.body_font,
                 text="""
                 Thank you for installing Pearl!\n
                 Pearl uses Ollama under the hood to generate text. Clicking the Interactive Install button below
                 will open an interactive terminal where you can install Ollama and your first model after entering
                 your root password (simple).

                 If preferred, you can also download Ollama from the Ollama website manually along with a starting model
                 using the links provided. The recommended starting model is llama3.2:latest (same process, more steps).
                 """).pack(fill="x", expand=True, padx=10, pady=10)

    # Ollama Buttons
    ollama_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    ollama_buttons_frame.pack(padx=10, pady=10, side="top")

    ollama_download_button = ctk.CTkButton(
        ollama_buttons_frame,
        text="Interactive Install",
        state="normal",
        command=lambda: ollama_installation(globals))
    ollama_download_button.grid(row=0, column=0, padx=5, sticky="ew")

    ollama_web_download_button = ctk.CTkButton(
        ollama_buttons_frame,
        text="Web Download",
        state="normal",
        command=lambda: webbrowser.open("https://ollama.com/download"))
    ollama_web_download_button.grid(row=0, column=1, padx=5, sticky="ew")

    models_download_button = ctk.CTkButton(
        ollama_buttons_frame,
        state="normal",
        text="Download Models",
        command=lambda: webbrowser.open("https://ollama.com/search"))
    models_download_button.grid(row=0, column=2, padx=5, sticky="ew")

    # Models tooltip
    models_tooltip = ToolTip(
        models_download_button,
        msg="https://ollama.com/search",
        delay=0.3,
        follow=True,
        fg="white",
        bg="gray20",
        padx=10,
        pady=5)

    # Kokoro Frame
    kokoro_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    kokoro_frame.pack(fill="x", expand=False, padx=10, pady=10)

    kokoro_text_container = ctk.CTkFrame(
        kokoro_frame,
        width=inner_width,
        fg_color="transparent")
    kokoro_text_container.pack(anchor="center", pady=5)

    ctk.CTkLabel(kokoro_text_container,
                 justify="left",
                 anchor="w",
                 text="""
                 For enhanced Text to Speech, you may also install Kokoro (this is optional).

                 First, click the Docker button to install Docker (a dependency of Kokoro), then
                 head to https://github.com/remsky/Kokoro-FastAPI and follow the instructions for your OS.
                 """).pack(
                     fill="both", expand=True, padx=10, pady=10)

    # Kokoro Buttons
    kokoro_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    kokoro_buttons_frame.pack(padx=10, pady=10)

    kokoro_download_button = ctk.CTkButton(
        kokoro_buttons_frame,
        text="Download Kokoro",
        state="normal",
        command=lambda: webbrowser.open(
            "https://github.com/remsky/Kokoro-FastAPI"))
    kokoro_download_button.grid(row=0, column=0, padx=5, sticky="ew")

    docker_download_button = ctk.CTkButton(
        kokoro_buttons_frame,
        text="Download Docker",
        command=lambda: webbrowser.open(
            "https://www.docker.com/get-started/"))
    docker_download_button.grid(row=0, column=1, padx=5, sticky="ew")

    # Buttons Frameollama_web_download_button
    continue_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    continue_buttons_frame.pack(fill="x", padx=10, pady=10)

    ctk.CTkButton(continue_buttons_frame,
                  text="Continue",
                  command=lambda: continue_to_chat(globals)).pack(padx=5, pady=5)

    def refresh_button_states():
        """Refreshes button states and adds/removes tooltips"""
        if globals.ollama_active:
            # Disable download button and offer tooltip when Ollama is installed
            ollama_download_button.configure(state="disabled")
            ollama_web_download_button.configure(state="disabled")

            globals.ollama_web_download_tooltip = ToolTip(
                ollama_web_download_button,
                msg="Ollama already installed!",
                delay=0.3,
                follow=True,
                fg="white",
                bg="gray20",
                padx=10,
                pady=5)

            globals.ollama_interactive_download_tooltip = ToolTip(
                ollama_download_button,
                msg="Ollama already installed!",
                delay=0.3,
                follow=True,
                fg="white",
                bg="gray20",
                padx=10,
                pady=5)
        else:
            # Enable ollama download buttons and offer tooltips when Ollama is not installed
            ollama_download_button.configure(state="normal")
            ollama_web_download_button.configure(state="normal")
            globals.ollama_web_download_tooltip = ToolTip(
                ollama_web_download_button,
                msg="https://ollama.com/download",
                delay=0.3,
                follow=True,
                fg="white",
                bg="gray20",
                padx=10,
                pady=5
            )
            globals.ollama_interactive_download_tooltip = ToolTip(
                ollama_download_button,
                msg="Opens a new Terminal Window",
                delay=0.3,
                follow=True,
                fg="white",
                bg="gray20",
                padx=10,
                pady=5
            )

        # Offer tooltip for kokoro indicating installation is not necessary
        if globals.kokoro_active:
            kokoro_download_button.configure(state="disabled")
            kokoro_download_tooltip = ToolTip(
                kokoro_download_button,
                msg="Kokoro already installed!",
                delay=0.3,
                follow=True,
                fg="white",
                bg="gray20",
                padx=10,
                pady=5)
        else:
            kokoro_download_button.configure(state="normal")
            globals.kokoro_download_tooltip = ToolTip(
                kokoro_download_button,
                msg="https://github.com/remsky/Kokoro-FastAPI",
                delay=0.3,
                follow=True,
                fg="white",
                bg="gray20",
                padx=10,
                pady=5)

        if globals.docker_version:
            docker_download_button.configure(state="disabled")
            globals.docker_download_tooltip = ToolTip(
                docker_download_button,
                msg="Docker already installed!",
                delay=0.3,
                follow=True,
                fg="white",
                bg="gray20",
                padx=10,
                pady=5)
        else:
            docker_download_button.configure(state="normal")
            globals.docker_download_tooltip = ToolTip(
                docker_download_button,
                msg="https://www.docker.com/get-started/",
                delay=0.3,
                follow=True,
                fg="white",
                bg="gray20",
                padx=10,
                pady=5)

    refresh_button_states()

    def configure_widgets(globals):
        """Configure chat window widgets to enable when Ollama is active."""
        if globals.ollama_active:
            globals.send_button.configure(state="normal")
            globals.file_button.configure(state="normal")
            globals.entry_box.configure(state="normal")

    def continue_to_chat(globals):
        """Forgets setup and settings pages to return
        the user to a clean chat page"""
        ollama_test(globals)
        globals.settings_overlay.pack_forget()
        globals.setup_page.pack_forget()
        globals.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
        refresh_button_states()
        configure_widgets(globals)
