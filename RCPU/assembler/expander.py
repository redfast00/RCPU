from RCPU.architecture import instruction_mapping

def expand_instruction(line):
    instruction, arguments = parser.parse_instruction(line)
    if instruction in instruction_mapping.keys():
        # No need to expand this
        return [line]