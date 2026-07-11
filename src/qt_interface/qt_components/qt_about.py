# src/qt_interface/qt_components/qt_about.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
import webbrowser


def create_about_panel(globs):
    about_panel = QWidget(globs.window)
    about_panel.setFixedSize(450, 550)
    about_panel.setStyleSheet("""
        background-color: rgb(43, 43, 43);
        border-radius: 10px;
    """)
    about_panel.hide()

    layout = QVBoxLayout(about_panel)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)

    # === HEADER ===
    header_layout = QHBoxLayout()
    title = QLabel("About")
    title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
    header_layout.addWidget(title)
    header_layout.addStretch()

    close_header_btn = QPushButton("×")
    close_header_btn.setFixedSize(30, 30)
    close_header_btn.setStyleSheet("background-color: transparent; color: white; border: none; font-size: 18px;")
    close_header_btn.setCursor(QCursor(Qt.PointingHandCursor))
    close_header_btn.clicked.connect(lambda: toggle_about_panel(globs))
    header_layout.addWidget(close_header_btn)
    layout.addLayout(header_layout)

    # === SCROLLABLE CONTENT ===
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet("""
        QScrollArea { border: none; background-color: transparent; }
        QScrollBar:vertical { background-color: #333; width: 8px; border-radius: 4px; }
        QScrollBar::handle:vertical { background-color: #4a4a4a; min-height: 50px; border-radius: 4px; }
    """)

    content_widget = QWidget()
    content_layout = QVBoxLayout(content_widget)
    content_layout.setContentsMargins(0, 0, 0, 0)
    content_layout.setSpacing(10)

    desc_label = QLabel(
"""
Pearl — Personal Everything Assistant Running Locally

Pearl is your friendly, fully local AI companion. 
Everything stays on your computer — no cloud, no tracking, no surprises.

She chats with you privately, switches context smartly based on keywords, 
supports file uploads, remembers chats only if you want, 
and looks good doing it with 5 built-in themes.

Fully offline after setup if you choose. Your data, your rules.

Key Features
• Completely private AI conversations
• Dynamic context switching (no manual prompts needed)
• Optional chat saving — delete anytime
• File uploads
• 5 beautiful themes
• Optional Kokoro TTS voice output

Requirements
• Ollama running locally (ministral-3:3b-instruct-2512-q4_K_Mrecommended for best compatibility)
• Kokoro Fast-API server (optional for TTS)
• Linux (Ubuntu 18.04+) or Windows 10/11
• Minimum: 4-core CPU, 8 GB RAM, 50 GB+ free space recommended

Icon by Twoeliz

Disclaimer — Third-Party AI Models
Pearl lets you use open-source AI models of your choice. 
The developer is not responsible for the accuracy, legality, appropriateness, 
or safety of any AI-generated content. Outputs are provided AS-IS with no warranties. 
You are fully responsible for choosing models, configuring safeguards, 
and any consequences from their use. By running Pearl you accept this.

Have fun!
"""
    )
    desc_label.setStyleSheet("font-size: 13px; color: #ddd; padding: 5px;")
    desc_label.setWordWrap(True)
    content_layout.addWidget(desc_label)

    version_label = QLabel(f"Current Version: {globs.current_version}")
    version_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2ecc71; padding-top: 10px;")
    version_label.setAlignment(Qt.AlignCenter)
    content_layout.addWidget(version_label)

    content_layout.addStretch()
    scroll_area.setWidget(content_widget)
    layout.addWidget(scroll_area, stretch=1)

    # === CLOSE BUTTON ===
    close_btn = QPushButton("Close")
    close_btn.setStyleSheet("""
        QPushButton { background-color: #3a3a3a; color: white; padding: 10px; border-radius: 4px; font-weight: bold; }
        QPushButton:hover { background-color: #4a4a4a; }
    """)
    close_btn.setCursor(QCursor(Qt.PointingHandCursor))
    close_btn.clicked.connect(lambda: toggle_about_panel(globs))
    layout.addWidget(close_btn)

    globs.about_panel = about_panel
    return about_panel


def toggle_about_panel(globs):
    if globs.about_panel.isVisible():
        globs.about_panel.hide()
        if hasattr(globs, 'dim_overlay'):
            globs.dim_overlay.hide()
    else:
        for attr in ['settings_panel', 'changelog_panel']:
            if hasattr(globs, attr):
                p = getattr(globs, attr)
                if p and p.isVisible():
                    p.hide()

        globs.dim_overlay.resize(globs.window.width(), globs.window.height() - 35)
        globs.dim_overlay.move(0, 35)
        globs.dim_overlay.show()
        globs.dim_overlay.raise_()

        x = (globs.window.width() - globs.about_panel.width()) // 2
        y = (globs.window.height() - globs.about_panel.height()) // 2
        globs.about_panel.move(x, y)
        globs.about_panel.show()
        globs.about_panel.raise_()
