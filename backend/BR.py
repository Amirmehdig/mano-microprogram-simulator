from backend.register import Register


class Branch:
    def __init__(self, cpu):
        self.cpu = cpu
        self.br = {
            '00': self.jmp_func,
            '01': self.call_func,
            '10': self.ret_func,
            '11': self.map_func
        }

    def instruction(self, br_code, flag=True):
        self.br[br_code](flag)

    def jmp_func(self, flag):
        if flag:
            self.cpu.CAR.word_to_register(self.cpu.micro_program_ram[int(self.cpu.CAR)][13:20])
        else:
            self.cpu.CAR.increment()

    def call_func(self, flag):
        if flag:
            tmp = Register(7)
            tmp.write(self.cpu.CAR)
            tmp.increment()
            self.cpu.CAR.word_to_register(self.cpu.micro_program_ram[int(self.cpu.CAR)][13:20])
            self.cpu.SBR.write(tmp)
        else:
            self.cpu.CAR.increment()

    def ret_func(self, flag):
        self.cpu.CAR.write(self.cpu.SBR)

    def map_func(self, flag):
        tmp = [0, 0, 0, 0, 0, 0]
        tmp[1: 4] = self.cpu.DR.bits[1: 4]
        self.cpu.CAR.word_to_register(tmp)
