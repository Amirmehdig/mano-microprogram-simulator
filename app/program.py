from PyQt6.QtWidgets import QWidget
from ui.program_tab import Ui_ProgramTab


class ProgramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ProgramTab()
        self.ui.setupUi(self)
