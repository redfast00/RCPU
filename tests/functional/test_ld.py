from .utils import execute_code

def test_LDA_LDM():
    program = '''
        .data
        .teststr string 'Hello'
        .testnum 20
        .memory_loc 500
        .text
        .global main:
        main:
        LDV A, .testnum
        LDM A, .memory_loc
        LDA B, .memory_loc
        HLT
    '''
    c = execute_code(program)
    assert c.registers.get(1) == 20
    assert c.RAM.get(500) == 20

def test_LDR():
    program = '''
        .data
        .teststr string 'ABCDEF'
        .text
        .global main:
        main:
        LDV A, .teststr
        LDR B, A
        HLT
    '''
    c = execute_code(program)
    assert c.registers.get(1) == ord('A')
    assert c.RAM.get(c.registers.get(0)) == ord('A')

def test_LDP():
    program = '''
        .data
        .teststr string 'ABCDEF'
        .replacer string '!'
        .text
        .global main:
        main:
        LDV A, .replacer
        LDR B, A
        LDV A, .teststr
        LDP A, B
        HLT
    '''
    c = execute_code(program)
    assert c.kernel.read_string(c.registers.get(0)) == "!BCDEF"