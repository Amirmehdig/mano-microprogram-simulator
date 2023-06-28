class Condition:
    def __init__(self, cpu):
        self.cpu = cpu
        self.cd = {
            '00': self.u_func,
            '01': self.i_func,
            '10': self.s_func,
            '11': self.z_func
        }

    def instruction(self, code):
        return self.cd[code]()

    def u_func(self):
        return True

    def i_func(self):
        if self.cpu.DR.bits[0] == 1:
            return True
        else:
            return False

    def s_func(self):
        if self.cpu.AC.bits[0] == 0:
            return True
        else:
            return False

    def z_func(self):
        if int(self.cpu.AC) == 0:
            return True
        else:
            return False
