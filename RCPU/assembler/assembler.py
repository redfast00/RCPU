from . import parser
from . import translator
from . import utils
from RCPU.assembler.expanders.expander import expand_instruction
from RCPU.architecture import MAX_VALUE

def create_resourcetable(data):
    '''Creates a resourcetable from the datasection that maps a name (like .value) to a value (like 5).'''
    resourcetable = {}
    for line in data:
        name, value = parser.parse_resource(line)
        resourcetable[name] = value
    return resourcetable

def expand(text):
    '''Expands pseudo-instructions into real instructions, supports symbolic arguments'''
    newtext = []
    for line in text:
        if parser.is_instruction(line):
            # Copy list of expanded instructions on the end of newtext
            newtext.extend(expand_instruction(line))
        else:
            # Just add label in
            newtext.append(line)
    return newtext

def expand_all(text):
    '''Expands pseudo-instructions until all pseudo-instructions are converted to real instructions'''
    while text != expand(text):
        text = expand(text)
    return text

def replace_labels(text):
    '''Replaces labels in text with their locations in text'''
    labels = {}
    first_pass = []
    second_pass = []
    current_location = 0
    # Put all labels in dictionary
    for line in text:
        if parser.is_label(line):
            # Add label to dictionary and don't copy it into the second pass
            labels[line] = current_location
        else:
            first_pass.append(line)
            current_location += 1
    # Translate all labels
    for line in first_pass:
        assert parser.is_instruction(line)
        instruction, arguments = parser.parse_instruction(line)
        # Replace labels with their location in memory
        arguments = [str(labels[arg]) if parser.is_label(arg) else arg for arg in arguments]
        translated = parser.unparse_instruction(instruction, arguments)
        second_pass.append(translated)
    return second_pass

def generate_datasection(text, resourcetable):
    '''Creates the binary datasection at the end of a binary and
        converts symbolic values in text to values referring to memory'''
    base_address = len(text)
    newtext = []
    datasection = []
    used_resourcetable = {}
    for line in text:
        # Should all be instructions by now
        instruction, arguments = parser.parse_instruction(line)
        newarguments = []
        for argument in arguments:
            if parser.is_reference(argument):
                value = resourcetable[argument]
                if type(value) == int:
                    assert 0 <= value and value <= MAX_VALUE
                    argument = str(value)
                elif type(value) == str:
                    if value not in used_resourcetable:
                        address = len(datasection) + base_address
                        for char in value:
                            datasection.append(ord(char))
                        datasection.append(0)
                        used_resourcetable[value] = address
                    argument = str(used_resourcetable[value])
                else:
                    raise utils.AssemblerException('Unsupported resource type')
            newarguments.append(argument)
        newtext.append(parser.unparse_instruction(instruction, newarguments))
    return newtext, datasection

def translate_all(text):
    '''Translates all textual instructions in the text section into binary instructions.'''
    binary = []
    t = translator.InstructionTranslator
    for line in text:
        instruction, arguments = parser.parse_instruction(line)
        binary.append(t.translate(instruction, arguments))
    return binary

def replace_entrypoint(text):
    '''Replaces the entrypoint (.global) with a JMP to the location of the entrypoint.'''
    # TODO: replace this with a long jump in case entrypoint is above 0x3FF
    entrypoint = parser.parse_global(text[0])
    text[0] = parser.unparse_instruction("JMP", [entrypoint])
    return text