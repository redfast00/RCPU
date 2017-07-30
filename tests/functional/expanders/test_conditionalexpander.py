from tests.functional.utils import execute_code

def test_JGE():
    program = '''
        .text
        .global main:
            main:
                LDV A, 25
                LDV B, 10
                LDV C, positive:
                JGE B, C
                HLT
            positive:
                LDV C, 16
                HLT
    '''
    c = execute_code(program)
    for reg, val in enumerate([25, 10, 16, 0]):
        assert c.registers.get(reg) == val