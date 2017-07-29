import RCPU.assembler.assembler as assembler
from RCPU.assembler.preprocessor import preprocess
import argparse
import struct
import logging

from pprint import pprint, pformat

def pretty_log_debug(stage, msg, *args, **kwargs):
    logging.debug(stage+'\n'+pformat(msg), *args, **kwargs)

def assemble(lines):
    data, text = preprocess(lines)
    resourcetable = assembler.create_resourcetable(data)
    # Replace entrypoint with a JMP instruction to that label
    text = assembler.replace_entrypoint(text)
    pretty_log_debug('preprocessed',{
        'resourcetable':resourcetable,
        'text':text,
        'data':data
    })
    # Expand text section: turns all pseudo-instructions into real instructions
    text = assembler.expand_all(text)
    # Replace labels with their locations in the binary
    text = assembler.replace_labels(text)
    pretty_log_debug('expanded',{
        'text':text,
    })
    # Insert references to resourcetable
    text, datasection = assembler.generate_datasection(text, resourcetable)
    # Translate instructions into machine code
    binary = assembler.translate_all(text)
    binary += datasection
    return binary

def pack_binary(binary):
    return [struct.pack('H', instruction) for instruction in binary]

def main():
    parser = argparse.ArgumentParser(description='Assemble some assembly code.')

    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('outfile', type=argparse.FileType('wb'))
    parser.add_argument('--debug', action='store_const', const=logging.DEBUG, default=logging.WARNING, dest='loglevel')
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format='%(levelname)s: %(message)s')
    lines = args.infile.readlines()
    assembled = assemble(lines)
    packed = pack_binary(assembled)
    for instruction in packed:
        args.outfile.write(instruction)
if __name__ == '__main__':
    main()