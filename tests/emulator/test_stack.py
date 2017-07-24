import RCPU.emulator.stack as stack

def test_push_pop():
    s = stack.Stack()
    s.push(12)
    assert s.pop() == 12
def test_order():
    s = stack.Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1