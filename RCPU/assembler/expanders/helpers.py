from RCPU.architecture import register_mapping

def get_free_register(registers_used):
    '''Returns a register that is not in use'''
    for register in register_mapping.values():
        if register not in registers_used:
            return register

def fill_instructions(instructions, **kwargs):
    '''Formats instructions with values given in **kwargs'''
    return [instruction.format(**kwargs) for instruction in instructions]