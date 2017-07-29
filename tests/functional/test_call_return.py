from .utils import execute_code

def test_CAL_RET():
    program = '''
        .data
        .text
        .global main:
        test_func:
            LDV A, 123
            RET
        main:
            LDV A, test_func:
            CAL A
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 123