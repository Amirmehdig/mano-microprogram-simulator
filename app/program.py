from time import sleep

from PyQt6.QtCore import Qt, QObject, pyqtSignal, QThread
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QTableWidgetItem

from backend.cpu import CPU
from ui.program_tab import Ui_ProgramTab


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()

    def __init__(self, cpu, slider):
        super().__init__()
        self.cpu = cpu
        self.slider = slider

    def run(self):
        while self.cpu.clock_pulse():
            sleep(1 - (self.slider.value() / 10))
            self.progress.emit()
        self.finished.emit()


class ProgramWidget(QWidget):
    def __init__(self, cpu: CPU):
        super().__init__()
        self.ui = Ui_ProgramTab()
        self.ui.setupUi(self)

        self.cpu = cpu

        self.refresh()
        self.initialize_main_memory()
        self.initialize_micro_memory()

        self.table_detail()

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
        self.cpu.AR.set_value(0)
        self.cpu.DR.set_value(0)
        self.cpu.PC.set_value(0)
        self.cpu.AC.set_value(0)
        self.cpu.CAR.set_value(64)
        self.cpu.SBR.set_value(0)

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
            address_item = QTableWidgetItem(hex(i)[2:].zfill(2).upper())
            address_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.microMemoryTableWidget.setItem(i, 1, address_item)

            # Instruction
            inst_item = QTableWidgetItem(instruction)
            self.ui.microMemoryTableWidget.setItem(i, 2, inst_item)

            # Hex
            hex_item = QTableWidgetItem(
                hex(int("".join(str(x) for x in self.cpu.micro_program_ram[i]), 2))[2:].zfill(5).upper()
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
            address_item = QTableWidgetItem(hex(i)[2:].zfill(4).upper())
            address_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.mainMemoryTableWidget.setItem(i, 1, address_item)

            # Instruction
            inst_item = QTableWidgetItem(instruction)
            self.ui.mainMemoryTableWidget.setItem(i, 2, inst_item)

            # Hex
            hex_item = QTableWidgetItem(
                hex(int("".join(str(x) for x in self.cpu.program_ram[i]), 2))[2:].zfill(4).upper()
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

        self.cpu.PC.set_value(self.cpu.program_assembler.first_org)

        # Successful message for compile
        self.ui.consoleTextEdit.append("> Compile is successful!")

    def run(self):
        self.thread = QThread()
        self.worker = Worker(self.cpu, self.ui.speedHorizontalSlider)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.update_registers)

        self.thread.start()

        self.buttons_status(False, False, False, False)
        self.thread.finished.connect(
            lambda: self.buttons_status(True, True, True, True)
        )
        self.thread.finished.connect(
            lambda: self.ui.consoleTextEdit.append("> Program executed!")
        )

    def next(self):
        clock = self.cpu.clock_pulse()
        self.update_registers()

        if not clock:
            self.buttons_status(True, False, False, True)
            self.ui.consoleTextEdit.append("> Program executed!")

    def reset(self):
        self.refresh()
        self.update_registers()
        self.compile()
        self.buttons_status(True, True, True, True)

    def update_registers(self):
        self.ui.ARLineEdit.setText(hex(int(self.cpu.AR))[2:].zfill(4).upper())
        self.ui.DRLineEdit.setText(hex(int(self.cpu.DR))[2:].zfill(4).upper())
        self.ui.PCLineEdit.setText(hex(int(self.cpu.PC))[2:].zfill(4).upper())
        self.ui.ACLineEdit.setText(hex(int(self.cpu.AC))[2:].zfill(4).upper())
        self.ui.CARLineEdit.setText(hex(int(self.cpu.CAR))[2:].zfill(4).upper())
        self.ui.SBRLineEdit.setText(hex(int(self.cpu.SBR))[2:].zfill(4).upper())

        micro_word = list(map(str, self.cpu.micro_program_ram[int(self.cpu.CAR)].bits))
        self.ui.F1LineEdit.setText("".join(micro_word[0:3]))
        self.ui.F2LineEdit.setText("".join(micro_word[3:6]))
        self.ui.F3LineEdit.setText("".join(micro_word[6:9]))
        self.ui.CDLineEdit.setText("".join(micro_word[9:11]))
        self.ui.BRLineEdit.setText("".join(micro_word[11:13]))
        self.ui.ADLineEdit.setText("".join(micro_word[13:]))

        program_word = list(map(str, self.cpu.program_ram[int(self.cpu.PC)].bits))
        self.ui.ADDRLineEdit.setText(hex(int("".join(program_word[5:]), 2))[2:].zfill(3))
        self.ui.OPCodeLineEdit.setText("".join(program_word[1:5]))
        self.ui.ILineEdit.setText("".join(program_word[0]))

        self.initialize_main_memory()
        self.initialize_micro_memory()

        self.update_table_highlight()

    def update_table_highlight(self):
        self.ui.mainMemoryTableWidget.selectRow(self.cpu.last_PC)
        self.ui.microMemoryTableWidget.selectRow(self.cpu.last_CAR)

    def buttons_status(self, compile_status, run_status, next_status, reset_status):
        self.ui.compilePushButton.setEnabled(compile_status)
        self.ui.runPushButton.setEnabled(run_status)
        self.ui.nextPushButton.setEnabled(next_status)
        self.ui.resetPushButton.setEnabled(reset_status)
