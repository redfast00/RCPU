from .utils import execute_code


def test_allocate():
    program = '''
        .data
        .one allocate 1
        .two allocate 1
        .text
        .global main:
        main:
        LDV A, .one
        LDV B, .two
        HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) != c.registers.get(1)
