# src/qt_interface/qt_interface.py
import os
import logging
import subprocess
import webbrowser
import urllib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QEvent, QTimer, QObject
from src.qt_interface.qt_components.qt_title_bar import TitleBar
from src.qt_interface.qt_components.qt_top_bar import create_top_bar
from src.qt_interface.qt_components.qt_sidebar import create_sidebar, toggle_sidebar
from src.qt_interface.qt_chat_page import create_chat_page
from src.qt_interface.qt_settings.qt_settings import create_settings_panel
from src.utils.load import load_data_path
from src.interface.setup.setup_wizard import create_wizard
from src.qt_interface.qt_components.qt_changelog import create_changelog_panel, toggle_changelog_panel
from src.qt_interface.qt_components.qt_about import create_about_panel, toggle_about_panel


class WindowResizeEventFilter(QObject):
    """
    Global event filter to handle cursor shape changes for frameless window resizing.
    This ensures mouse moves over child widgets also trigger edge detection.
    """
    
    def __init__(self, window, resize_margin=10):
        super().__init__()
        self.window = window
        self.resize_margin = resize_margin
        self.last_cursor_shape = Qt.ArrowCursor
        self.resize_state = {
            "active": False,
            "edge": None,
            "last_pos": None,
            "start_geom": None
        }
        
    def get_resize_edge_from_global(self, global_pos):
        geom = self.window.frameGeometry()
        x, y = global_pos.x(), global_pos.y()
        
        left = x <= geom.left() + self.resize_margin
        right = x >= geom.right() - self.resize_margin
        top = y <= geom.top() + self.resize_margin
        bottom = y >= geom.bottom() - self.resize_margin
        
        if top and left: return "TL"
        if top and right: return "TR"
        if bottom and left: return "BL"
        if bottom and right: return "BR"
        if left: return "L"
        if right: return "R"
        if top: return "T"
        if bottom: return "B"
        return None
    
    def get_cursor_shape(self, edge):
        shapes = {
            "L": Qt.SizeHorCursor, "R": Qt.SizeHorCursor,
            "T": Qt.SizeVerCursor, "B": Qt.SizeVerCursor,
            "TL": Qt.SizeFDiagCursor, "BR": Qt.SizeFDiagCursor,
            "TR": Qt.SizeBDiagCursor, "BL": Qt.SizeBDiagCursor,
            None: Qt.ArrowCursor
        }
        return shapes.get(edge, Qt.ArrowCursor)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseMove:
            global_pos = event.globalPosition().toPoint()
            
            # --- Active resize drag ---
            if self.resize_state["active"]:
                start_geom = self.resize_state["start_geom"]
                start_pos = self.resize_state["last_pos"]
                
                total_delta = global_pos - start_pos
                edge = self.resize_state["edge"]
                
                min_w = self.window.minimumWidth()
                min_h = self.window.minimumHeight()
                
                # Start from original geometry each frame
                new_left = start_geom.left()
                new_right = start_geom.right()
                new_top = start_geom.top()
                new_bottom = start_geom.bottom()
                
                if edge in ["L", "TL", "BL"]:
                    new_left = start_geom.left() + total_delta.x()
                    if new_left > start_geom.right() - min_w:
                        new_left = start_geom.right() - min_w
                if edge in ["R", "TR", "BR"]:
                    new_right = start_geom.right() + total_delta.x()
                    if new_right < start_geom.left() + min_w:
                        new_right = start_geom.left() + min_w
                if edge in ["T", "TL", "TR"]:
                    new_top = start_geom.top() + total_delta.y()
                    if new_top > start_geom.bottom() - min_h:
                        new_top = start_geom.bottom() - min_h
                if edge in ["B", "BL", "BR"]:
                    new_bottom = start_geom.bottom() + total_delta.y()
                    if new_bottom < start_geom.top() + min_h:
                        new_bottom = start_geom.top() + min_h
                
                self.window.setGeometry(new_left, new_top, new_right - new_left, new_bottom - new_top)
                
                return True
            
            # --- Cursor shape only ---
            edge = self.get_resize_edge_from_global(global_pos)
            target_shape = self.get_cursor_shape(edge)
            
            if self.last_cursor_shape != target_shape:
                self.window.setCursor(target_shape)
                self.last_cursor_shape = target_shape
                
        elif event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                global_pos = event.globalPosition().toPoint()
                edge = self.get_resize_edge_from_global(global_pos)
                
                if edge:
                    self.resize_state["active"] = True
                    self.resize_state["edge"] = edge
                    self.resize_state["last_pos"] = global_pos
                    self.resize_state["start_geom"] = self.window.frameGeometry()
                    return True
        
        elif event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                if self.resize_state["active"]:
                    self.resize_state["active"] = False
                    self.resize_state["edge"] = None
                    self.resize_state["last_pos"] = None
                    self.resize_state["start_geom"] = None
                    self.window.setCursor(Qt.ArrowCursor)
                    return True
        
        return False


