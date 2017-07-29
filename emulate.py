import RCPU.emulator.cpu as cpu

import argparse
import struct
import logging

def unpack(raw):
    '''Unpacks raw into a list of binary instructions'''
    return struct.unpack("H" * (len(raw) / 2), raw)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute a binary.')
    parser.add_argument('infile', type=argparse.FileType('rb'))
    parser.add_argument('--debug', action='store_const', const=logging.DEBUG, default=logging.WARNING, dest='loglevel')
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format='%(levelname)s: %(message)s')

    # Load binary from disk
    filecontent = args.infile.read()
    binary = unpack(filecontent)
    c = cpu.CPU()
    c.RAM.load(binary)
    # Main CPU loop
    while c.running:
        c.step()
        logging.debug(c.registers)
