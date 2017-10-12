from __future__ import unicode_literals
from .utils import init_kernel


def test_read():
    for to_test in ["a", "b", "\n", "test"]:
        k = init_kernel(stdin=to_test)

        k.stack.push(0)  # Push stream_num
        k.stack.push(2)  # Push syscall number
        k.syscall()
        assert k.stack.pop() == ord(to_test[0])


def test_multiple_read():
    to_test = "Hello World! 123\t\n"
    k = init_kernel(stdin=to_test)
    for char in to_test:
        k.stack.push(0)
        k.stack.push(2)
        k.syscall()
        assert k.stack.pop() == ord(char)
