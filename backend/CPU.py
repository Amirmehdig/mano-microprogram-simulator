from memory import Memory
from register import Register

class CPU:
    def __init__(self):
        self.program_ram = Memory(16, 2048)

        self.AR = Register(11)
        self.PC = Register(11)
        self.AC = Register(16)
        self.DR = Register(16)

        self.micro_program_ram = Memory(20, 128)

        self.CAR = Register(7)
        self.SBR = Register(7)

