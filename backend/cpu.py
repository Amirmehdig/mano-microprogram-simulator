from backend.assembler.program import ProgramAssembler
from backend.memory import Memory
from backend.register import Register
from backend.assembler.micro import MicroprogramAssembler
from backend.F1 import F1
from backend.F2 import F2
from backend.F3 import F3
from backend.CD import Condition
from backend.BR import Branch


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
        self.micro_assemble(open("backend/assembly/default_micro.asm", "r").read())

        self.CAR = Register(7)
        self.CAR.set_value(64)
        self.SBR = Register(7)

        self.program_counter = int(self.PC)

        self.F1 = F1(self)
        self.F2 = F2(self)
        self.F3 = F3(self)
        self.CD = Condition(self)
        self.BR = Branch(self)

    def micro_assemble(self, micro_code: str):
        self.micro_assembler = MicroprogramAssembler(micro_code)
        self.micro_assembler.assemble()

        for key, value in self.micro_assembler.res_dict.items():
            self.micro_program_ram[key].word_to_register(value)

    def program_assemble(self, program_code: str):
        self.program_assembler = ProgramAssembler(program_code, self.micro_assembler.label_dict)
        self.program_assembler.assemble()

        for key, value in self.program_assembler.res_dict.items():
            self.program_ram[key].word_to_register(value)

    def clock_pulse(self):
        if "".join([str(x) for x in self.program_ram[int(self.PC) - 1][1:5]]) == "0100":
            return False

        a, b = self.micro_assembler.disassemble(int(self.CAR), self.micro_program_ram[int(self.CAR)])
        print(int(self.CAR), a if a else "", b)

        word = list(map(str, self.micro_program_ram[int(self.CAR)].bits))
        self.F1.instruction("".join(word[0:3]))
        self.F2.instruction("".join(word[3:6]))
        self.F3.instruction("".join(word[6:9]))

        if self.CD.instruction("".join(word[9: 11])):
            self.BR.instruction("".join(word[11: 13]), True)
        else:
            self.BR.instruction("".join(word[11: 13]), False)

        return True
