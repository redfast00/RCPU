import RCPU.emulator.cpu as cpu


def test_decode():
    c = cpu.CPU()
    instruction = 0b0000000000000000
    assert c.decode(instruction) == ("MOV", 0b000000000000)
    instruction = 0b0000000000001111
    assert c.decode(instruction) == ("JMR", 0b000000000000)
    instruction = 0b1000000000001110
    assert c.decode(instruction) == ("JMP", 0b100000000000)


def test_fetch():
    c = cpu.CPU()
    a = 0b1000000000001110
    b = 0b1000000000001111
    c.RAM.load([a, b])
    assert c.fetch() == a
    c.registers.ip += 1
    assert c.fetch() == b


def test_step():
    c = cpu.CPU()
    # LDV A, 512
    a = 0b1000000000000001
    c.RAM.load([a])
    assert c.registers.get(0b00) == 0
    assert c.registers.ip == 0
    c.step()
    assert c.registers.get(0b00) == 0b1000000000
    assert c.registers.ip == 1
