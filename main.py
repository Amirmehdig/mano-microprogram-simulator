import sys

from PyQt6.QtWidgets import QApplication

from app.main import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec())
