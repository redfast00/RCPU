import RCPU.emulator.registers as registers

def test_persistence():
    r = registers.Registers()
    r.set(0b00, 26)
    assert r.get(0b00) == 26
def test_init():
    r = registers.Registers()
    for i in range(4):
        assert r.get(i) == 0

def test_str():
    r = registers.Registers()
    for i in range(4):
        r.set(i, i)
    assert str(r) == "[0, 1, 2, 3] IP=0, SP=0"
