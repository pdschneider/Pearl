# Interface/Setup/setup_window.py
import webbrowser
import customtkinter as ctk
import src.utils.fonts as fonts
from CTkToolTip import CTkToolTip
from src.connections.ollama import ollama_installation
from src.connections.docker import docker_installation
from src.connections.kokoro import install_kokoro
from src.utils.refresher import refresh_gui


def create_setup_tab(globs, setup_tab):
    """
    Creates the tab to display setup instructions for new users.

            Parameters:
                    globs: Global variables
                    setup_tab: The main frame of the setup window
    """
    setup_frame = ctk.CTkScrollableFrame(setup_tab)
    setup_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Ollama Frame
    ollama_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    ollama_frame.pack(fill="x", expand=False, padx=10, pady=10)

    ctk.CTkLabel(ollama_frame,
                 text="Install Ollama",
                 font=fonts.title_font,
                 anchor="center").pack(fill="x", pady=10, padx=10)

    inner_width = 900
    ollama_text_container = ctk.CTkFrame(
        ollama_frame,
        width=inner_width,
        fg_color="transparent")
    ollama_text_container.pack(anchor="center", pady=5)

    # Ollama installation instructions
    ctk.CTkLabel(ollama_text_container,
                 justify="left",
                 anchor="w",
                 font=fonts.body_font,
                 text="""
                 Thank you for installing Pearl!\n
                 Pearl uses Ollama under the hood to generate text. Clicking the Install Ollama button below
                 will open an interactive terminal where you can install Ollama and your first model (simple).

                 If preferred, you can also download Ollama from the Ollama website manually along with a starting model
                 using the links provided. The recommended starting model is ministral-3:3b-instruct-2512-q4_K_M (same process, more steps).
                 """).pack(fill="x", expand=True, padx=10, pady=10)

    # Ollama Buttons
    ollama_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    ollama_buttons_frame.pack(padx=10, pady=10, side="top")

    globs.ollama_interactive_download_button = ctk.CTkButton(
        ollama_buttons_frame,
        text="Install Ollama",
        state="normal",
        command=lambda: ollama_installation(globs))
    globs.ollama_interactive_download_button.grid(row=0, column=0, padx=5, sticky="ew")

    globs.ollama_web_download_button = ctk.CTkButton(
        ollama_buttons_frame,
        text="Web Download",
        state="normal",
        command=lambda: webbrowser.open("https://ollama.com/download"))
    globs.ollama_web_download_button.grid(row=0, column=1, padx=5, sticky="ew")

    models_download_button = ctk.CTkButton(
        ollama_buttons_frame,
        state="normal",
        text="Download Models",
        command=lambda: webbrowser.open("https://ollama.com/search"))
    models_download_button.grid(row=0, column=2, padx=5, sticky="ew")

    # Models tooltip
    models_tooltip = CTkToolTip(models_download_button,
               message="https://ollama.com/search",
               delay=0.3,
               follow=True,
               padx=10,
               pady=5)

    # Docker Setup
    docker_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    docker_frame.pack(fill="x", expand=False, padx=10, pady=10)

    ctk.CTkLabel(docker_frame,
                 text="Install Docker",
                 font=fonts.title_font,
                 anchor="center").pack(fill="x", pady=10, padx=10)

    docker_text_container = ctk.CTkFrame(
        docker_frame,
        width=inner_width,
        fg_color="transparent")
    docker_text_container.pack(anchor="center", pady=5)

    ctk.CTkLabel(docker_text_container,
                justify="left",
                anchor="w",
                text="""
                For enhanced Text to Speech, you may also install Docker + Kokoro (this is optional).

                Docker must first be installed (a dependency of Kokoro's). Docker is a containerization engine
                designed to isolate processes and make them more easily manageable and secure. An interactive
                install is available (recommended), or you can download Docker from their official website.
                """).pack(
                    fill="both", expand=True, padx=10, pady=10)

    # Docker Buttons
    docker_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    docker_buttons_frame.pack(padx=10, pady=10)

    globs.docker_interactive_download_button = ctk.CTkButton(
        docker_buttons_frame,
        text="Install Docker",
        state="normal",
        command=lambda: docker_installation(globs))
    globs.docker_interactive_download_button.grid(row=0, column=0, padx=5, sticky="ew")

    globs.docker_web_download_button = ctk.CTkButton(
        docker_buttons_frame,
        text="Web Download",
        command=lambda: webbrowser.open(
            "https://www.docker.com/get-started/"))
    globs.docker_web_download_button.grid(row=0, column=1, padx=5, sticky="ew")

    # Kokoro Frame
    kokoro_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    kokoro_frame.pack(fill="x", expand=False, padx=10, pady=10)

    ctk.CTkLabel(kokoro_frame,
                 text="Install Kokoro",
                 font=fonts.title_font,
                 anchor="center").pack(fill="x", pady=10, padx=10)

    kokoro_text_container = ctk.CTkFrame(
        kokoro_frame,
        width=inner_width,
        fg_color="transparent")
    kokoro_text_container.pack(anchor="center", pady=5)

    ctk.CTkLabel(kokoro_text_container,
                 justify="left",
                 anchor="w",
                 text="""
                 After Docker is installed, you can run the interactive install for Kokoro
                 or follow the instructions on the Kokoro GitHub page for your OS. A reboot is
                 sometimes required between installing Docker and installing Kokoro.
                 """).pack(
                     fill="both", expand=True, padx=10, pady=10)

    # Kokoro Buttons
    kokoro_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    kokoro_buttons_frame.pack(padx=10, pady=10)

    globs.kokoro_interactive_download_button = ctk.CTkButton(
        kokoro_buttons_frame,
        text="Install Kokoro",
        state="normal",
        command=lambda: install_kokoro(globs))
    globs.kokoro_interactive_download_button.grid(row=0, column=0, padx=5, sticky="ew")

    globs.kokoro_web_download_button = ctk.CTkButton(
        kokoro_buttons_frame,
        text="Web Download",
        state="normal",
        command=lambda: webbrowser.open(
            "https://github.com/remsky/Kokoro-FastAPI"))
    globs.kokoro_web_download_button.grid(row=0, column=1, padx=5, sticky="ew")

    # Continue Buttons Frame
    continue_buttons_frame = ctk.CTkFrame(setup_tab, fg_color="transparent")
    continue_buttons_frame.pack(fill="x", padx=10, pady=10)

    ctk.CTkButton(continue_buttons_frame,
                  text="Continue",
                  command=lambda: continue_to_chat(globs)).pack(padx=5, pady=5)

    def refresh_button_states():
        """Refreshes button states and adds/removes tooltips"""
        if globs.ollama_active:
            # Disable download button and offer tooltip when Ollama is installed
            globs.ollama_interactive_download_button.configure(state="disabled")
            globs.ollama_web_download_button.configure(state="disabled")

            globs.ollama_web_download_tooltip = CTkToolTip(
                globs.ollama_web_download_button,
                message="Ollama already installed!",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)

            globs.ollama_interactive_download_tooltip = CTkToolTip(
                globs.ollama_interactive_download_button,
                message="Ollama already installed!",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)
        else:
            # Enable ollama download buttons and offer tooltips when Ollama is not installed
            if globs.os_name.startswith("Linux"):
                globs.ollama_interactive_download_button.configure(state="normal")
            globs.ollama_web_download_button.configure(state="normal")
            globs.ollama_web_download_tooltip = CTkToolTip(
                globs.ollama_web_download_button,
                message="https://ollama.com/download",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5
            )
            if globs.os_name.startswith("Linux"):
                globs.ollama_interactive_download_tooltip = CTkToolTip(
                    globs.ollama_interactive_download_button,
                    message="Opens a new Terminal Window",
                    delay=0.3,
                    follow=True,
                    padx=10,
                    pady=5
                )

        # Offer tooltip for kokoro indicating installation is not necessary
        if globs.kokoro_active:
            globs.kokoro_web_download_button.configure(state="disabled")
            kokoro_download_tooltip = CTkToolTip(
                globs.kokoro_web_download_button,
                message="Kokoro already installed!",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)
        else:
            globs.kokoro_web_download_button.configure(state="normal")
            globs.kokoro_download_tooltip = CTkToolTip(
                globs.kokoro_web_download_button,
                message="https://github.com/remsky/Kokoro-FastAPI",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)

        if globs.docker_version:
            globs.docker_web_download_button.configure(state="disabled")
            if globs.os_name.startswith("Linux"):
                globs.docker_interactive_download_button.configure(state="disabled")
            globs.docker_web_download_tooltip = CTkToolTip(
                globs.docker_web_download_button,
                message="Docker already installed!",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)
            if globs.os_name.startswith("Linux"):
                globs.docker_interactive_download_tooltip = CTkToolTip(
                    globs.docker_interactive_download_button,
                    message="Docker already installed!",
                    delay=0.3,
                    follow=True,
                    padx=10,
                    pady=5)
        else:
            globs.docker_web_download_button.configure(state="normal")
            if globs.os_name.startswith("Linux"):
                globs.docker_interactive_download_button.configure(state="normal")
            globs.docker_web_download_tooltip = CTkToolTip(
                globs.docker_web_download_button,
                message="https://www.docker.com/get-started/",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)
            if globs.os_name.startswith("Linux"):
                globs.docker_interactive_download_tooltip = CTkToolTip(
                    globs.docker_interactive_download_button,
                    message="Opens a new Terminal Window",
                    delay=0.3,
                    follow=True,
                    padx=10,
                    pady=5)

    refresh_button_states()

    def configure_widgets(globs):
        """Configure chat window widgets to enable when Ollama is active."""
        if globs.ollama_active:
            globs.send_button.configure(state="normal")
            globs.file_button.configure(state="normal")
            globs.entry_box.configure(state="normal")

    def continue_to_chat(globs):
        """Forgets setup and settings pages to return
        the user to a clean chat page"""
        globs.app_title.configure(text="Pearl at your service!")
        refresh_gui(globs)
        # Map chat page
        app_pages = [globs.chat_page, globs.setup_page, globs.settings_page, globs.changelog]
        for page in app_pages:
            if page:
                page.pack_forget()
        globs.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
        refresh_button_states()
        configure_widgets(globs)
