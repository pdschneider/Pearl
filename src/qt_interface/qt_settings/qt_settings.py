# src/qt_interface/qt_settings/qt_settings.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

def create_settings_panel(globals):
    """Creates the settings panel that overlays the main content."""

    # Main settings container
    settings_panel = QWidget(globals.window)
    settings_panel.setFixedSize(600, 500)  # Start with a reasonable size
    settings_panel.setStyleSheet("""
        background-color: rgb(43, 43, 43);
        border-radius: 10px;
    """)

    # Hide it initially
    settings_panel.hide()

    # Layout for the panel
    layout = QVBoxLayout(settings_panel)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)

    # Title
    title = QLabel("Settings")
    title.setStyleSheet("font-size: 20px; font-weight: bold;")
    layout.addWidget(title)

    # Placeholder content
    placeholder = QLabel("Settings content will go here...")
    layout.addWidget(placeholder)

    # Close button
    close_btn = QPushButton("Close")
    close_btn.clicked.connect(lambda: toggle_settings_panel(globals))
    layout.addWidget(close_btn)

    # Store reference
    globals.settings_panel = settings_panel

    return settings_panel

def toggle_settings_panel(globals):
    """Shows or hides the settings panel."""
    
    if globals.settings_panel.isVisible():
        globals.settings_panel.hide()
    else:
        # Calculate center position
        parent_w = globals.window.width()
        parent_h = globals.window.height()
        panel_w = globals.settings_panel.width()
        panel_h = globals.settings_panel.height()
        
        x = (parent_w - panel_w) // 2
        y = (parent_h - panel_h) // 2
        
        # Move and show
        globals.settings_panel.move(x, y)
        globals.settings_panel.show()
