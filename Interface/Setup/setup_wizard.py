# Interface/Setup/setup_wizard.py
from PySide6.QtWidgets import (QWizard, QWizardPage,
                               QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout)
from PySide6.QtGui import QPixmap
import webbrowser
import logging
from Connections.ollama import ollama_installation
from Connections.docker import docker_installation
from Connections.kokoro import install_kokoro

def create_wizard(globals):
    """Opens the wizard window."""
    # Create Wizard Window
    wizard = QWizard()
    wizard.setWindowTitle("Pearl Setup")
    wizard.resize(650, 600)

    # Welcome Page
    welcome_page = QWizardPage()
    wizard.addPage(welcome_page)
    welcome_page.setTitle("Welcome to Pearl")
    welcome_page.setSubTitle("Personal Everything Assistant Running Locally")
    welcome_page.setPixmap(QWizard.LogoPixmap, QPixmap("defaults/assets/pearl.ico"))
    welcome_layout = QVBoxLayout()
    welcome_page.setLayout(welcome_layout)

    welcome_note = QLabel()
    welcome_note.setText(
        """
        Thank you for installing Pearl!
        
        Pearl is your friendly, fully local AI companion. 
        Everything stays on your computer — no cloud, no tracking, no surprises.

        She chats with you privately, switches context smartly based on keywords, 
        supports file uploads, remembers chats only if you want, 
        and looks good doing it with 5 built-in themes.

        Fully offline after setup if you choose. Your data, your rules.
        """)
    welcome_layout.addWidget(welcome_note)

    # Ollama Page
    ollama_page = QWizardPage()
    wizard.addPage(ollama_page)
    ollama_page.setTitle("Install Ollama")
    ollama_page.setSubTitle("Ollama is what Pearl uses under the hood to generate text (Required)")
    ollama_page.setPixmap(QWizard.LogoPixmap, QPixmap("defaults/assets/pearl.ico"))

    # Main Layout
    ollama_layout = QVBoxLayout()
    ollama_page.setLayout(ollama_layout)

    # Instructions
    ollama_instructions = QLabel()
    ollama_instructions.setText(
        """
        Pearl uses Ollama under the hood to generate text. Clicking the
        Interactive Install button below will open an interactive terminal where
        you can install Ollama and your first model (simple).

        If preferred, you can also download Ollama from the Ollama website
        manually along with a starting model using the links provided.
        The recommended starting model is llama3.2:latest (same process, more steps).
        """)
    ollama_layout.addWidget(ollama_instructions)

    # Install/Download Buttons
    ollama_buttons_layout = QHBoxLayout()

    ollama_install = QPushButton()
    ollama_install.setText("Interactive Install")
    ollama_install.clicked.connect(lambda: ollama_installation(globals))
    ollama_buttons_layout.addWidget(ollama_install)
    ollama_install.setFixedWidth(150)

    ollama_download = QPushButton()
    ollama_download.setText("Web Download")
    ollama_download.clicked.connect(lambda: webbrowser.open("https://ollama.com/download"))
    ollama_buttons_layout.addWidget(ollama_download)
    ollama_download.setFixedWidth(150)

    ollama_models = QPushButton()
    ollama_models.setText("Download Models")
    ollama_models.clicked.connect(lambda: webbrowser.open("https://ollama.com/search"))
    ollama_buttons_layout.addWidget(ollama_models)
    ollama_models.setFixedWidth(150)

    ollama_layout.addLayout(ollama_buttons_layout)

    # TTS Page
    tts_page = QWizardPage()
    wizard.addPage(tts_page)
    tts_page.setTitle("Enhanced TTS")
    tts_page.setSubTitle("Optional TTS install (skippable)")
    tts_page.setPixmap(QWizard.LogoPixmap, QPixmap("defaults/assets/pearl.ico"))
    tts_layout = QVBoxLayout()
    tts_page.setLayout(tts_layout)

    # Docker Section
    docker_header = QLabel()
    docker_header.setText("Install Docker")
    docker_header.setStyleSheet("font-weight: bold;")
    tts_layout.addWidget(docker_header)

    docker_instructions = QLabel()
    docker_instructions.setText(
        """
        For enhanced Text to Speech, you may also install Kokoro (this is optional).

        Docker must first be installed (a dependency of Kokoro's). Docker is a
        containerization engine designed to isolate processes and make them more
        easily manageable and secure. An interactive install is available for Linux
        users, otherwise you can download Docker from the official website.
        """)
    tts_layout.addWidget(docker_instructions)

    # Install/Download Buttons
    docker_buttons_layout = QHBoxLayout()

    if globals.os_name.startswith("Linux"):
        docker_install = QPushButton()
        docker_install.setText("Interactive Install")
        docker_install.clicked.connect(lambda: docker_installation(globals))
        docker_buttons_layout.addWidget(docker_install)
        docker_install.setFixedWidth(150)

    docker_download = QPushButton()
    docker_download.setText("Web Download")
    docker_download.clicked.connect(lambda: webbrowser.open("https://www.docker.com/get-started/"))
    docker_buttons_layout.addWidget(docker_download)
    docker_download.setFixedWidth(150)

    tts_layout.addLayout(docker_buttons_layout)

    # Kokoro Section
    kokoro_header = QLabel()
    kokoro_header.setText("Install Kokoro")
    kokoro_header.setStyleSheet("font-weight: bold;")
    tts_layout.addWidget(kokoro_header)

    kokoro_instructions = QLabel()
    kokoro_instructions.setText(
        """
        After Docker is installed, you can follow the interactive install for
        Kokoro (Linux Only) or follow the instructions on the Kokoro GitHub
        page for your OS. A reboot is required between installing Docker and
        installing Kokoro.
        """)
    tts_layout.addWidget(kokoro_instructions)

    # Install/Download Buttons
    kokoro_buttons_layout = QHBoxLayout()

    if globals.os_name.startswith("Linux"):
        kokoro_install = QPushButton()
        kokoro_install.setText("Interactive Install")
        kokoro_install.clicked.connect(lambda: install_kokoro(globals))
        kokoro_buttons_layout.addWidget(kokoro_install)
        kokoro_install.setFixedWidth(150)

    kokoro_download = QPushButton()
    kokoro_download.setText("Web Download")
    kokoro_download.clicked.connect(lambda: webbrowser.open("https://github.com/remsky/Kokoro-FastAPI"))
    kokoro_buttons_layout.addWidget(kokoro_download)
    kokoro_download.setFixedWidth(150)

    tts_layout.addLayout(kokoro_buttons_layout)

    # Execute Wizard
    result = wizard.exec()

    if result == QWizard.Accepted:
        logging.info("Wizard finished")
    else:
        logging.info("Wizard cancelled")
