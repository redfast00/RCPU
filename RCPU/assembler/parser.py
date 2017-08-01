from . import utils
from ast import literal_eval
import string

LABEL_CHAR = ':'
ALLOWED_LABEL_NAME_CHARS = string.ascii_letters + string.digits + '_-'

def parse_resource(line):
    parts = line.split(' ', 2)
    if len(parts) == 2:
        return parts[0], int(parts[1])
    elif len(parts) == 3 and parts[1] == 'string':
        return parts[0], literal_eval(parts[2])
    elif len(parts) == 3 and parts[1] == 'allocate':
        # Allocate some memory for later use
        # String length is one less than allocated memory because of NUL terminator
        size = int(parts[2])
        if size < 1:
            raise utils.AssemblerException("Size of allocated memory too small: {}".format(line))
        return parts[0], '_' * (size - 1)
    else:
        raise utils.AssemblerException("Unknown resource type in .data: {}".format(line))

def parse_global(line):
    assert line.startswith(".global")
    parts = line.split()
    assert len(parts) == 2
    return parts[1]

def is_label(line):
    # TODO check valid label chars
    return line.endswith(LABEL_CHAR) and ' ' not in line

def is_instruction(line):
    return not is_label(line)

def is_reference(part):
    return part.startswith(".")

def parse_instruction(line):
    parts = line.split(' ', 1)
    if len(parts) > 1:
        # Instruction with arguments
        instruction, arguments = parts
        # Split arguments
        argparts = arguments.split(",")
        arguments = [part.strip() for part in argparts]
    else:
        instruction = parts[0]
        arguments = []
    return instruction.upper(), arguments

def unparse_instruction(instruction, arguments):
    if arguments:
        return instruction + ' ' + ','.join(arguments)
    else:
        return instruction