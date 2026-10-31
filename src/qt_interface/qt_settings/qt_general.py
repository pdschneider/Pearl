# src/qt_interface/qt_settings/qt_general.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QComboBox,
    QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from src.qt_interface.qt_styling import dark
from src.utils.toast import show_toast
from src.utils.load import load_data_path
import logging
import shutil


def create_general_settings_tab(globs):
    """
    Create the General Settings tab for Qt interface.
    Returns a QWidget that can be added directly to the tab widget.
    """

    # Create the main widget that will BE the tab
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)
    layout.setAlignment(Qt.AlignTop)

    # Title
    title = QLabel("General Settings")
    title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
    layout.addWidget(title)

    # Language Selection
    language_layout = QHBoxLayout()

    language_label = QLabel()
    language_label.setText("Language: ")
    language_layout.addWidget(language_label)

    language_combobox = QComboBox()
    language_combobox.addItem("English")
    language_combobox.setCurrentIndex(0)
    language_combobox.setFixedWidth(200)
    language_combobox.setStyleSheet(dark.combobox)
    language_layout.addWidget(language_combobox)
    language_layout.addStretch()

    layout.addLayout(language_layout)

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

    # Delete Chats
    delete_layout = QHBoxLayout()
    delete_label = QLabel()
    delete_label.setText("Delete All Chats")
    delete_label.setStyleSheet("QLabel { color: white; font-size: 14px; }")
    delete_layout.addWidget(delete_label)

    delete_button = QPushButton()
    delete_button.setText("Delete")
    delete_button.setStyleSheet(dark.danger_button)
    delete_button.setCursor(Qt.PointingHandCursor)
    delete_button.clicked.connect(lambda: delete_chats())
    delete_layout.addWidget(delete_button)
    delete_layout.addStretch()

    layout.addLayout(delete_layout)

    # Add some spacer at the bottom so it doesn't hug the edge
    layout.addStretch()

    def delete_chats():
        # Create a messagebox asking for confirmation
        logging.debug(f"Attempting to delete chats...")
        if not globs.legacy_mode:
            reply = QMessageBox.question(
                globs.window,
                "Delete Chats",
                f"Are you sure you would like to delete all conversations?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    shutil.rmtree(load_data_path("local", "chats"))
                    logging.info(f"Chats deleted!")
                    from src.qt_interface.qt_components.qt_sidebar import populate_sidebar_history
                    populate_sidebar_history(globs)
                    show_toast(globs, "Conversations deleted!")
                except Exception as e:
                    logging.error(f"Unable to delete chats due to: {e}")
                    show_toast(globs, "Could not delete conversations", _type="error")

    # Store references for later use in save function
    globs.github_check_checkbox = github_check_checkbox
    globs.beta_checkbox = beta_checkbox
    globs.window_checkbox = window_checkbox
    globs.legacy_checkbox = legacy_checkbox

    return tab_widget
