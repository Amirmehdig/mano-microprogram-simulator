import re


def find_by_value(dict, value):
    for key, v in dict.items():
        if v == value:
            return key
    return None


def to_bin(value: int, size):
    if value < 0:
        return list(
            map(int, list(bin(value & (2 ** size - 1))[2:]))
        )[-size:]
    else:
        return list(
            map(int, list(bin(value)[2:].zfill(size)))
        )[-size:]


class ProgramAssembler:
    pattern = re.compile("^(([\w][\w\d]{0,2})[ ]*,)?[ ]*(([\w]+)( ([\d-]+|[\w][\w\d]{0,2})( I)?)?)$")

    def __init__(self, code: str, micro_table):
        self.code_lines = [line.upper() for line in code.split("\n")]
        self.micro_table = micro_table

    def assemble(self):
        self.label_dict = self.first_pass()
        self.res_dict = self.second_pass()

    def first_pass(self):
        label_dict = {}

        LC = 0
        for line in self.code_lines:
            line = line.strip()

            match = self.pattern.match(line).groups()
            if match[0] is not None:
                label_dict[match[1]] = LC
            elif match[3] == "ORG":
                LC = int(match[5], 16) - 1
            elif match[2] == "END":
                break
            LC += 1

        return label_dict

    def second_pass(self):
        res_dict = {}

        LC = 0
        for line in self.code_lines:
            line = line.strip()

            match = self.pattern.match(line).groups()
            if match[3] == "ORG":
                LC = int(match[5], 16) - 1
            elif match[3] == "END":
                break
            elif match[3] == "DEC":
                res_dict[LC] = to_bin(int(match[5]), 16)
            elif match[3] == "HEX":
                res_dict[LC] = to_bin(int(match[5], 16), 16)
            elif match[4] is not None:  # MRI
                if match[5].isnumeric():
                    address = to_bin(int(match[5], 16), 11)
                else:
                    address = to_bin(self.label_dict[match[5]], 11)
                opcode = list(map(int, list(bin(self.micro_table[match[3]])[2:-2].zfill(4))))
                I = [1] if match[6] is not None else [0]

                res_dict[LC] = I + opcode + address
            else:
                if match[3] == "HLT":
                    self.hlt_pos = LC

                opcode = list(map(int, list(bin(self.micro_table[match[3]])[2:-2].zfill(4))))
                res_dict[LC] = [0] + opcode + [0] * 11

            LC += 1

        return res_dict

    def disassemble(self, i, word, after_hlt=False):
        word = list(map(str, word))

        label = find_by_value(self.label_dict, i)

        if not after_hlt:
            address = find_by_value(self.label_dict, int("".join(word[5:16]), 2))
            if address is None:
                address = hex(int("".join(word[5:16]), 2))[2:].zfill(2)

            opcode = find_by_value(self.micro_table, int("".join(word[1:5]) + "00", 2))

            if opcode == "HLT":
                instruction = f"{opcode}"
            else:
                instruction = f"{opcode} {address}"

            if word[0] == "1":
                instruction += " I"
        else:
            instruction = f"HEX {hex(int(''.join(word), 2))[2:].zfill(4)}"

        return f"{label}," if label else None, instruction


if __name__ == "__main__":
    code = """ORG 0
ADD A2 
STORE A3
HLT
ORG 10
A2, DEC 15
A3, HEX 5
END"""
    micro_table = {'ADD': 0, 'BRANCH': 4, 'OVER': 6, 'STORE': 8, 'EXCHANGE': 12, 'HLT': 16, 'FETCH': 64, 'INDRCT': 67}

    a = ProgramAssembler(code, micro_table)
    a.assemble()
    print(a.label_dict)
    for i in a.res_dict:
        print(i, a.res_dict[i])

    after_hlt = False
    for i in a.res_dict:
        label, instruction = a.disassemble(i, a.res_dict[i], after_hlt)
        print(label, instruction)
        if instruction == "HLT":
            after_hlt = True
