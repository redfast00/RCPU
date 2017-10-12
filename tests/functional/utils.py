from RCPU.assemble import assemble
from RCPU.emulate import cpu_loop
import RCPU.emulator.cpu as cpu


def execute_code(code):
    program = code.splitlines()
    assembled = assemble(program)
    c = cpu.CPU()
    c.RAM.load(assembled)
    cpu_loop(c)
    return c
