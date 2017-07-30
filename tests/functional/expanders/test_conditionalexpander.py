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