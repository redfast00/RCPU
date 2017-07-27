import RCPU.emulator.alu as alu

# ALU doesn't store anything, so defined here instead of in every function
a = alu.ALU()

def test_calculate():
    # Addition
    assert a.calculate(0b00000000, 0, 0) == 0
    assert a.calculate(0b00000000, 20, 25) == 45
    # Shift
    assert a.calculate(0b00100100, 0, 856) == 856 << 1

def test_overflow():
    # Overflow addition
    assert a.calculate(0b00000000, 0xFFFF, 0x1) == 0
    # Underflow subtraction
    assert a.calculate(0b00000001, 0x0, 0x1) == 0xFFFF

def test_ADD():
    assert a.ADD(0, 5, 20) == 5 + 20

def test_SUB():
    assert a.SUB(0, 25, 13) == 25 -13

def test_MUL():
    assert a.MUL(0, 30, 20) == 600

def test_DIV():
    assert a.DIV(0, 30, 5) == 6
    assert a.DIV(0, 34, 5) == 6

def test_LSH():
    assert a.LSH(2, 0, 30) == 30 << 2

def test_RSH():
    assert a.RSH(2, 0, 30) == 30 >> 2

def test_AND():
    assert a.AND(0, 5, 67) == 5 & 67

def test_OR():
    assert a.OR(0, 5, 67) == 5 | 67

def test_XOR():
    assert a.XOR(0, 5, 67) == 5 ^ 67

def test_NOT():
    assert a.NOT(0, 0, 0x00) == 0xFFFF
    assert a.NOT(0, 0, 0b0101010111110000) == 0b1010101000001111

def test_INC():
    assert a.INC(0, 25, 0) == 26

def test_DEC():
    assert a.DEC(0, 26, 0) == 25