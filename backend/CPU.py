from memory import Memory
from register import Register
from assemblermircroprogram import AssemblerMicroProgram
from F1 import F1
from F2 import F2
from F3 import F3
from CD import Condition
from BR import Branch

class CPU:
    def __init__(self):
        self.program_label_table = {}
        self.micro_program_label_table = {}

        self.program_ram = Memory(16, 2048)

        self.AR = Register(11)
        self.PC = Register(11)
        self.AC = Register(16)
        self.DR = Register(16)

        self.micro_program_ram = Memory(20, 128)

        self.CAR = Register(7)
        self.CAR.set_value(64)
        self.SBR = Register(7)

        self.program_counter = int(self.PC)

        self.F1 = F1(self)
        self.F2 = F2(self)
        self.F3 = F3(self)
        self.CD = Condition(self)
        self.BR = Branch(self)


    def assemble(self, code: str):
        micro_assembler = AssemblerMicroProgram(code)
        self.micro_program_label_table = micro_assembler.get_label_table()
        micro_controller = micro_assembler.get_memory_words()
        for key in micro_controller:
            self.micro_program_ram[key].word_to_register(micro_controller[key])


    def clock_pulse(self):
        word = list(map(str, self.micro_program_ram[int(self.CAR)].bits))
        self.F1.instruction(word[0:3])
        self.F2.instruction(word[3:6])
        self.F3.instruction(word[6:9])
        if self.CD.instruction(word[9: 11]):
            self.BR.instruction(word[11: 13], True)
        else:
            self.BR.instruction(word[11: 13], False)
