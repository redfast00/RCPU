import RCPU.emulator.kernel as kernel
import RCPU.emulator.ram as ram
import RCPU.emulator.stack as stack
import RCPU.emulator.registers as registers

import io

def init_kernel(stdin=None):
    r = ram.RAM(256)
    # Fill up RAM with 1's to be certain that 0 termination works
    r.load([1] * 256)
    s = stack.Stack(registers.Registers())
    k = kernel.Kernel(r, s)
    if stdin:
        k.filenumber_mapping[0] = io.StringIO(stdin)
    return k