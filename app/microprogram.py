import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QTableWidgetItem

from backend.assembly.default_micro import default_code
from backend.cpu import CPU
from ui.micro_tab import Ui_MicroTab


class MicroprogramWidget(QWidget):
    def __init__(self, cpu: CPU):
        super().__init__()
        self.ui = Ui_MicroTab()
        self.ui.setupUi(self)

        self.cpu = cpu

        self.table_detail()
        self.initialize_micro_memory()
        self.ui.codeTextEdit.setText(default_code)

        self.ui.writePushButton.clicked.connect(self.write)

    def table_detail(self):
        # Micro table
        self.ui.microTableWidget.setColumnWidth(0, 80)
        self.ui.microTableWidget.setColumnWidth(1, 60)
        self.ui.microTableWidget.setColumnWidth(2, 160)
        self.ui.microTableWidget.setColumnWidth(3, 80)

    def write(self):
        code = self.ui.codeTextEdit.toPlainText()

        try:
            # Compile code & write in micro memory
            self.cpu.micro_assemble(code)

            # Log with console
            self.ui.consoleTextEdit.append("> Microprogram memory updated!")

            self.initialize_micro_memory()
        except Exception:
            print(traceback.format_exc())

    def initialize_micro_memory(self):
        self.clear_table(self.ui.microTableWidget)

        for i in range(128):
            self.ui.microTableWidget.insertRow(i)

            if self.cpu.micro_program_ram[i].is_valid:
                label, instruction = self.cpu.micro_assembler.disassemble(i, self.cpu.micro_program_ram[i])
            else:
                label = ""
                instruction = ""

            # Label
            label_item = QTableWidgetItem(label if label else "")
            self.ui.microTableWidget.setItem(i, 0, label_item)

            # Address
            address_item = QTableWidgetItem(hex(i)[2:].zfill(2).upper())
            address_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.microTableWidget.setItem(i, 1, address_item)

            # Instruction
            inst_item = QTableWidgetItem(instruction)
            self.ui.microTableWidget.setItem(i, 2, inst_item)

            # Hex
            hex_item = QTableWidgetItem(
                hex(int("".join(str(x) for x in self.cpu.micro_program_ram[i]), 2))[2:].zfill(5).upper()
            )
            hex_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.microTableWidget.setItem(i, 3, hex_item)

            # Row color
            if i % 2 == 1:
                for item in [label_item, address_item, inst_item, hex_item]:
                    item.setBackground(QColor("#fafafa"))

    def clear_table(self, table_widget):
        while table_widget.rowCount() > 0:
            table_widget.removeRow(0)
