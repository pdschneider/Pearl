from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
import sys

def pyside_app():
    # Creates base application
    app = QApplication(sys.argv)

    # Creates Window
    window = QMainWindow()

    # Sets window parameters
    window.setWindowTitle("Update Available")
    window.setGeometry(500, 200, 480, 220)

    # Create and set label
    label = QLabel("Pearl has a new update!", window)
    label.move(175, 50)
    label.adjustSize()

    # Create update button
    download = QPushButton(window)
    download.setText("Download")
    download.move(200,75)
    download.adjustSize()

    # Shows Window
    window.show()

    # Starts the event loop
    sys.exit(app.exec())

pyside_app()