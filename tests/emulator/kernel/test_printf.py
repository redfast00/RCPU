from .utils import init_kernel
import pytest


def test_printf(capsys):
    k = init_kernel()
    # This loads the third argument of printf, a number
    k.stack.push(443)
    # This loads the second argument of printf, the address of a string
    k.write_string(20, "this is a test")
    k.stack.push(20)
    # This loads the first argument of printf, the format string
    k.write_string(40, "FMT: %s,%d,%%")
    k.stack.push(40)
    # This loads the syscall number
    k.stack.push(0)
    k.syscall()
    out, err = capsys.readouterr()
    assert out == "FMT: this is a test,443,%"


def test_printf_raises():
    k = init_kernel()
    k.write_string(40, "TEST %k")
    k.stack.push(40)
    k.stack.push(0)
    with pytest.raises(Exception) as excinfo:
        k.syscall()
    assert "Error in printf" in str(excinfo.value)


def test_printf_runs_into_end_of_memory(capsys):
    k = init_kernel()
    k.RAM.set(255, ord('A'))
    k.stack.push(255)
    k.stack.push(0)
    k.syscall()
    out, err = capsys.readouterr()
    assert out == 'A'
