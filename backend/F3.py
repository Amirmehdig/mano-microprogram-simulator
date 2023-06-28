from CPU import CPU


class F3:
    def __init__(self, cpu: CPU):
        self.cpu = cpu
        self.opcode = {'000': self.nop_func,
                       '001': self.xor_func,
                       '010': self.com_func,
                       '011': self.shl_func,
                       '100': self.shr_func,
                       '101': self.incpc_func,
                       '110': self.artpc_func
                       }

    def instruction(self, op):
        self.opcode[op]()

    def nop_func(self):
        pass

    def xor_func(self):
        self.cpu.AC.write(self.cpu.AC ^ self.cpu.DR)

    def com_func(self):
        self.cpu.AC.complement()

    def shl_func(self):
        self.cpu.AC.left_shift(0)

    def shr_func(self):
        self.cpu.AC.right_shift(self.cpu.AC.bits[0])

    def incpc_func(self):
        self.cpu.PC.increment()

    def artpc_func(self):
        self.cpu.PC.write(self.cpu.AR)


