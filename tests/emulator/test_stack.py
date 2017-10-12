import RCPU.emulator.stack as stack
import RCPU.emulator.registers as registers


def test_push_pop():
    r = registers.Registers()
    s = stack.Stack(r)
    s.push(12)
    assert s.pop() == 12


def test_order():
    r = registers.Registers()
    s = stack.Stack(r)
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1


def test_changing_sp():
    r = registers.Registers()
    s = stack.Stack(r)
    assert r.sp == 0
    s.push(0)
    assert r.sp == 1
    s.push(1)
    assert r.sp == 2
    s.pop()
    assert r.sp == 1
    s.pop()
    assert r.sp == 0
