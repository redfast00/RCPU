from .utils import execute_code


def test_push():
    c = execute_code('''
        .text
        .global main:
        main:
        LDV A, 20
        PSH A
        LDV B, 22
        PSH B
        LDV C, 24
        PSH C
        LDV D, 26
        PSH D
        HLT
    ''')
    for i in [26, 24, 22, 20]:
        assert c.stack.pop() == i


def test_pop():
    c = execute_code('''
        .text
        .global main:
        main:
        LDV A, 20
        PSH A
        LDV B, 22
        PSH B
        LDV C, 24
        PSH C
        LDV D, 26
        PSH D
        POP A
        POP B
        POP C
        POP D
        HLT
    ''')
    for reg, value in enumerate([26, 24, 22, 20]):
        assert c.registers.get(reg) == value
