from PyQt6.QtWidgets import QMainWindow

from app.program import ProgramWidget
from app.microprogram import MicroprogramWidget
from ui.main import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.program_tab = ProgramWidget()
        self.ui.tabWidget.addTab(self.program_tab, "Program")

        self.micro_tab = MicroprogramWidget()
        self.ui.tabWidget.addTab(self.micro_tab, "Microprogram")

        self.show()
