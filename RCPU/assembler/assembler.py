from . import parser
from . import translator
from . import utils
from . import resources
import string
from RCPU.safe_eval import safe_eval
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
    # TODO refractor this
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
        iterator = iter(line)
        translated = ''
        for char in iterator:
            current = ''
            try:
                while char in parser.ALLOWED_LABEL_NAME_CHARS:
                    current += char
                    char = next(iterator)
                current += char
            except StopIteration:
                pass
            if char == parser.LABEL_CHAR:
                translated += str(labels[current])
            else:
                translated += current
        # instruction, arguments = parser.parse_instruction(line)
        # # Replace labels with their location in memory
        # arguments = [str(labels[arg]) if parser.is_label(arg) else arg for arg in arguments]
        # translated = parser.unparse_instruction(instruction, arguments)
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
        parts = resources.split_resource(line)
        generated = ''
        for part in parts:
            if parser.is_reference(part):
                value = resourcetable[part]
                if type(value) == int:
                    assert 0 <= value and value <= MAX_VALUE
                    part = str(value)
                elif type(value) == str:
                    if value not in used_resourcetable:
                        address = len(datasection) + base_address
                        for char in value:
                            datasection.append(ord(char))
                        datasection.append(0)
                        used_resourcetable[value] = address
                    part = str(used_resourcetable[value])
                else:
                    raise utils.AssemblerException('Unsupported resource type')
            generated += part
        newtext.append(generated)
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

def replace_symbolic(line):
    instruction, arguments = parser.parse_instruction(line)
    arguments = [
        str(safe_eval(argument))
        if (argument.startswith('(') and argument.endswith(')'))
        else argument
        for argument in arguments
    ]
    return parser.unparse_instruction(instruction, arguments)

def eval_expressions(lines):
    return [replace_symbolic(line) for line in lines]