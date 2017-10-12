from RCPU.assembler.expanders.baseexpander import BaseExpander
from RCPU.architecture import MAX_VALUE_LDV
from RCPU.assembler.expanders.helpers import get_free_register, fill_instructions


class UtilExpander(BaseExpander):
    @BaseExpander.instruction
    def LDV16(arg):
        destination = arg[0]
        try:
            value = int(arg[1])
            symbolic = False
        except ValueError:
            value = arg[1]
            symbolic = True
        if not symbolic and value <= MAX_VALUE_LDV:
            return ["LDV {D},{V}".format(D=destination, V=value)]
        else:
            tmp_reg = get_free_register([destination])
            instructions = [
                "PSH {T}",
                "LDV {D},({V} >> 6)",
                "LSH {D},6",
                "LDV {T},({V} & 0b111111)",
                "OR {D},{T}",
                "POP {T}"
            ]
            return fill_instructions(instructions, T=tmp_reg, D=destination, V=value)

    @BaseExpander.instruction
    def SWP(arg):
        first = arg[0]
        second = arg[1]
        instructions = [
            "PSH {F}",
            "MOV {F},{S}",
            "POP {S}"
        ]
        return fill_instructions(instructions, F=first, S=second)
