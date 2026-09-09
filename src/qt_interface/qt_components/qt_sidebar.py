# src/qt_interface/qt_components/qt_sidebar.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton,
                               QLabel, QScrollArea)
from PySide6.QtCore import (Qt, QPropertyAnimation,
                            QEasingCurve, QRect, QTimer)
from src.managers.chat_history import load_conversations, load_specific_conversation
from src.managers.chat_history import start_new_conversation
from src.qt_interface.qt_settings.qt_settings import toggle_settings_panel
from src.qt_interface.qt_styling import dark
import logging
import sounddevice as sd


# Title bar height
TITLE_BAR_HEIGHT = 35


def create_sidebar(globs):
    """Creates the sidebar with smooth slide-in animation."""

    sidebar = QWidget()
    sidebar.setFixedWidth(250)
    sidebar.setAutoFillBackground(True)
    sidebar.setStyleSheet("background-color: rgb(43, 43, 43);") 

    # Main vertical layout
    layout = QVBoxLayout(sidebar)
    layout.setContentsMargins(5, 5, 5, 5)
    layout.setSpacing(5)

    # === BUTTONS FRAME (at the top) ===
    buttons_layout = QHBoxLayout()
    buttons_layout.setSpacing(5)
    buttons_layout.setContentsMargins(0, 0, 0, 0)

    # Hamburger button
    hamburger_btn = QPushButton("☰")
    hamburger_btn.setFixedSize(40, 40)
    hamburger_btn.setCursor(Qt.PointingHandCursor)
    hamburger_btn.clicked.connect(lambda: toggle_sidebar(globs, sidebar))
    buttons_layout.addWidget(hamburger_btn)

    # New Chat button
    new_chat_btn = QPushButton("✎  New Chat")
    new_chat_btn.setFixedSize(100, 40)
    new_chat_btn.setCursor(Qt.PointingHandCursor)
    new_chat_btn.clicked.connect(lambda: start_new_chat(globs))
    buttons_layout.addWidget(new_chat_btn)
    buttons_layout.addStretch()

    layout.addLayout(buttons_layout)

    # === CHAT HISTORY SECTION ===
    # Title label
    history_title = QLabel("Chat History")
    history_title.setStyleSheet("font-weight: bold; font-size: 14px; padding-top: 10px;")
    history_title.setAlignment(Qt.AlignLeft)
    layout.addWidget(history_title)

    # Scroll area for chat entries
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet("border: none; background-color: transparent;")
    
    # Create scroll content widget
    scroll_content = QWidget()
    scroll_content.setStyleSheet("background-color: transparent;")
    scroll_content.setLayout(QVBoxLayout())
    scroll_content.layout().setSpacing(4)
    scroll_content.layout().setContentsMargins(0, 0, 0, 0)
    
    scroll_area.setWidget(scroll_content)
    layout.addWidget(scroll_area)
    
    # Store references
    globs.sidebar = sidebar
    globs.sidebar_is_open = False
    globs.scroll_area = scroll_area
    globs._sidebar_scroll_content = scroll_content

    # Settings Button
    settings_btn = QPushButton("⚙  Settings")
    settings_btn.setFixedSize(100, 40)
    settings_btn.setCursor(Qt.PointingHandCursor)
    settings_btn.setStyleSheet(dark.settings_button)
    settings_btn.clicked.connect(lambda: toggle_settings_panel(globs))
    layout.addWidget(settings_btn)

    # Initial Position: Off-screen to the left, STARTING BELOW TITLE BAR
    sidebar_height = globs.window.height() - TITLE_BAR_HEIGHT
    sidebar.setGeometry(-250, TITLE_BAR_HEIGHT, 250, sidebar_height)

    # Store last chat count for optimization
    globs.sidebar_last_count = 0

    # Initial population
    populate_sidebar_history(globs)

    return sidebar


