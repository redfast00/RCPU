import RCPU.emulator.cpu as cpu

import argparse
import struct

parser = argparse.ArgumentParser(description='Execute a binary.')

parser.add_argument('--infile', type=argparse.FileType('rb'), required=True)
parser.add_argument('--quiet', action='store_false')
args = parser.parse_args()

binary = args.infile.read()
# Load binary into tuple
to_load = struct.unpack("H" * (len(binary) / 2), binary)
c = cpu.CPU()
c.RAM.load(to_load)
while c.running:
    c.step()
    print(c.registers)