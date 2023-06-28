from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from ui.program_tab import Ui_ProgramTab


class ProgramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ProgramTab()
        self.ui.setupUi(self)

        self.refresh()

        # Run button status (True: run, False: stop)
        self.is_run = True

        self.ui.compilePushButton.clicked.connect(self.compile)
        self.ui.runPushButton.clicked.connect(self.run)
        self.ui.nextPushButton.clicked.connect(self.next)
        self.ui.resetPushButton.clicked.connect(self.reset)

    def refresh(self):
        # Refresh memories
        self.initialize_main_memory()
        self.initialize_micro_memory()

        # Refresh registers
        self.ui.ARLineEdit.setText("0000")
        self.ui.DRLineEdit.setText("0000")
        self.ui.PCLineEdit.setText("0000")
        self.ui.ACLineEdit.setText("0000")
        self.ui.CARLineEdit.setText("0000")
        self.ui.SBRLineEdit.setText("0000")
        self.ui.F1LineEdit.setText("0000")
        self.ui.F2LineEdit.setText("0000")
        self.ui.F3LineEdit.setText("0000")
        self.ui.CDLineEdit.setText("0000")
        self.ui.BRLineEdit.setText("0000")
        self.ui.ADLineEdit.setText("0000")
        self.ui.ILineEdit.setText("0000")
        self.ui.OPCodeLineEdit.setText("0000")
        self.ui.ADDRLineEdit.setText("0000")

    def initialize_micro_memory(self):
        data = []  # memory data

        self.clear_table(self.ui.microMemoryTableWidget)

        for i in range(len(data)):
            self.ui.microMemoryTableWidget.insertRow(i)

            # Label
            self.ui.microMemoryTableWidget.setItem(i, 0, QTableWidgetItem(data[i][0]))
            # Address
            self.ui.microMemoryTableWidget.setItem(i, 1, QTableWidgetItem(data[i][1]))
            # Instruction
            self.ui.microMemoryTableWidget.setItem(i, 2, QTableWidgetItem(data[i][2]))
            # Hex
            self.ui.microMemoryTableWidget.setItem(i, 3, QTableWidgetItem(data[i][3]))

    def initialize_main_memory(self):
        data = []  # memory data

        self.clear_table(self.ui.mainMemoryTableWidget)

        for i in range(len(data)):
            self.ui.mainMemoryTableWidget.insertRow(i)

            # Label
            self.ui.mainMemoryTableWidget.setItem(i, 0, QTableWidgetItem(data[i][0]))
            # Address
            self.ui.mainMemoryTableWidget.setItem(i, 1, QTableWidgetItem(data[i][1]))
            # Instruction
            self.ui.mainMemoryTableWidget.setItem(i, 2, QTableWidgetItem(data[i][2]))
            # Hex
            self.ui.mainMemoryTableWidget.setItem(i, 3, QTableWidgetItem(data[i][3]))

    def clear_table(self, table_widget):
        while table_widget.rowCount() > 0:
            table_widget.removeRow(0)

    def compile(self):
        code = self.ui.codeTextEdit.toPlainText()

        # Compile code

        # Log error in console
        self.ui.consoleTextEdit.append("> Some error...")

        # Successful message for compile

    def run(self):
        # Change run button status and text
        self.ui.runPushButton.setText("Run" if self.is_run else "Stop")
        self.is_run = not self.is_run

        # Run code
        # while ...


    def next(self):
        pass

    def reset(self):
        pass

    def update_registers(self):
        self.ui.ARLineEdit.setText()
        self.ui.DRLineEdit.setText()
        self.ui.PCLineEdit.setText()
        self.ui.ACLineEdit.setText()
        self.ui.CARLineEdit.setText()
        self.ui.SBRLineEdit.setText()
        self.ui.F1LineEdit.setText()
        self.ui.F2LineEdit.setText()
        self.ui.F3LineEdit.setText()
        self.ui.CDLineEdit.setText()
        self.ui.BRLineEdit.setText()
        self.ui.ADLineEdit.setText()
        self.ui.ILineEdit.setText()
        self.ui.OPCodeLineEdit.setText()
        self.ui.ADDRLineEdit.setText()