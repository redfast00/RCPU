import RCPU.emulator.ram as ram


def test_persistent():
    r = ram.RAM(20)
    r.set(4, 25)
    assert r.get(4) == 25


def test_initialisation():
    r = ram.RAM(20)
    for i in range(20):
        assert r.get(i) == 0


def test_load_from_zero():
    r = ram.RAM(20)
    r.set(0, 1)
    r.set(1, 2)
    r.set(2, 3)
    to_load = [4, 5]
    r.load(to_load)
    assert r.get(0) == 4
    assert r.get(1) == 5
    assert r.get(2) == 3