def create_qt_interface(globs):
    """Creates the main PySide6 interface with borderless window."""

    # SETUP WINDOW
    globs.window.setWindowTitle("Pearl")
    if globs.saved_width and globs.saved_height and globs.saved_x and globs.saved_y:
        globs.window.setGeometry(
            globs.saved_x, globs.saved_y,
            globs.saved_width, globs.saved_height)
    else:
        globs.window.resize(900, 850)

    # MAKE IT BORDERLESS
    globs.window.setWindowFlags(Qt.FramelessWindowHint)

    # CENTRAL WIDGET & LAYOUT
    central_widget = QWidget()
    globs.window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)

    # Title Bar
    title_bar = TitleBar(globs.window)
    main_layout.addWidget(title_bar)
    globs.title_bar = title_bar

    # Menus
    file_menu = title_bar.menu_bar.addMenu("File")
    data_menu = title_bar.menu_bar.addMenu("Data")
    help_menu = title_bar.menu_bar.addMenu("Help")

    # Populate File Menu
    open_logs_action = file_menu.addAction("Logs")
    open_config_action = file_menu.addAction("Config")
    open_chats_action = file_menu.addAction("Chats")

    # Attach Actions to File Menu Buttons
    open_logs_action.triggered.connect(lambda: open_logs(globs))
    open_config_action.triggered.connect(lambda: open_config(globs))
    open_chats_action.triggered.connect(lambda: open_chats(globs))

    # Populate Data Menu
    data_menu.addAction("Export / Import Chats (coming soon...)")
    data_menu.addAction("Export / Import Settings (coming soon...)")

    # Populate Help Menu
    view_changelog_action = help_menu.addAction("Changelog")
    open_wizard_action = help_menu.addAction("Wizard")
    view_github_action = help_menu.addAction("Github")
    view_codeberg_action = help_menu.addAction("Codeberg")
    report_bug_action = help_menu.addAction("Report a Bug")
    view_about_action = help_menu.addAction("About")

    # Attach Functions to Help Buttons
    view_changelog_action.triggered.connect(lambda: toggle_changelog_panel(globs))
    open_wizard_action.triggered.connect(lambda: create_wizard(globs))
    view_github_action.triggered.connect(lambda: webbrowser.open(
        url=f"https://github.com/pdschneider/{globs.title}"))
    view_codeberg_action.triggered.connect(lambda: webbrowser.open(
            url="https://codeberg.org/pdschneider/InvoiceBuddy"))
    report_bug_action.triggered.connect(lambda: report_bug(globs))
    view_about_action.triggered.connect(lambda: toggle_about_panel(globs))

    # TOP BAR
    top_bar = create_top_bar(globs)
    main_layout.addWidget(top_bar)
    globs.top_bar = top_bar

    # CHAT PAGE
    chat_page = create_chat_page(globs)
    main_layout.addWidget(chat_page)
    globs.chat_page = chat_page

    # SETTINGS PANEL
    create_settings_panel(globs)

    # Changelog Panel
    create_changelog_panel(globs)

    # About Panel
    create_about_panel(globs)

    # SIDEBAR
    sidebar = create_sidebar(globs)
    sidebar.setParent(central_widget)
    sidebar.raise_()
    globs.sidebar = sidebar

    # Dim Overlay for Panels
    dim_overlay = QWidget(central_widget)
    dim_overlay.setParent(central_widget)
    dim_overlay.setAttribute(Qt.WA_StyledBackground, True)
    dim_overlay.setStyleSheet("background-color: rgba(0, 0, 0, 120);")
    dim_overlay.hide()

    def close_all_panels(event=None):
        """Closes all panels and the overlay when overlay is clicked."""
        for attr in ['settings_panel', 'changelog_panel', 'about_panel']:
            if hasattr(globs, attr):
                panel = getattr(globs, attr)
                if panel and panel.isVisible():
                    panel.hide()
        # Close sidebar if open
        if hasattr(globs, 'sidebar_is_open') and globs.sidebar_is_open:
            toggle_sidebar(globs, globs.sidebar)
        globs.dim_overlay.hide()

    dim_overlay.mousePressEvent = close_all_panels
    globs.dim_overlay = dim_overlay

    # RESIZE LOGIC
    RESIZE_MARGIN = 10
    globs.resize_state = {
        "active": False,
        "edge": None,
        "last_pos": None,
        "start_geom": None
    }

    def get_resize_edge_from_global(window, global_pos):
        geom = window.frameGeometry()
        x, y = global_pos.x(), global_pos.y()

        left = x <= geom.left() + RESIZE_MARGIN
        right = x >= geom.right() - RESIZE_MARGIN
        top = y <= geom.top() + RESIZE_MARGIN
        bottom = y >= geom.bottom() - RESIZE_MARGIN

        if top and left: return "TL"
        if top and right: return "TR"
        if bottom and left: return "BL"
        if bottom and right: return "BR"
        if left: return "L"
        if right: return "R"
        if top: return "T"
        if bottom: return "B"
        return None

    def get_cursor_shape(edge):
        shapes = {
            "L": Qt.SizeHorCursor, "R": Qt.SizeHorCursor,
            "T": Qt.SizeVerCursor, "B": Qt.SizeVerCursor,
            "TL": Qt.SizeFDiagCursor, "BR": Qt.SizeFDiagCursor,
            "TR": Qt.SizeBDiagCursor, "BL": Qt.SizeBDiagCursor,
            None: Qt.ArrowCursor
        }
        return shapes.get(edge, Qt.ArrowCursor)

    globs.window.setMouseTracking(True)
    for child in globs.window.findChildren(QWidget):
        child.setMouseTracking(True)

    # Install Global Event Filter for Cursor Changes
    resize_filter = WindowResizeEventFilter(globs.window)
    globs.app.installEventFilter(resize_filter)
    globs.resize_filter = resize_filter

    # Enable dynamic overlay/panel resize on window resize
    def update_overlay_geometry():
        """Updates overlay (settings + changelog + about) when resizing the window."""
        if hasattr(globs, 'dim_overlay'):
            globs.dim_overlay.resize(globs.window.width(), globs.window.height() - 35)
            globs.dim_overlay.move(0, 35)

        for panel_attr in ['settings_panel', 'changelog_panel', 'about_panel']:
            panel = getattr(globs, panel_attr, None)
            if panel and panel.isVisible():
                if panel_attr == 'settings_panel':
                    panel_w = max(650, int(globs.window.width() * 0.85))
                    panel_h = max(550, int(globs.window.height() * 0.85))
                    panel.resize(panel_w, panel_h)
                else:
                    # Fixed size for changelog/about
                    pass

                # Re-center
                parent_w = globs.window.width()
                parent_h = globs.window.height()
                panel_w = panel.width()
                panel_h = panel.height()
                x = (parent_w - panel_w) // 2
                y = max(45, (parent_h - panel_h) // 2)
                panel.move(x, y)

    original_resize = globs.window.resizeEvent
    def custom_resize(event):
        original_resize(event)
        QTimer.singleShot(0, update_overlay_geometry)

    globs.window.resizeEvent = custom_resize

    # SHOW
    globs.window.setMinimumSize(750, 650)
    globs.window.show()

    def open_logs(globs):
        """Opens the logs folder."""
        if globs.os_name.startswith("Windows"):
            logging.debug(f"Opening logs folder on Windows...")
            os.startfile(load_data_path("cache", "logs"))
        else:
            logging.debug(f"Opening logs folder on Linux...")
            subprocess.run(
                ['xdg-open', load_data_path("cache", "logs")], check=True)

    def open_config(globs):
        """Opens the settings folder."""
        if globs.os_name.startswith("Windows"):
            logging.debug(f"Opening settings folder on Windows...")
            os.startfile(load_data_path("config"))
        else:
            logging.debug(f"Opening settings folder on Linux...")
            subprocess.run(
                ['xdg-open', load_data_path("config")], check=True)

    def open_chats(globs):
        """Opens the chats folder."""
        if globs.os_name.startswith("Windows"):
            logging.debug(f"Opening settings folder on Windows...")
            os.startfile(load_data_path("config"))
        else:
            logging.debug(f"Opening settings folder on Linux...")
            subprocess.run(
                ['xdg-open', load_data_path("local", "chats")], check=True)


    def report_bug(globs):
        """Opens the default mail application to report a bug."""

        # Display a messagebox first
        reply = QMessageBox.question(
            globs.window,
            "Report Bug?",
            f"Would you like to open your default email application for a bug report?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes)
        
        # Opens up the default email application
        if reply == QMessageBox.StandardButton.Yes:
            logging.debug(f"Bug Report button clicked.")
            to = "bugs@phillipplays.com"
            subject = "Bug Report for Pearl"
            body = f"Thank you very much for making a report! " \
            f"Let me know what problem occurred, the behavior your expected, " \
            f"and feel free to also include any logs or screenshots that may help! " \
            f" | Pearl Version: {globs.current_version} | OS: {globs.os_name}"
            encoded_body = urllib.parse.quote(body)
            mailto = f"mailto:{to}?subject={subject}&body={encoded_body}"
            webbrowser.open(mailto)
