from .utils import execute_code

def test_ADD():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            LDV B, 10
            ADD A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 40
    assert c.registers.get(1) == 10

def test_LSH():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            LSH A, 3
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 30 << 3

def test_RSH():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            RSH A, 3
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 30 >> 3

def test_SUB():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            LDV B, 10
            SUB A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 20
    assert c.registers.get(1) == 10

def test_SUBS():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            LDV B, 10
            SUBS A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 30
    assert c.registers.get(1) == 20

def test_MUL():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            LDV B, 10
            MUL A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 300
    assert c.registers.get(1) == 10

def test_DIV():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            LDV B, 10
            DIV A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 3
    assert c.registers.get(1) == 10
    # Check that flooring works properly
    program = '''
        .text
        .global main:
        main:
            LDV A, 38
            LDV B, 10
            DIV A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 3
    assert c.registers.get(1) == 10

def test_DIVS():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            LDV B, 10
            DIVS A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 30
    assert c.registers.get(1) == 3

def test_AND():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            LDV B, 10
            AND A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 30 & 10
    assert c.registers.get(1) == 10

def test_OR():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            LDV B, 10
            OR A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 30 | 10
    assert c.registers.get(1) == 10

def test_XOR():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            LDV B, 10
            XOR A, B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 30 ^ 10
    assert c.registers.get(1) == 10

def test_NOT():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            NOT A
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 0xFFFF - 30

def test_INC():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            INC A
            INC A
            INC B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 32
    assert c.registers.get(1) == 1

def test_DEC():
    program = '''
        .text
        .global main:
        main:
            LDV A, 30
            DEC A
            DEC A
            DEC B
            HLT
    '''
    c = execute_code(program)
    assert c.registers.get(0) == 28
    assert c.registers.get(1) == 0xFFFF