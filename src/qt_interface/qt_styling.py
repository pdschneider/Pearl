# src/qt_interface/qt_styling.py
from types import SimpleNamespace

dark = SimpleNamespace(
    scroll_area = """
        QScrollArea#chatScrollArea { border: none; background-color: transparent; }
        QScrollBar#chatScrollBar:vertical { background-color: #2b2b2b; width: 10px; border-radius: 5px; margin: 0; }
        QScrollBar#chatScrollBar::handle:vertical { background-color: #505055; min-height: 40px; border-radius: 5px; }
        QScrollBar#chatScrollBar::handle:vertical:hover { background-color: #606066; }
        QScrollBar#chatScrollBar::add-page:vertical, QScrollBar#chatScrollBar::sub-page:vertical { background: none; }
        QScrollBar#chatScrollBar::add-line:vertical, QScrollBar#chatScrollBar::sub-line:vertical {
            height: 0; subcontrol-position: none;
        }
        QScrollBar#chatScrollBar::up-arrow:vertical, QScrollBar#chatScrollBar::down-arrow:vertical {
            width: 0; height: 0; image: none;
        }
    """,
    close_button = """
        QPushButton { background-color: #3a3a3a; color: white; padding: 10px; border-radius: 4px; font-weight: bold; }
        QPushButton:hover { background-color: #4a4a4a; }
    """,
    settings_button = """
        QPushButton {
            background-color: #333333;
            border: 1px solid #4a4a4a;
            border-radius: 6px;
            color: #d0d0d0;
            padding: 6px 14px;
            font-size: 13px;
        }
        QPushButton:hover {
            background-color: #3d3d3d;
            border: 1px solid #7E57C2;
            color: white;
        }
        QPushButton:pressed {
            background-color: #2a2a2a;
        }
    """,
    settings_checkbox = """
        QCheckBox {
            color: #d0d0d0; font-size: 13px; spacing: 10px;
            padding: 6px 10px;
            background-color: transparent; border-radius: 4px;
        }
        QCheckBox:hover { color: white; }
        QCheckBox::indicator {
            width: 18px; height: 18px;
            border: 1px solid #555; border-radius: 4px;
            background-color: #2b2b2b;
        }
        QCheckBox::indicator:hover { border: 1px solid #7E57C2; }
        QCheckBox::indicator:checked {
            background-color: #7E57C2; border: 1px solid #6a48b0;
        }
        QCheckBox::indicator:checked:disabled { background-color: #555; border: 1px solid #555; }
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
            background-color: #7E57C2;
            color: #ffffff;
        }
    """,
    tabs = """
        QTabWidget::pane {
            border: none;
            border-top: 1px solid #3a3a40;
            background-color: transparent;
        }
        QTabBar::tab {
            background-color: transparent;
            color: #888;
            padding: 8px 18px;
            margin-right: 4px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-size: 13px;
        }
        QTabBar::tab:hover {
            color: #dddddd;
        }
        QTabBar::tab:selected {
            color: #7E57C2;
            border-bottom: 2px solid #7E57C2;
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
            background-color: #2b2b2b;
            width: 10px;
            border-radius: 5px;
            margin: 0;
        }
        QTextEdit QScrollBar::handle:vertical {
            background-color: #505055;
            border-radius: 5px;
            min-height: 40px;
        }
        QTextEdit QScrollBar::handle:vertical:hover {
            background-color: #606066;
        }
        QTextEdit QScrollBar::add-line:vertical,
        QTextEdit QScrollBar::sub-line:vertical {
            height: 0;
            subcontrol-position: none;
        }
        QTextEdit QScrollBar::up-arrow:vertical,
        QTextEdit QScrollBar::down-arrow:vertical {
            width: 0;
            height: 0;
            image: none;
        }
        QTextEdit QScrollBar::add-page:vertical,
        QTextEdit QScrollBar::sub-page:vertical {
            background: none;
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
            selection-background-color: #7E57C2;
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
    """,
    line_edit = """
        QLineEdit {
            background-color: #333;
            border: 1px solid #555;
            border-radius: 4px;
            color: white;
            padding: 5px;
        }
        QLineEdit:focus {
            border: 1px solid #7E57C2;
        }
    """,
    scrollbar = """
        QScrollBar:vertical {
            background-color: #2b2b2b;
            width: 10px;
            border-radius: 5px;
            margin: 0;
        }
        QScrollBar::handle {
            background-color: #505055;
            border-radius: 5px;
            min-height: 40px;
        }
        QScrollBar::handle:hover {
            background-color: #606066;
        }
        QScrollBar::add-page, QScrollBar::sub-page {
            background: none;
        }
        QScrollBar::add-line, QScrollBar::sub-line {
            height: 0;
            subcontrol-position: none;
        }
        QScrollBar::up-arrow, QScrollBar::down-arrow {
            width: 0;
            height: 0;
            image: none;
        }
    """,
    attachment_chip = """
        QFrame#attachmentChip {
            background-color: #3a3a3a;
            border: 1px solid #4a4a4a;
            border-radius: 8px;
        }
        QFrame#attachmentChip:hover {
            border: 1px solid #7E57C2;
        }
    """,
    attachment_chip_label = """
        QLabel {
            color: #d0d0d0;
            background-color: transparent;
            font-size: 13px;
        }
    """,
    attachment_chip_remove = """
        QPushButton {
            background-color: transparent;
            border: none;
            color: #999999;
            font-size: 11px;
            border-radius: 9px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 40);
            color: white;
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 70);
        }
    """
)
