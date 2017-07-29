from .utils import execute_code

def test_basic():
    program = '''
        .text
        .global main:
        main:
        HLT
    '''
    c = execute_code(program)
    for i in range(4):
        assert c.registers.get(i) == 0
    assert c.registers.sp == 0

def test_resources():
    program = '''
        .data
        .teststr string 'Hello'
        .testnum 20
        .text
        .global main:
        main:
        LDV A, .teststr
        LDV B, .testnum
        HLT
    '''
    c = execute_code(program)
    assert c.kernel.read_string(c.registers.get(0)) == "Hello"
    assert c.registers.get(1) == 20
