from RCPU.assembler.expanders.baseexpander import BaseExpander


class ArithmeticExpander(BaseExpander):

    @BaseExpander.instruction
    def ADD(arg):
        return ['ATH {d},{s},0,0,0'.format(d=arg[0], s=arg[1])]

    @BaseExpander.instruction
    def SUB(arg):
        return ['ATH {d},{s},1,0,0'.format(d=arg[0], s=arg[1])]

    @BaseExpander.instruction
    def SUBS(arg):
        return ['ATH {d},{s},1,1,0'.format(d=arg[0], s=arg[1])]

    @BaseExpander.instruction
    def MUL(arg):
        return ['ATH {d},{s},2,0,0'.format(d=arg[0], s=arg[1])]

    @BaseExpander.instruction
    def DIV(arg):
        return ['ATH {d},{s},3,0,0'.format(d=arg[0], s=arg[1])]

    @BaseExpander.instruction
    def DIVS(arg):
        return ['ATH {d},{s},3,1,0'.format(d=arg[0], s=arg[1])]

    @BaseExpander.instruction
    def LSH(arg):
        return ['ATH {s},{s},4,1,{b}'.format(s=arg[0], b=arg[1])]

    @BaseExpander.instruction
    def RSH(arg):
        return ['ATH {s},{s},5,1,{b}'.format(s=arg[0], b=arg[1])]

    @BaseExpander.instruction
    def AND(arg):
        return ['ATH {d},{s},6,0,0'.format(d=arg[0], s=arg[1])]

    @BaseExpander.instruction
    def OR(arg):
        return ['ATH {d},{s},7,0,0'.format(d=arg[0], s=arg[1])]

    @BaseExpander.instruction
    def XOR(arg):
        return ['ATH {d},{s},8,0,0'.format(d=arg[0], s=arg[1])]

    @BaseExpander.instruction
    def NOT(arg):
        return ['ATH {s},{s},9,1,0'.format(s=arg[0])]

    @BaseExpander.instruction
    def INC(arg):
        return ['ATH {d},{d},10,0,0'.format(d=arg[0])]

    @BaseExpander.instruction
    def DEC(arg):
        return ['ATH {d},{d},11,0,0'.format(d=arg[0])]
