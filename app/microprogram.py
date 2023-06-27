from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from ui.micro_tab import Ui_MicroTab


class MicroprogramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MicroTab()
        self.ui.setupUi(self)
