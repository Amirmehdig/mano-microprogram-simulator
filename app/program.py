from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QTableWidgetItem

from backend.cpu import CPU
from ui.program_tab import Ui_ProgramTab


class ProgramWidget(QWidget):
    def __init__(self, cpu: CPU):
        super().__init__()
        self.ui = Ui_ProgramTab()
        self.ui.setupUi(self)

        self.cpu = cpu

        self.refresh()

        self.table_detail()

        # Run button status (True: run, False: stop)
        self.is_run = True

        self.ui.compilePushButton.clicked.connect(self.compile)
        self.ui.runPushButton.clicked.connect(self.run)
        self.ui.nextPushButton.clicked.connect(self.next)
        self.ui.resetPushButton.clicked.connect(self.reset)

    def table_detail(self):
        # Micro table
        self.ui.microMemoryTableWidget.setColumnWidth(0, 80)
        self.ui.microMemoryTableWidget.setColumnWidth(1, 60)
        self.ui.microMemoryTableWidget.setColumnWidth(2, 160)
        self.ui.microMemoryTableWidget.setColumnWidth(3, 80)

        # Program table
        self.ui.mainMemoryTableWidget.setColumnWidth(0, 80)
        self.ui.mainMemoryTableWidget.setColumnWidth(1, 60)
        self.ui.mainMemoryTableWidget.setColumnWidth(2, 160)
        self.ui.mainMemoryTableWidget.setColumnWidth(3, 80)

    def refresh(self):
        # Refresh memories
        # self.initialize_main_memory()
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
        self.clear_table(self.ui.microMemoryTableWidget)

        for i in range(128):
            self.ui.microMemoryTableWidget.insertRow(i)

            if self.cpu.micro_program_ram[i].is_valid:
                label, instruction = self.cpu.micro_assembler.disassemble(i, self.cpu.micro_program_ram[i])
            else:
                label = ""
                instruction = ""

            # Label
            label_item = QTableWidgetItem(label if label else "")
            self.ui.microMemoryTableWidget.setItem(i, 0, label_item)

            # Address
            address_item = QTableWidgetItem(hex(i)[2:].zfill(2))
            address_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.microMemoryTableWidget.setItem(i, 1, address_item)

            # Instruction
            inst_item = QTableWidgetItem(instruction)
            self.ui.microMemoryTableWidget.setItem(i, 2, inst_item)

            # Hex
            hex_item = QTableWidgetItem(
                hex(int("".join(str(x) for x in self.cpu.micro_program_ram[i]), 2))[2:].zfill(5)
            )
            hex_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.microMemoryTableWidget.setItem(i, 3, hex_item)

            # Row color
            if i % 2 == 1:
                for item in [label_item, address_item, inst_item, hex_item]:
                    item.setBackground(QColor("#fafafa"))

    def initialize_main_memory(self):
        self.clear_table(self.ui.mainMemoryTableWidget)

        after_hlt = False
        for i in range(2048):
            self.ui.mainMemoryTableWidget.insertRow(i)

            if self.cpu.program_ram[i].is_valid:
                label, instruction = self.cpu.program_assembler.disassemble(i, self.cpu.program_ram[i], after_hlt)
            else:
                label = ""
                instruction = ""

            if instruction == "HLT":
                after_hlt = True

            # Label
            label_item = QTableWidgetItem(label if label else "")
            self.ui.mainMemoryTableWidget.setItem(i, 0, label_item)

            # Address
            address_item = QTableWidgetItem(hex(i)[2:].zfill(4))
            address_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.mainMemoryTableWidget.setItem(i, 1, address_item)

            # Instruction
            inst_item = QTableWidgetItem(instruction)
            self.ui.mainMemoryTableWidget.setItem(i, 2, inst_item)

            # Hex
            hex_item = QTableWidgetItem(
                hex(int("".join(str(x) for x in self.cpu.program_ram[i]), 2))[2:].zfill(4)
            )
            hex_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.mainMemoryTableWidget.setItem(i, 3, hex_item)

            # Row color
            if i % 2 == 1:
                for item in [label_item, address_item, inst_item, hex_item]:
                    item.setBackground(QColor("#fafafa"))

    def clear_table(self, table_widget):
        while table_widget.rowCount() > 0:
            table_widget.removeRow(0)

    def compile(self):
        code = self.ui.codeTextEdit.toPlainText()

        # Compile code
        self.cpu.program_assemble(code)
        self.initialize_main_memory()

        # Successful message for compile
        self.ui.consoleTextEdit.append("> Compile is successful!")

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
