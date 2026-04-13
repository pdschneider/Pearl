# src/qt_interface/qt_interface.py
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from src.qt_interface.qt_components.qt_top_bar import create_top_bar


def create_interface(globals):
    """Creates the main interface in PySide."""
    # Set up main window attributes
    globals.window.setWindowTitle("Pearl")
    if globals.saved_width and globals.saved_height and globals.saved_x and globals.saved_y:
        w = globals.saved_width
        h = globals.saved_height
        x = globals.saved_x
        y = globals.saved_y
        globals.window.setGeometry(x, y, w, h)
    else:
        globals.window.resize(900, 850)

    # Central Widget
    central_widget = QWidget()
    globals.window.setCentralWidget(central_widget)

    # Configure layout
    main_layout = QVBoxLayout(central_widget)
    main_layout.setContentsMargins(5, 5, 5, 5)
    main_layout.setSpacing(5)
    globals.window.setLayout(main_layout)

    # Create top navigation bar
    top_bar = create_top_bar(globals, central_widget)
    main_layout.addWidget(top_bar)

    title = QLabel()
    title.setText("Pearl")
    title.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(title)

    # Show window
    globals.window.show()
