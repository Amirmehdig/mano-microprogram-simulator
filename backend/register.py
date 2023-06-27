class Register:
    def __init__(self, size: int = 16) -> None:
        self.size = size
        self.bits = [0] * size

    def __getitem__(self, item):
        return self.bits[item]

    def __setitem__(self, key, value):
        self.bits[key] = value

    def __int__(self):
        result = 0
        for bit in self.bits[1:]:
            result = (result << 1) | bit
        if self.bits[0]:
            result -= 2 ** (self.size - 1)
        return result

    def __add__(self, other):
        def full_adder(a, b, c):
            carry_out = 0
            sum_res = a ^ b ^ c
            if a + b + c > 1:
                carry_out = 1
            return sum_res, carry_out
        carry = 0
        result = Register(self.size)
        for i in range(self.size - 1, -1, -1):
            result[i], carry = full_adder(self.bits[i], other.bits[i], carry)
        return result, carry

    def __imod__(self, value):
        value = int(value)
        self.set_value(value)
        return self

    def __ilshift__(self, other):
        self.set_value(int(other))
        return self

    def __iand__(self, other):
        for i in range(self.size):
            self.data[i] = self.data[i] & other.data[i]
        return self

    def increment(self):
        self %= int(self) + 1

    def master_reset(self):
        self %= 0

    def right_shift(self, serial_in):
        temp_data = [serial_in] + self.bits
        out = temp_data.pop()
        self.bits = temp_data
        return out

    def left_shift(self, serial_in):
        temp_data = self.bits + [serial_in]
        out = temp_data.pop(0)
        self.bits = temp_data
        return out

    def complement(self):
        for i in range(self.size):
            self.bits[i] = int(not self.bits[i])

    def set_value(self, value):
        if -32768 <= value <= 32767:
            if value < 0:
                self.bits = list(
                    map(int, list(bin(value&(2**self.size - 1))[2:])))[-self.size:]
            else:
                self.bits = list(
                    map(int, list(bin(value)[2:].zfill(self.size))))[-self.size:]

    def hex(self):
        result = 0
        for bit in self.bits:
            result = (result << 1) | bit
        return hex(result)
