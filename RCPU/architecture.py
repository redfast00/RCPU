MAX_VALUE = 0xFFFF
MAX_VALUE_LDV = 0x3FF
MAX_MEM_LDA = 0x3FF
MAX_MEM_LDM = 0x3FF
MAX_MEM_JMP = 0x3FF
instruction_mapping = {
    0: "MOV",
    1: "LDV",
    2: "LDA",
    3: "LDM",
    4: "LDR",
    5: "LDP",
    6: "ATH",
    7: "CAL",
    8: "RET",
    9: "JLT",
    10: "PSH",
    11: "POP",
    12: "SYS",
    13: "HLT",
    14: "JMP",
    15: "JMR"
}
register_mapping = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D'
}
alu_instruction_mapping = {
    0: 'ADD',
    1: 'SUB',
    2: 'MUL',
    3: 'DIV',
    4: 'LSH',
    5: 'RSH',
    6: 'AND',
    7: 'OR',
    8: 'XOR',
    9: 'NOT',
    10: "INC",
    11: "DEC"
}
