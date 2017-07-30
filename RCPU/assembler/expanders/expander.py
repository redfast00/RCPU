from RCPU.architecture import instruction_mapping
import RCPU.assembler.parser as parser

from .arithmetic import ArithmeticExpander
from .utilexpander import UtilExpander
from .conditionalexpander import ConditionalExpander

_all_classes = [ArithmeticExpander, UtilExpander, ConditionalExpander]
mapping = {}
for c in _all_classes:
    mapping.update(c.get_instructions())

def expand_instruction(line):
    instruction, arguments = parser.parse_instruction(line)
    if instruction in instruction_mapping.values():
        # No need to expand this
        return [line]
    else:
        return mapping[instruction](arguments)