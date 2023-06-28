from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from ui.micro_tab import Ui_MicroTab


class MicroprogramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MicroTab()
        self.ui.setupUi(self)

        self.ui.writePushButton.clicked.connect(self.write)

    def write(self):
        code = self.ui.codeTextEdit.toPlainText()

        # Compile code & write in micro memory

        # Log with console
        self.ui.consoleTextEdit.append("> LoL")

        self.initialize_memory()

    def initialize_memory(self):
        data = []  # memory data

        self.clear_table(self.ui.microTableWidget)

        for i in range(len(data)):
            self.ui.microTableWidget.insertRow(i)

            # Label
            self.ui.microTableWidget.setItem(i, 0, QTableWidgetItem(data[i][0]))
            # Address
            self.ui.microTableWidget.setItem(i, 1, QTableWidgetItem(data[i][1]))
            # Instruction
            self.ui.microTableWidget.setItem(i, 2, QTableWidgetItem(data[i][2]))
            # Hex
            self.ui.microTableWidget.setItem(i, 3, QTableWidgetItem(data[i][3]))

    def clear_table(self, table_widget):
        while table_widget.rowCount() > 0:
            table_widget.removeRow(0)
