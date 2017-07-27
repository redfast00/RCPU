import RCPU.emulator.kernel as kernel
import RCPU.emulator.ram as ram
import RCPU.emulator.stack as stack
import RCPU.emulator.registers as registers

import pytest

def init_kernel():
    r = ram.RAM(256)
    # Fill up RAM with 1's to be certain that 0 termination works
    r.load([1] * 256)
    s = stack.Stack(registers.Registers())
    return kernel.Kernel(r, s)

def load_str_into_memory(memory, string, address):
    memory.load([ord(char) for char in string] + [0],base_address=address)

def test_read_string():
    k = init_kernel()
    k.RAM.load([ord(char) for char in "ABCDE"] + [0])
    assert k.read_string(0) == "ABCDE"
    k.RAM.load([ord(char) for char in "PYTHON"] + [0], base_address=40)
    assert k.read_string(40) == "PYTHON"

def test_read_string_empty():
    k = init_kernel()
    k.RAM.set(0, 0)
    assert k.read_string(0) == ""
    k.RAM.set(40, 0)
    assert k.read_string(40) == ""

def test_printf():
    k = init_kernel()
    # This loads the third argument of printf, a number
    k.stack.push(443)
    # This loads the second argument of printf, the address of a string
    load_str_into_memory(k.RAM, "this is a test", 20)
    k.stack.push(20)
    # This loads the first argument of printf, the format string
    load_str_into_memory(k.RAM, "FMT: %s,%d,%%", 40)
    k.stack.push(40)
    # This loads the syscall number
    k.stack.push(0)
    assert k.syscall() == "FMT: this is a test,443,%"

def test_printf_raises():
    k = init_kernel()
    load_str_into_memory(k.RAM, "TEST %k", 40)
    k.stack.push(40)
    k.stack.push(0)
    with pytest.raises(Exception) as excinfo:
        k.syscall()
    assert "Error in printf" in str(excinfo.value)

def test_printf_runs_into_end_of_memory():
    k = init_kernel()
    k.RAM.set(255, ord('A'))
    k.stack.push(255)
    k.stack.push(0)
    assert k.syscall() == "A"