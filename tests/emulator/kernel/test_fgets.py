from __future__ import unicode_literals
from .utils import init_kernel

def test_read():
    for to_test in ["test\n", "test test", "testtestt"]:
        k = init_kernel(stdin=to_test)

        k.stack.push(0)  # Push stream_num
        k.stack.push(10) # Push size
        k.stack.push(0)  # Push location in memory to write the string to
        k.stack.push(1)  # Push syscall number
        k.syscall()
        assert k.read_string(0) == to_test.strip()
        assert k.stack.pop() == len(to_test.strip())

def test_cut_off_at_size():
    size = 10
    k = init_kernel(stdin=u"A" * 20)
    k.stack.push(0)    # Push stream_num
    k.stack.push(size) # Push size
    k.stack.push(0)    # Push location in memory to write the string to
    k.stack.push(1)    # Push syscall number
    k.syscall()
    assert k.read_string(0) == "A" * (size - 1)