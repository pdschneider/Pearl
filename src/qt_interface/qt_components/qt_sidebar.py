# src/qt_interface/qt_components/qt_sidebar.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton,
                               QLabel, QScrollArea)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QColor

def create_sidebar(globals):
    """Creates the sidebar with smooth slide-in animation."""

    sidebar = QWidget()
    sidebar.setFixedWidth(250)
    sidebar.setAutoFillBackground(True)
    # Dark background matching your customtkinter theme
    sidebar.setStyleSheet("background-color: rgb(43, 43, 43);") 

    # Main vertical layout
    layout = QVBoxLayout(sidebar)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)

    # === BUTTONS FRAME (at the top) ===
    buttons_layout = QHBoxLayout()
    buttons_layout.setSpacing(5)

    # Hamburger button
    hamburger_btn = QPushButton("☰")
    hamburger_btn.setFixedHeight(40)
    hamburger_btn.setCursor(Qt.PointingHandCursor)
    hamburger_btn.clicked.connect(lambda: toggle_sidebar(globals, sidebar))
    buttons_layout.addWidget(hamburger_btn)

    # New Chat button
    new_chat_btn = QPushButton("✎")
    new_chat_btn.setFixedHeight(40)
    new_chat_btn.setCursor(Qt.PointingHandCursor)
    buttons_layout.addWidget(new_chat_btn)

    layout.addLayout(buttons_layout)

    # === CHAT HISTORY SECTION ===
    # Title label
    history_title = QLabel("Chat History")
    history_title.setStyleSheet("font-weight: bold; font-size: 14px; padding-top: 10px;")
    history_title.setAlignment(Qt.AlignLeft)
    layout.addWidget(history_title)

    # Scroll area for chat entries (we'll build this next)
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet("border: none; background-color: transparent;")
    layout.addWidget(scroll_area)

    # Store state
    globals.sidebar = sidebar
    globals.sidebar_is_open = False
    globals.scroll_area = scroll_area  # Save for later use

    # Initial Position: Off-screen to the left
    sidebar.setGeometry(-250, 0, 250, globals.window.height())

    return sidebar

def toggle_sidebar(globals, sidebar):
    """Smoothly slides the sidebar in or out."""

    target_x = 0 if not globals.sidebar_is_open else -250
    current_rect = sidebar.geometry()

    # Create the animation
    anim = QPropertyAnimation(sidebar, b"geometry")
    anim.setDuration(300)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    globals.sidebar_animation = anim

    start_rect = QRect(current_rect.x(), current_rect.y(), current_rect.width(), current_rect.height())
    end_rect = QRect(target_x, 0, 250, globals.window.height())

    anim.setStartValue(start_rect)
    anim.setEndValue(end_rect)

    sidebar.raise_()
    anim.start()

    globals.sidebar_is_open = not globals.sidebar_is_open
