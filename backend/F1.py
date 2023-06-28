class F1:

    def __init__(self, cpu):
        self.cpu = cpu
        self.opcode = {'000': self.nop_func,
                       '001': self.add_func,
                       '010': self.clrac_func,
                       '011': self.incac_func,
                       '100': self.drtac_func,
                       '101': self.drtar_func,
                       '110': self.pctar_func,
                       '111': self.write_func
                       }

    def instruction(self, op):
        self.opcode[op]()

    def nop_func(self):
        pass

    def add_func(self):
        self.cpu.AC.write((self.cpu.AC + self.cpu.DR)[0])

    def clrac_func(self):
        self.cpu.AC.master_reset()

    def incac_func(self):
        self.cpu.AC.increment()

    def drtac_func(self):
        self.cpu.AC.write(self.cpu.DR)

    def drtar_func(self):
        self.cpu.AR.write_to_smaller_reg(self.cpu.DR)

    def pctar_func(self):
        self.cpu.AR.write(self.cpu.PC)

    def write_func(self):
        self.cpu.program_ram[int(self.cpu.AR)].write(self.cpu.DR)
