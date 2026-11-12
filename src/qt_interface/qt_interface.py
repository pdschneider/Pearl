# src/qt_interface/qt_interface.py
import os
import logging
import subprocess
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, QStackedWidget
)
from PySide6.QtCore import Qt, QEvent, QTimer, QObject
from src.qt_interface.qt_components.qt_title_bar import TitleBar
from src.qt_interface.qt_components.qt_top_bar import create_top_bar
from src.qt_interface.qt_components.qt_sidebar import create_sidebar, toggle_sidebar
from src.qt_interface.qt_chat_page import create_chat_page
from src.qt_interface.qt_settings.qt_settings import create_settings_panel
from src.utils.load import load_data_path
from src.interface.setup.setup_wizard import create_wizard
from src.qt_interface.qt_components.qt_changelog import (
    create_changelog_panel, toggle_changelog_panel
)
from src.qt_interface.qt_components.qt_about import (
    create_about_panel, toggle_about_panel
)
from src.qt_interface.qt_components.qt_bug_report import (
    create_report_panel, toggle_report_panel
)
from src.qt_interface.qt_new_chat import create_new_chat_page
from src.qt_interface.qt_chat_page import (
    create_chat_page, switch_to_new_chat_page, switch_to_chat_page
)
from src.utils.icons import load_qt_icons
from src.utils.qt_save import save_qt_settings


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
        # Only act on events for our own main window
        if not isinstance(obj, QWidget) or obj.window() is not self.window:
            return False
        # Skip resize logic if a popup/menu is open
        if QApplication.activePopupWidget():
            return False

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

    # Set up Window
    globs.window.setWindowTitle("Pearl")

    # Restore saved geometry (only if dynamic window size is enabled)
    if globs.saved_width and globs.saved_height and globs.saved_x and globs.saved_y and globs.dynamic_window_size:
        globs.window.setGeometry(globs.saved_x, globs.saved_y, globs.saved_width, globs.saved_height)
    else:
        # Center default-sized window on the primary screen
        screen_geo = globs.window.screen().availableGeometry()
        x = (screen_geo.width() - 900) // 2
        y = (screen_geo.height() - 850) // 2
        globs.window.setGeometry(x, y, 900, 850)

    # Bordless Window
    globs.window.setWindowFlags(Qt.FramelessWindowHint)

    # Central Widget & Layout
    central_widget = QWidget()
    globs.window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)

    # Load Icons
    load_qt_icons(globs)

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
    exit_app_action = file_menu.addAction("Exit")

    # Attach Actions to File Menu Buttons
    open_logs_action.triggered.connect(lambda: open_logs(globs))
    open_config_action.triggered.connect(lambda: open_config(globs))
    open_chats_action.triggered.connect(lambda: open_chats(globs))
    exit_app_action.triggered.connect(lambda: globs.window.close())

    # Populate Data Menu
    data_menu.addAction("Export / Import Chats (coming soon...)")
    data_menu.addAction("Export / Import Settings (coming soon...)")

    # Populate Help Menu
    view_changelog_action = help_menu.addAction("Changelog")
    open_wizard_action = help_menu.addAction("Wizard")
    report_bug_action = help_menu.addAction("Bug Report")
    view_about_action = help_menu.addAction("About")

    # Attach Functions to Help Buttons
    view_changelog_action.triggered.connect(lambda: toggle_changelog_panel(globs))
    open_wizard_action.triggered.connect(lambda: create_wizard(globs))
    report_bug_action.triggered.connect(lambda: toggle_report_panel(globs))
    view_about_action.triggered.connect(lambda: toggle_about_panel(globs))

    # TOP BAR
    top_bar = create_top_bar(globs)
    main_layout.addWidget(top_bar)
    globs.top_bar = top_bar

    # PAGE STACK: new-chat landing page + chat page
    globs.page_stack = QStackedWidget()
    new_chat_page = create_new_chat_page(globs)

    globs.page_stack.addWidget(new_chat_page)   # index 0: landing
    chat_page = create_chat_page(globs)

    globs.page_stack.addWidget(chat_page)       # index 1: chat
    main_layout.addWidget(globs.page_stack)

    globs.chat_page = chat_page
    globs.new_chat_page = new_chat_page

    # Input starts on the landing page
    switch_to_new_chat_page(globs)
    globs.switch_to_chat_page = switch_to_chat_page

    # SETTINGS PANEL
    create_settings_panel(globs)

    # Changelog Panel
    create_changelog_panel(globs)

    # About Panel
    create_about_panel(globs)

    # Report Panel
    create_report_panel(globs)

    # Sidebar
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
        for attr in ['settings_panel', 'changelog_panel', 'about_panel', 'report_panel']:
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

    # Resize Logic
    globs.resize_state = {
        "active": False,
        "edge": None,
        "last_pos": None,
        "start_geom": None
    }

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

        for panel_attr in ['settings_panel', 'changelog_panel', 'about_panel', 'report_panel']:
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

    # Handle window close: stop observers and save settings
    original_close = globs.window.closeEvent

    def custom_close(event):
        try:
            save_qt_settings(globs)
        except Exception as e:
            logging.error(f"Error occurred when saving settings: {e}")
        original_close(event)

    globs.window.closeEvent = custom_close
