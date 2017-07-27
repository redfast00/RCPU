import RCPU.emulator.kernel as kernel
import RCPU.emulator.ram as ram
import RCPU.emulator.stack as stack
import RCPU.emulator.registers as registers

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
    # This will be a number
    k.stack.push(443)
    load_str_into_memory(k.RAM, "this is a test", 20)
    # This is an address of a string
    k.stack.push(20)
    load_str_into_memory(k.RAM, "FMT: %s,%d", 40)
    # This is an address of a string
    k.stack.push(40)
    k.stack.push(0)
    assert k.syscall() == "FMT: this is a test,443"