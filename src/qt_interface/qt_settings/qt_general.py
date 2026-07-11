# src/qt_interface/qt_settings/general_qt.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QComboBox
from PySide6.QtCore import Qt
import logging


def create_general_settings_tab(globs):
    """
    Create the General Settings tab for Qt interface.
    Returns a QWidget that can be added directly to the tab widget.
    """

    # Create the main widget that will BE the tab
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(20, 20, 20, 20)  # More padding
    layout.setSpacing(20)  # More space between elements
    layout.setAlignment(Qt.AlignTop)  # Align everything to top

    # Title
    title = QLabel("General Settings")
    title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
    layout.addWidget(title)

    # Check for Updates
    github_check_checkbox = QCheckBox("Check for Updates on Startup")
    github_check_checkbox.setStyleSheet("color: white; font-size: 14px; margin-left: 10px;")
    github_check_checkbox.setChecked(globs.github_check)
    layout.addWidget(github_check_checkbox)

    # Beta Updates
    beta_checkbox = QCheckBox("Include Beta Updates")
    beta_checkbox.setStyleSheet("color: white; font-size: 14px; margin-left: 10px;")
    beta_checkbox.setChecked(globs.beta)
    layout.addWidget(beta_checkbox)

    # Save Window Placement
    window_checkbox = QCheckBox("Save Window Placement")
    window_checkbox.setStyleSheet("color: white; font-size: 14px; margin-left: 10px;")
    window_checkbox.setChecked(globs.dynamic_window_size)
    layout.addWidget(window_checkbox)

    # Legacy Mode
    legacy_checkbox = QCheckBox("Legacy Mode")
    legacy_checkbox.setStyleSheet("color: white; font-size: 14px; margin-left: 10px;")
    legacy_checkbox.setChecked(globs.legacy_mode)
    layout.addWidget(legacy_checkbox)

    # Add some spacer at the bottom so it doesn't hug the edge
    layout.addStretch()

    # Store references for later use in save function
    globs.github_check_checkbox = github_check_checkbox
    globs.beta_checkbox = beta_checkbox
    globs.window_checkbox = window_checkbox
    globs.legacy_checkbox = legacy_checkbox

    return tab_widget
