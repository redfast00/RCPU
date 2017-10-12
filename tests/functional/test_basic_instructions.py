from .utils import execute_code


def test_JMP():
    program = '''
        .data
        .text
        .global main:
        main:
            LDV C, 24
            JMP branch:
        return:
            LDV A, 20
            HLT
        branch:
            ; To make sure we don't just go trough the program
            LDV A, 123
            LDV B, 22
            JMP return:
    '''
    c = execute_code(program)
    for reg, value in enumerate([20, 22, 24]):
        assert c.registers.get(reg) == value


def test_JMR():
    program = '''
        .data
        .text
        .global main:
        main:
            LDV C, 24
            LDV D, branch:
            JMR D
        return:
            LDV A, 20
            LDV B, 22
            HLT
        branch:
            LDV A, 123
            LDV A, return:
            JMR A
    '''
    c = execute_code(program)
    for reg, value in enumerate([20, 22, 24]):
        assert c.registers.get(reg) == value


def test_JLT():
    program = '''
        .data
        .text
        .global main:
        main:
            LDV C, success:
            LDV B, 20
            LDV A, 15
            JLT B, C
            JMP failure:
            HLT
        success:
            LDV A, 123
            HLT
        failure:
            LDV A, 321
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 123
    program = '''
        .data
        .text
        .global main:
        main:
            LDV C, success:
            LDV B, 20
            LDV A, 25
            JLT B, C
            JMP failure:
            HLT
        success:
            LDV A, 123
            HLT
        failure:
            LDV A, 321
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 321


def test_MOV():
    program = '''
        .data
        .text
        .global main:
        main:
            LDV A, 20
            LDV B, 15
            MOV B, A
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 20
    assert c.registers.get(1) == 20
