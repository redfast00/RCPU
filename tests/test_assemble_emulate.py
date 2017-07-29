from RCPU.assemble import assemble
from RCPU.emulate import cpu_loop
import RCPU.emulator.cpu as cpu

def test_basic():
    program = '''
        .text
        .global main:
        main:
        HLT
    '''.splitlines()
    assembled = assemble(program)
    c = cpu.CPU()
    c.RAM.load(assembled)
    cpu_loop(c)
    for i in range(4):
        assert c.registers.get(i) == 0
    assert c.registers.sp == 0

def test_printf(capsys):
    program = '''
        .data
          .format string '%d test'
          .printf 0

        .text
          .global main:

        main:
          ; Print 20
          LDV A, 20
          PSH A
          LDV A, .format
          PSH A
          LDV A, .printf
          PSH A
          SYS
          HLT
    '''.splitlines()
    assembled = assemble(program)
    c = cpu.CPU()
    c.RAM.load(assembled)
    cpu_loop(c)
    out, err = capsys.readouterr()
    assert out == "20 test"
    assert c.registers.sp == 0

