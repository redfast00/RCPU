import RCPU.emulator.registers as registers

def test_persistence():
    r = registers.Registers()
    r.set(0b00, 26)
    assert r.get(0b00) == 26
def test_init():
    r = registers.Registers()
    for i in range(4):
        assert r.get(i) == 0
