from backend.register import Register


class F2:
    def __init__(self, cpu):
        self.cpu = cpu
        self.opcode = {'000': self.nop_func,
                       '001': self.sub_func,
                       '010': self.or_func,
                       '011': self.and_func,
                       '100': self.read_func,
                       '101': self.actdr_func,
                       '110': self.incdr_func,
                       '111': self.pctdr_func
                       }

    def instruction(self, op):
        self.opcode[op]()

    def nop_func(self):
        pass

    def sub_func(self):
        temp = Register(16)
        temp.set_value(1)
        res = Register()
        res.write(self.cpu.AC + self.cpu.DR.complement() + temp)
        self.cpu.AC.write(res)

    def or_func(self):
        self.cpu.AC.write(self.cpu.AC | self.cpu.DR)

    def and_func(self):
        self.cpu.AC.write(self.cpu.AC & self.cpu.DR)

    def read_func(self):
        self.cpu.DR.write(self.cpu.program_ram[int(self.cpu.AR)])

    def actdr_func(self):
        self.cpu.DR.write(self.cpu.AC)

    def incdr_func(self):
        self.cpu.DR.increment()

    def pctdr_func(self):
        self.cpu.DR.write_to_bigger_reg(self.cpu.PC)
