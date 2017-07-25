from . import parser
from . import expander
def create_resourcetable(data):
    resourcetable = {}
    for line in data:
        name, value = parser.parse_resources(line)
        resourcetable[name] = value

def expand(text):
    '''Expands pseudo-instructions into real instructions, supports symbolic arguments'''
    newtext = []
    for line in text:
        if parser.is_instruction(line):
            newtext.extend(expanders.expand_instruction(line))
        else:
            # Just add label in
            newtext.append(line)
def assemble(data, text):
    # First step: create a resourcetable of data section
    resourcetable = create_resourcetable(data)
    parsed = []

