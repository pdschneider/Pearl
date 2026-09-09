# src/qt_interface/qt_styling.py
from types import SimpleNamespace

dark = SimpleNamespace(
    scroll_area = """
        QScrollArea { border: none; background-color: transparent; }
        QScrollBar:vertical { background-color: #333; width: 8px; border-radius: 4px; }
        QScrollBar::handle:vertical { background-color: #4a4a4a; min-height: 50px; border-radius: 4px; }
    """,
    close_button = """
        QPushButton { background-color: #3a3a3a; color: white; padding: 10px; border-radius: 4px; font-weight: bold; }
        QPushButton:hover { background-color: #4a4a4a; }
    """,
    settings_button = """
        QPushButton {
            background-color: #3a3a3a;
            border: none;
            border-radius: 8px;
            color: white;
        }
        QPushButton:hover {
            background-color: #454545;
        }
    """,
    menu = """
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
    """,
    menu_bar = """
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
    """,
    tabs = """
        QTabWidget::pane {
            border: 1px solid #444;
            border-radius: 5px;
            background-color: #2b2b2b;
        }
        QTabBar::tab {
            background-color: #333;
            color: #aaa;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        QTabBar::tab:selected {
            background-color: #2b2b2b;
            color: #2ecc71;
            font-weight: bold;
        }
    """,
    input_box = """
        QTextEdit {
            background-color: transparent;
            border: none;
            color: white;
            padding: 6px;
        }
        QTextEdit:focus {
            outline: none;
        }
    """,
    send_button = """
        QPushButton {
            background-color: #4a4a4a;
            border: none;
            border-radius: 16px;
            color: white;
        }
        QPushButton:hover {
            background-color: #5a5a5a;
        }
    """
)