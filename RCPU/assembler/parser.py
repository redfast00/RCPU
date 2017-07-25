LABEL_CHAR = ':'

def parse_resource(line):
    parts = line.split(maxsplit=2)
    if len(parts) == 2:
        return parts[0], int(parts[1])
    elif len(parts) == 3 and parts[1] == 'string':
        return parts[0], parts[2][1:-1]

def is_label(line):
    return line.endswith(LABEL_CHAR) and ' ' not in line

def is_instruction(line):
    return not is_label(line)

def parse_instruction(line):
    parts = line.split(' ', maxsplit=1)
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
