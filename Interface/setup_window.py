# Interface/setup_window.py
import webbrowser
import customtkinter as ctk
import Utils.fonts as fonts
from CTkToolTip import CTkToolTip
from Connections.ollama import ollama_installation
from Connections.docker import docker_installation
from Connections.kokoro import install_kokoro
from Utils.refresher import refresh_gui


def create_setup_tab(globals, setup_tab):
    """
    Creates the tab to display setup instructions for new users.

            Parameters:
                    globals: Global variables
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
                 Pearl uses Ollama under the hood to generate text. Clicking the Interactive Install button below
                 will open an interactive terminal where you can install Ollama and your first model (simple).

                 If preferred, you can also download Ollama from the Ollama website manually along with a starting model
                 using the links provided. The recommended starting model is llama3.2:latest (same process, more steps).
                 """).pack(fill="x", expand=True, padx=10, pady=10)

    # Ollama Buttons
    ollama_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    ollama_buttons_frame.pack(padx=10, pady=10, side="top")

    globals.ollama_interactive_download_button = ctk.CTkButton(
        ollama_buttons_frame,
        text="Interactive Install",
        state="normal",
        command=lambda: ollama_installation(globals))
    globals.ollama_interactive_download_button.grid(row=0, column=0, padx=5, sticky="ew")

    globals.ollama_web_download_button = ctk.CTkButton(
        ollama_buttons_frame,
        text="Web Download",
        state="normal",
        command=lambda: webbrowser.open("https://ollama.com/download"))
    globals.ollama_web_download_button.grid(row=0, column=1, padx=5, sticky="ew")

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
                For enhanced Text to Speech, you may also install Kokoro (this is optional).

                Docker must first be installed (a dependency of Kokoro's). Docker is a containerization engine
                designed to isolate processes and make them more easily manageable and secure. An interactive install
                is available for Linux users, otherwise you can download Docker from the official website.
                """).pack(
                    fill="both", expand=True, padx=10, pady=10)

    # Docker Buttons
    docker_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    docker_buttons_frame.pack(padx=10, pady=10)

    globals.docker_interactive_download_button = ctk.CTkButton(
        docker_buttons_frame,
        text="Interactive Install",
        state="normal",
        command=lambda: docker_installation(globals))
    globals.docker_interactive_download_button.grid(row=0, column=0, padx=5, sticky="ew")

    # Remove Interactive Install button if not on Linux
    if not globals.os_name.startswith("Linux"):
        globals.docker_interactive_download_button.grid_remove()

    globals.docker_web_download_button = ctk.CTkButton(
        docker_buttons_frame,
        text="Web Download",
        command=lambda: webbrowser.open(
            "https://www.docker.com/get-started/"))
    globals.docker_web_download_button.grid(row=0, column=1, padx=5, sticky="ew")

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
                 After Docker is installed, you can follow the interactive install for Kokoro (Linux Only)
                 or follow the instructions on the Kokoro GitHub page for your OS. A reboot is required
                 between installing Docker and installing Kokoro.
                 """).pack(
                     fill="both", expand=True, padx=10, pady=10)

    # Kokoro Buttons
    kokoro_buttons_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
    kokoro_buttons_frame.pack(padx=10, pady=10)

    globals.kokoro_interactive_download_button = ctk.CTkButton(
        kokoro_buttons_frame,
        text="Install Kokoro",
        state="normal",
        command=lambda: install_kokoro(globals))
    globals.kokoro_interactive_download_button.grid(row=0, column=0, padx=5, sticky="ew")

    # Remove Kokoro Interactive Install button on Windows
    if not globals.os_name.startswith("Linux"):
        globals.kokoro_interactive_download_button.grid_remove()

    globals.kokoro_web_download_button = ctk.CTkButton(
        kokoro_buttons_frame,
        text="Web Download",
        state="normal",
        command=lambda: webbrowser.open(
            "https://github.com/remsky/Kokoro-FastAPI"))
    globals.kokoro_web_download_button.grid(row=0, column=1, padx=5, sticky="ew")

    # Continue Buttons Frame
    continue_buttons_frame = ctk.CTkFrame(setup_tab, fg_color="transparent")
    continue_buttons_frame.pack(fill="x", padx=10, pady=10)

    ctk.CTkButton(continue_buttons_frame,
                  text="Continue",
                  command=lambda: continue_to_chat(globals)).pack(padx=5, pady=5)

    def refresh_button_states():
        """Refreshes button states and adds/removes tooltips"""
        if globals.ollama_active:
            # Disable download button and offer tooltip when Ollama is installed
            globals.ollama_interactive_download_button.configure(state="disabled")
            globals.ollama_web_download_button.configure(state="disabled")

            globals.ollama_web_download_tooltip = CTkToolTip(
                globals.ollama_web_download_button,
                message="Ollama already installed!",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)

            globals.ollama_interactive_download_tooltip = CTkToolTip(
                globals.ollama_interactive_download_button,
                message="Ollama already installed!",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)
        else:
            # Enable ollama download buttons and offer tooltips when Ollama is not installed
            if globals.os_name.startswith("Linux"):
                globals.ollama_interactive_download_button.configure(state="normal")
            globals.ollama_web_download_button.configure(state="normal")
            globals.ollama_web_download_tooltip = CTkToolTip(
                globals.ollama_web_download_button,
                message="https://ollama.com/download",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5
            )
            if globals.os_name.startswith("Linux"):
                globals.ollama_interactive_download_tooltip = CTkToolTip(
                    globals.ollama_interactive_download_button,
                    message="Opens a new Terminal Window",
                    delay=0.3,
                    follow=True,
                    padx=10,
                    pady=5
                )

        # Offer tooltip for kokoro indicating installation is not necessary
        if globals.kokoro_active:
            globals.kokoro_web_download_button.configure(state="disabled")
            kokoro_download_tooltip = CTkToolTip(
                globals.kokoro_web_download_button,
                message="Kokoro already installed!",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)
        else:
            globals.kokoro_web_download_button.configure(state="normal")
            globals.kokoro_download_tooltip = CTkToolTip(
                globals.kokoro_web_download_button,
                message="https://github.com/remsky/Kokoro-FastAPI",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)

        if globals.docker_version:
            globals.docker_web_download_button.configure(state="disabled")
            if globals.os_name.startswith("Linux"):
                globals.docker_interactive_download_button.configure(state="disabled")
            globals.docker_web_download_tooltip = CTkToolTip(
                globals.docker_web_download_button,
                message="Docker already installed!",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)
            if globals.os_name.startswith("Linux"):
                globals.docker_interactive_download_tooltip = CTkToolTip(
                    globals.docker_interactive_download_button,
                    message="Docker already installed!",
                    delay=0.3,
                    follow=True,
                    padx=10,
                    pady=5)
        else:
            globals.docker_web_download_button.configure(state="normal")
            if globals.os_name.startswith("Linux"):
                globals.docker_interactive_download_button.configure(state="normal")
            globals.docker_web_download_tooltip = CTkToolTip(
                globals.docker_web_download_button,
                message="https://www.docker.com/get-started/",
                delay=0.3,
                follow=True,
                padx=10,
                pady=5)
            if globals.os_name.startswith("Linux"):
                globals.docker_interactive_download_tooltip = CTkToolTip(
                    globals.docker_interactive_download_button,
                    message="Opens a new Terminal Window",
                    delay=0.3,
                    follow=True,
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
        globals.app_title.configure(text="Pearl at your service!")
        refresh_gui(globals)
        # Map chat page
        app_pages = [globals.chat_page, globals.setup_page, globals.settings_page, globals.changelog]
        for page in app_pages:
            if page:
                page.pack_forget()
        globals.chat_page.pack(fill="both", expand=True, padx=10, pady=0)
        refresh_button_states()
        configure_widgets(globals)
