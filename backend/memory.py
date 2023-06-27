from register import Register

class Memory:
    def __init__(self, word_size: int, capacity: int):
        self.ram = []
        for i in range(capacity):
            reg = Register(word_size)
            self.ram.append(reg)

    def __getitem__(self, item):
        return self.ram[item]

    def __setitem__(self, key, value):
        self.ram[key] = value
