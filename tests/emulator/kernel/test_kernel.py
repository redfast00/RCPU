from .utils import init_kernel


def test_read_string():
    k = init_kernel()
    k.RAM.load([ord(char) for char in "ABCDE"] + [0])
    assert k.read_string(0) == "ABCDE"
    k.RAM.load([ord(char) for char in "PYTHON"] + [0], base_address=40)
    assert k.read_string(40) == "PYTHON"


def test_write_string():
    k = init_kernel()
    k.write_string(0, "Hello World!")
    assert k.read_string(0) == "Hello World!"
    # Test empty string
    k = init_kernel()
    k.write_string(20, '')
    assert k.read_string(20) == ''


def test_read_string_empty():
    k = init_kernel()
    k.RAM.set(0, 0)
    assert k.read_string(0) == ""
    k.RAM.set(40, 0)
    assert k.read_string(40) == ""
