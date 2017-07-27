import RCPU.assembler.assembler as assembler
from RCPU.assembler.preprocessor import preprocess
import argparse
import struct

from pprint import pprint

parser = argparse.ArgumentParser(description='Assemble some assembly code.')

parser.add_argument('--infile', type=argparse.FileType('r'), required=True)
parser.add_argument('--outfile', type=argparse.FileType('wb'), required=True)
parser.add_argument('--quiet', action='store_false')

args = parser.parse_args()

lines = args.infile.readlines()
data, text = preprocess(lines)
pprint([data, text])

resourcetable = assembler.create_resourcetable(data)
pprint(resourcetable)
# Replace entrypoint with a JMP instruction to that label
text = assembler.replace_entrypoint(text)
# Expand text section: turns all pseudo-instructions into real instructions
text = assembler.expand_all(text)
# Replace labels with their locations in the binary
text = assembler.replace_labels(text)
# Insert references to resourcetable
text, datasection = assembler.generate_datasection(text, resourcetable)
# Translate instructions into machine code
binary = assembler.translate_all(text)
binary += datasection

packed = [struct.pack('H', instruction) for instruction in binary]
for instruction in packed:
    args.outfile.write(instruction)