def toggle_sidebar(globs, sidebar):
    """Smoothly slides the sidebar in or out."""
    import logging
    
    logging.debug(f"TOGGLE_SIDEBAR CALLED: is_open={globs.sidebar_is_open}, has_anim={hasattr(globs, 'sidebar_animation')}")
    
    if getattr(globs, 'sidebar_animation', None):
        logging.debug(f"Stopping existing animation...")
        globs.sidebar_animation.stop()

    target_x = 0 if not globs.sidebar_is_open else -250
    sidebar_height = globs.window.height() - TITLE_BAR_HEIGHT

    start_rect = sidebar.geometry()
    end_rect = QRect(target_x, TITLE_BAR_HEIGHT, 250, sidebar_height)

    logging.debug(f"Target X: {target_x}")
    logging.debug(f"Start geometry: {start_rect}")
    logging.debug(f"End geometry: {end_rect}")

    anim = QPropertyAnimation(sidebar, b"geometry")
    anim.setDuration(300)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    anim.setStartValue(start_rect)
    anim.setEndValue(end_rect)
    
    globs.sidebar_animation = anim

    if not globs.sidebar_is_open:
        logging.debug(f"Opening sidebar... showing overlay, raising sidebar")
        globs.dim_overlay.resize(globs.window.width(), globs.window.height() - TITLE_BAR_HEIGHT)
        globs.dim_overlay.move(0, TITLE_BAR_HEIGHT)
        globs.dim_overlay.show()
        sidebar.raise_()
    else:
        logging.debug(f"Closing sidebar... raising sidebar, will hide overlay AFTER animation")
        sidebar.raise_()
        QTimer.singleShot(1, lambda: globs.dim_overlay.hide())

    anim.start()
    logging.debug(f"Sidebar geometry when opening: {sidebar.geometry()}")
    logging.debug(f"Window geometry: {globs.window.geometry()}")
    logging.debug(f"Animation started, toggling is_open from {globs.sidebar_is_open} to {not globs.sidebar_is_open}")

    globs.sidebar_is_open = not globs.sidebar_is_open
    logging.debug(f"After toggle: sidebar_is_open = {globs.sidebar_is_open}, pos={sidebar.pos()}")


def populate_sidebar_history(globs):
    """Populates sidebar with grouped chat history."""

    # Load conversations first
    conversations = load_conversations(globs)
    current_count = len(conversations)
    
    # Skip if count hasn't changed (optimization)
    if hasattr(globs, 'sidebar_last_count') and globs.sidebar_last_count == current_count:
        logging.debug(f"Sidebar chat count unchanged ({current_count}). Skipping repopulation.")
        return
    
    globs.sidebar_last_count = current_count

    # Clear existing entries
    scroll_content = getattr(globs, '_sidebar_scroll_content', None)
    if scroll_content:
        while scroll_content.layout().count():
            item = scroll_content.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    else:
        return

    # Load conversations
    conversations = load_conversations(globs)
    if not conversations:
        no_chats = QLabel("No chats yet!")
        no_chats.setAlignment(Qt.AlignCenter)
        no_chats.setStyleSheet("color: gray; padding: 20px;")
        scroll_content.layout().addWidget(no_chats)
        return

    # Group by date categories
    from datetime import datetime, timedelta
    now = datetime.now()
    today = now.date()

    groups = {
        "Today": [],
        "Yesterday": [],
        "Last Week": [],
        "Past Month": [],
        "Older": []
    }

    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    for convo in conversations:
        created_at = convo["metadata"].get("created_at")
        if not created_at:
            groups["Older"].append(convo)
            continue

        try:
            created_dt = datetime.fromisoformat(created_at)
            created_date = created_dt.date()
        except:
            groups["Older"].append(convo)
            continue
    
        if created_date == today:
            groups["Today"].append(convo)
        elif created_date == yesterday:
            groups["Yesterday"].append(convo)
        elif created_date > week_ago:
            groups["Last Week"].append(convo)
        elif created_date > month_ago:
            groups["Past Month"].append(convo)
        else:
            groups["Older"].append(convo)

    # Create section headers and entries
    for section_name, convos in groups.items():
        if not convos:
            continue

        # Section header
        header = QLabel(section_name)
        header.setStyleSheet("font-weight: bold; font-size: 14px; padding: 8px 0 4px 0;")
        scroll_content.layout().addWidget(header)

        # Chat entries
        for convo in convos:
            title = convo["metadata"].get("title", "Untitled")
            if len(title) > 30:
                title = f"{title[:25]}..."

            conv_id = convo["metadata"]["conversation_id"]

            # Entry frame
            entry = QWidget()
            entry.setFixedHeight(40)
            entry.setStyleSheet(
                """
                QWidget {
                    background-color: #3a3a3a;
                    border-radius: 6px;
                }
                QWidget:hover {
                    background-color: #454545;
                }
                """
            )
            entry_layout = QHBoxLayout(entry)
            entry_layout.setContentsMargins(12, 5, 12, 5)

            # Title label
            title_label = QLabel(title)
            title_label.setWordWrap(True)
            entry_layout.addWidget(title_label)

            # Make clickable
            def on_click(event, cid=conv_id):
                load_specific_conversation(globs, cid)
                # Reload chat bubbles (need to import or reference)
                if hasattr(globs, 'refresh_chat_page'):
                    globs.refresh_chat_page()
                # Close sidebar
                if globs.sidebar_is_open:
                    toggle_sidebar(globs, globs.sidebar)

            entry.mousePressEvent = on_click
            title_label.mousePressEvent = on_click

            scroll_content.layout().addWidget(entry)

    # Scroll to top
    globs.scroll_area.verticalScrollBar().setValue(0)


def start_new_chat(globs):
    """Resets to a new conversation and clears the chat page."""

    # Stop sound
    sd.stop()

    # Start new conversation
    start_new_conversation(globs)
