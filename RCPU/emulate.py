import RCPU.emulator.cpu as cpu

import argparse
import struct
import logging

def unpack(raw):
    '''Unpacks raw into a list of binary instructions'''
    return struct.unpack("H" * (len(raw) // 2), raw)

def cpu_loop(c):
    while c.running:
        c.step()
        logging.debug(c.registers)


def main(): #pragma: no cover
    parser = argparse.ArgumentParser(description='Execute a binary.')
    parser.add_argument('infile', type=argparse.FileType('rb'))
    parser.add_argument('--debug', action='store_const', const=logging.DEBUG, default=logging.WARNING, dest='loglevel')
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format='%(levelname)s: %(message)s')

    # Load binary from disk into CPU
    filecontent = args.infile.read()
    c = cpu.CPU()
    unpacked = unpack(filecontent)
    c.RAM.load(unpacked)
    # Main CPU loop
    cpu_loop(c)

if __name__ == '__main__':
    main()