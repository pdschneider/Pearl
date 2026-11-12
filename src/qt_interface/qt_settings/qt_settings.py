# src/qt_interface/qt_settings/qt_settings.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget
)
from PySide6.QtCore import Qt
from src.qt_interface.qt_settings.qt_general import create_general_settings_tab
from src.qt_interface.qt_settings.qt_system import create_system_settings_tab
from src.qt_interface.qt_settings.qt_appearance import create_appearance_settings_tab
from src.qt_interface.qt_settings.qt_behavior import create_behavior_settings_tab
from src.qt_interface.qt_settings.qt_audio import create_audio_settings_tab
from src.qt_interface.qt_settings.qt_personalization import create_personalization_settings_tab
from src.qt_interface.qt_settings.qt_tools import create_tools_settings_tab
from src.qt_interface.qt_styling import dark
from src.utils.qt_save import save_qt_settings
import logging


def create_settings_panel(globs):
    """Creates the settings overlay panel with tabs."""

    # Main container
    settings_panel = QWidget(globs.window)
    settings_panel.setMinimumSize(650, 550)
    settings_panel.setStyleSheet("""
        background-color: rgb(43, 43, 43);
        border-radius: 10px;
    """)
    settings_panel.hide()

    layout = QVBoxLayout(settings_panel)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)

    # Header
    header_layout = QVBoxLayout()
    title = QLabel("Settings")
    title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
    header_layout.addWidget(title)
    layout.addLayout(header_layout)

    # Tabs
    tabs = QTabWidget()
    tabs.setStyleSheet(dark.tabs)

    # General tab
    general_tab = create_general_settings_tab(globs)
    tabs.addTab(general_tab, "General")

    # Appearance tab
    appearance_tab = create_appearance_settings_tab(globs)
    tabs.addTab(appearance_tab, "Appearance")

    # Behavior tab
    behavior_tab = create_behavior_settings_tab(globs)
    tabs.addTab(behavior_tab, "Behavior")

    # Personalization tab
    personalization_tab = create_personalization_settings_tab(globs)
    tabs.addTab(personalization_tab, "Personalization")

    # Tools tab
    tools_tab = create_tools_settings_tab(globs)
    tabs.addTab(tools_tab, "Tools")

    # Audio tab
    audio_tab = create_audio_settings_tab(globs)
    tabs.addTab(audio_tab, "Audio")

    # System tab
    system_tab = create_system_settings_tab(globs)
    tabs.addTab(system_tab, "System")

    layout.addWidget(tabs)

    # Close Button
    close_btn = QPushButton("Save")
    close_btn.setStyleSheet(dark.close_button)
    close_btn.setCursor(Qt.PointingHandCursor)

    def on_close_click():
        """Save settings before closing the panel."""
        save_qt_settings(globs)  # Save first
        toggle_settings_panel(globs)  # Then close
        
        # Re-establish proper z-order: sidebar > dim_overlay > main content
        if hasattr(globs, 'sidebar') and hasattr(globs, 'dim_overlay'):
            globs.dim_overlay.raise_()
            globs.sidebar.raise_()  # Sidebar must be ABOVE dim overlay
        
        if hasattr(globs, 'dim_overlay'):
            globs.dim_overlay.show()

    close_btn.clicked.connect(on_close_click)
    layout.addWidget(close_btn)

    # Store references
    globs.settings_panel = settings_panel
    globs.settings_tabs = tabs

    return settings_panel


def toggle_settings_panel(globs):
    """Shows or hides the settings panel with dim overlay."""
    
    if not hasattr(globs, 'settings_panel'):
        logging.error("Settings panel not created yet.")
        return
    
    panel = globs.settings_panel
    
    if panel.isVisible():
        # Closing settings
        panel.hide()
    else:
        # Opening settings
        
        # Close any other active panels first
        for attr in ['changelog_panel', 'about_panel', 'sidebar', 'report_panel']:
            if attr == 'sidebar':
                if hasattr(globs, 'sidebar_is_open') and globs.sidebar_is_open:
                    # Don't close sidebar - just leave it open
                    pass
            else:
                p = getattr(globs, attr, None)
                if p and p.isVisible():
                    p.hide()
        
        # Ensure overlay shows
        if hasattr(globs, 'dim_overlay'):
            globs.dim_overlay.resize(globs.window.width(), globs.window.height() - 35)
            globs.dim_overlay.move(0, 35)
            globs.dim_overlay.show()
            globs.dim_overlay.raise_()
        
        # Resize and center settings panel
        panel_w = max(650, int(globs.window.width() * 0.85))
        panel_h = max(550, int(globs.window.height() * 0.85))
        panel.resize(panel_w, panel_h)
        
        x = (globs.window.width() - panel_w) // 2
        y = max(45, (globs.window.height() - panel_h) // 2)
        panel.move(x, y)
        
        panel.raise_()
        panel.show()
    
    logging.debug(f"Settings panel visibility: {panel.isVisible()}")
