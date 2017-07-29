from .utils import execute_code

def test_LDV16():
    program = '''
        .text
        .global main:
        main:
            LDV16 A, {value}
            HLT
    '''
    for i in [0, 0xFF, 0xEFF, 0xFFFF]:
        c = execute_code(program.format(value=i))
        assert c.registers.get(0) == i

def test_SWP():
    program = '''
        .text
        .global main:
        main:
            LDV A, 123
            LDV B, 321
            SWP A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 321
    assert c.registers.get(1) == 123