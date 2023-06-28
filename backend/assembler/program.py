import re


def to_bin(value: int):
    if value < 0:
        return list(
            map(int, list(bin(value & (2 ** 16 - 1))[2:]))
        )[-16:]
    else:
        return list(
            map(int, list(bin(value)[2:].zfill(16)))
        )[-16:]


class ProgramAssembler:
    pattern = re.compile("^(([\w][\w\d]{0,2})[ ]*,)?[ ]*(([\w]+)( ([\d-]+|[\w][\w\d]{0,2})( I)?)?)$")

    def __init__(self, code: str, micro_table):
        self.code_lines = [line.upper() for line in code.split("\n")]
        self.micro_table = micro_table

    def assemble(self):
        self.label_dict = self.first_pass()
        res = self.second_pass()

        return self.label_dict, res

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
                res_dict[LC] = to_bin(int(match[5]))
            elif match[3] == "HEX":
                res_dict[LC] = to_bin(int(match[5], 16))
            elif match[4] is not None:  # MRI
                if match[5].isnumeric():
                    address = to_bin(int(match[5], 16))
                else:
                    address = to_bin(self.label_dict[match[5]])
                opcode = list(map(int, list(bin(self.micro_table[match[3]])[2:-2].zfill(4))))
                I = [1] if match[6] is not None else [0]

                res_dict[LC] = address + opcode + I
            else:
                opcode = list(map(int, list(bin(self.micro_table[match[3]])[2:-2].zfill(4))))
                res_dict[LC] = [0] * 12 + opcode + [0]

            LC += 1

        return res_dict


if __name__ == "__main__":
    code = """ORG 0
ADD 111 I
ADD A2 
ADD A3 I
STORE 100
STORE 111
ORG 10
A2, DEC 15
A3, HEX 0"""
    micro_table = {'ADD': 0, 'BRANCH': 4, 'OVER': 6, 'STORE': 8, 'EXCHANGE': 12, 'FETCH': 64, 'INDRCT': 67}

    a = ProgramAssembler(code, micro_table)
    labels, res_dict = a.assemble()
    print(labels)
    for i in res_dict:
        print(i, res_dict[i])
