from tests.functional.utils import execute_code

def test_JGE():
    program = '''
        .text
        .global main:
            main:
                LDV A, 456
                LDV B, 123
                LDV C, positive:
                JGE B, C
                HLT
            positive:
                LDV C, 789
                HLT
    '''
    c = execute_code(program)
    for reg, val in enumerate([456, 123, 789, 0]):
        assert c.registers.get(reg) == val

def test_JEQ():
    program = '''
        .text
        .global main:
            main:
                LDV A, 123
                LDV B, {value}
                LDV C, positive:
                LDV D, 80
                JEQ B, C
                LDV C, 321
                HLT
            positive:
                LDV C, 789
                HLT
    '''
    c = execute_code(program.format(value=123))
    assert c.registers._gp == [123,123,789,80]
    c = execute_code(program.format(value=456))
    assert c.registers._gp == [123,456,321,80]
    c = execute_code(program.format(value=12))
    assert c.registers._gp == [123,12,321,80]