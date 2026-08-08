# src/qt_interface/qt_components/qt_title_bar.py
from PySide6.QtWidgets import (QWidget, QHBoxLayout,
                               QMenuBar, QToolButton,
                               QMenu, QStyle)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        # --- Styling ---
        self.setFixedHeight(35)
        self.setStyleSheet("""
            TitleBar {
                background-color: #1e1e1e;
                border-top: 2px transparent;
                border-bottom: 2px solid transparent;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)

        # --- LEFT: Menu Bar ---
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setNativeMenuBar(False) # Force custom menu bar on macOS too
        self.menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: transparent;
                border: none;
                color: #e0e0e0;
                font-size: 13px;
            }
            QMenuBar::item {
                padding: 6px 12px;
                border-radius: 4px;
                color: #cccccc;
            }
            QMenuBar::item:selected {
                background-color: #333333;
                color: #ffffff;
            }
            QMenu {
                background-color: #252525;
                border: 1px solid #333333;
                color: #e0e0e0;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #2ecc71;
                color: #ffffff;
            }
        """)
        layout.addWidget(self.menu_bar)

        layout.addStretch()

        # --- RIGHT: Window Controls ---
        # Minimize
        self.min_btn = QToolButton(self)
        self.min_btn.setText("─")
        self.min_btn.setFixedSize(30, 30)
        self.min_btn.setToolTip("Minimize")
        self.min_btn.setStyleSheet(self._btn_style("min"))
        self.min_btn.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(self.min_btn)
        
        # Maximize/Restore
        self.max_btn = QToolButton(self)
        self.max_btn.setText("□")
        self.max_btn.setFixedSize(30, 30)
        self.max_btn.setToolTip("Maximize")
        self.max_btn.setStyleSheet(self._btn_style("max"))
        self.max_btn.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.max_btn)
        
        # Close
        self.close_btn = QToolButton(self)
        self.close_btn.setText("×")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setToolTip("Close")
        self.close_btn.setStyleSheet(self._btn_style("close"))
        self.close_btn.clicked.connect(self.parent_window.close)
        layout.addWidget(self.close_btn)

        # Dragging State
        self.dragging = False
        self.drag_position = QPoint()

    def contextMenuEvent(self, event):
        """Show context menu on right-click."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #444;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 30px 6px 8px;
                min-width: 120px;
                margin-left: 4px;
            }
            QMenu::item:selected {
                background-color: #444;
            }
        """)
        
        style = self.style()
        
        minimize_action = QAction("Minimize", menu)
        minimize_action.setIcon(style.standardIcon(QStyle.SP_TitleBarMinButton))
        minimize_action.triggered.connect(self.parent_window.showMinimized)
        menu.addAction(minimize_action)
        
        if self.parent_window.isMaximized():
            restore_action = QAction("Restore", menu)
            restore_action.setIcon(style.standardIcon(QStyle.SP_TitleBarNormalButton))
        else:
            restore_action = QAction("Maximize", menu)
            restore_action.setIcon(style.standardIcon(QStyle.SP_TitleBarMaxButton))
        restore_action.triggered.connect(self.toggle_maximize)
        menu.addAction(restore_action)
        
        menu.addSeparator()
        
        close_action = QAction("Close", menu)
        close_action.setIcon(style.standardIcon(QStyle.SP_TitleBarCloseButton))
        close_action.triggered.connect(self.parent_window.close)
        menu.addAction(close_action)
        
        menu.exec_(event.globalPos())

    def _btn_style(self, btn_type):
        """Generates dynamic styles for buttons."""
        font_size = "16px"
        hover_color = "#333333"
        if btn_type == "min":
            font_size = "17px"
        elif btn_type == "max":
            font_size = "15px"
        elif btn_type == "close":
            font_size = "23px"
            hover_color = "#e74c3c"
        return f"""
            QToolButton {{ border: none; background: transparent; color: #cccccc; font-size: {font_size}; border-radius: 30px; }}
            QToolButton:hover {{ background-color: {hover_color}; color: #ffffff; }}
        """

    def toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.max_btn.setText("□")
        else:
            self.parent_window.showMaximized()
            self.max_btn.setText("❐")

    def mousePressEvent(self, event):
        # Allow clicking on buttons to pass through, only drag if clicking empty space
        if self.childAt(event.pos()):
            return
        if event.button() == Qt.LeftButton:
            self.dragging = True
            # Calculate offset relative to the window's top-left
            self.drag_position = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.parent_window.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        event.accept()
