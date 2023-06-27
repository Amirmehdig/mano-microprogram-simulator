# code = '''ORG 0
#     ADD: NOP I CALL INDRCT
#         READ U JMP NEXT
#         ADD U JMP FETCH
#     ORG 4
#     BRANCH: NOP S JMP OVER
#             NOP U JMP FETCH
#     OVER:   NOP I CALL INDRCT
#             ARTPC U JMP FETCH
#     ORG 8
#     STORE: NOP I CALL INDRCT
#            ACTOR U JMP NEXT
#            WRITE U JMP FETCH
#     ORG 12
#     EXCHANGE:   NOP              I CALL INDRCT
#                 READ             U JMP NEXT
#                 ACTOR, DRTAC     U JMP NEXT
#                 WRITE            U JMP FETCH
#     ORG 64
#     FETCH: PCTAR U JMP NEXT
#            READ, INCPC U JMP NEXT
#            DRTAR U JMP MAP
#     INDRCT: READ U JMP NEXT
#             DRTAR U RET'''


class AssemblerMicroProgram:
    def __init__(self, code: str):
        self.lines = code.split('\n')
        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].split()
        self.f1 = {
            'NOP': '000',
            'ADD': '001',
            'CLRAC': '010',
            'INCAC': '011',
            'DRTAC': '100',
            'DRTAR': '101',
            'PCTAR': '110',
            'WRITE': '111'
        }

        self.f2 = {
            'SUB': '001',
            'OR': '010',
            'AND': '011',
            'READ': '100',
            'ACTDR': '101',
            'INCDR': '110',
            'PCTDR': '111'
        }

        self.f3 = {
            'XOR': '001',
            'COM': '010',
            'SHL': '011',
            'SHR': '100',
            'INCPC': '101',
            'ARTPC': '110'
        }

        self.conditions = {
            'U': '00',
            'I': '01',
            'S': '10',
            'Z': '11'
        }

        self.branch = {
            'JMP': '00',
            'CALL': '01',
            'RET': '10',
            'MAP': '11'
        }

    def get_label_table(self):
        res_dict = {}
        current_address = 0
        for i in range(len(self.lines)):
            if self.lines[i][0] == 'ORG':
                current_address = int(self.lines[i][1]) - 1
            if self.lines[i][0][-1] == ':':
                res_dict.__setitem__(self.lines[i][0].replace(':', ''), current_address)
            current_address += 1
        return res_dict

    def get_memory_words(self):
        labels = self.get_label_table()
        res_dict = {}
        current_address = 0
        for i in range(len(self.lines)):
            word = list('0' * 20)
            if self.lines[i][0] == 'ORG':
                current_address = int(self.lines[i][1])
                continue
            if len(self.lines[i]) >= 3:
                for j in range(len(self.lines[i])):
                    if self.lines[i][j][-1] == ',' or self.lines[i][j][0] == ',':
                        self.lines[i][j] = self.lines[i][j].replace(',', '')
                    if self.lines[i][j][-1] == ':':
                        continue
                    if self.lines[i][j] in self.f1:
                        word[0: 3] = self.f1[self.lines[i][j]]
                    if self.lines[i][j] in self.f2:
                        word[3: 6] = self.f2[self.lines[i][j]]
                    if self.lines[i][j] in self.f3:
                        word[6: 9] = self.f3[self.lines[i][j]]
                    if self.lines[i][j] in self.conditions:
                        word[9: 11] = self.conditions[self.lines[i][j]]
                    if self.lines[i][j] in self.branch:
                        word[11: 13] = self.branch[self.lines[i][j]]
                    if self.lines[i][j] in labels:
                        bin_address = bin(labels[self.lines[i][j]])[2:]
                        word[13: 20] = bin_address.zfill(7)
                    if self.lines[i][j] == 'NEXT':
                        bin_address = bin(current_address + 1)[2:]
                        word[13: 20] = bin_address.zfill(7)
            res_dict.__setitem__(current_address, word)
            current_address += 1
        return res_dict

# a = AssemblerMicroProgram(code)
# b = a.get_memory_words()
# print(b)
