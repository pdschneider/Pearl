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
        QTextEdit QScrollBar:vertical {
            background: transparent;
            width: 8px;
            margin: 0;
        }
        QTextEdit QScrollBar::handle:vertical {
            background: rgba(255, 255, 255, 60);
            border-radius: 4px;
            min-height: 30px;
            margin: 2px;
        }
        QTextEdit QScrollBar::handle:vertical:hover {
            background: rgba(255, 255, 255, 100);
        }
        QTextEdit QScrollBar::add-line:vertical,
        QTextEdit QScrollBar::sub-line:vertical {
            height: 0;
            width: 0;
        }
        QTextEdit QScrollBar::add-page:vertical,
        QTextEdit QScrollBar::sub-page:vertical {
            background: transparent;
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
    """,
    attach_button = """
        QPushButton {
            background-color: transparent;
            border: none;
            color: #aaaaaa;
            font-size: 16px;
            font-weight: bold;
            border-radius: 11px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 30);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 60);
        }
    """,
    tts_button = """
        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 11px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 30);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 60);
        }
        QPushButton:checked {
            background-color: rgba(46, 204, 113, 40);
        }
    """,
    social_button = """
        QPushButton {
            background-color: transparent;
            border: none;
            padding: 8px 12px;
            font-size: 22px;
            color: #e0e0e0;
        }

        QPushButton:hover {
            background-color: #3a3a3d;
            border-radius: 6px;
        }

        QPushButton:pressed {
            background-color: #2a2a2d;
            border-radius: 6px;
        }
        QToolTip {
            background-color: #2b2b2b; color: white; border: 1px solid #555;
        }
    """,
    combobox = """
        QComboBox {
            color: white;
            background-color: #333;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 5px;
            font-size: 14px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid transparent;
            margin-right: 10px;
        }
        QComboBox QAbstractItemView {
            background-color: #333;
            color: white;
            selection-background-color: #2ecc71;
            border: none;
        }
    """,
    danger_button = """
        QPushButton {
            color: white;
            background-color: #c0392b;
            border: 1px solid #e74c3c;
            border-radius: 4px;
            padding: 5px 15px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #e74c3c;
        }
        QPushButton:pressed {
            background-color: #a93226;
        }
    """
)
