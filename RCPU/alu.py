from architecture import alu_instruction_mapping
class ALU:
    def __init__(self):
        pass
    def calculate(self, subinstruction, destination, source):
        opcode, arguments = self.decode(subinstruction)
        return self.execute(opcode, arguments, destination, source)
    def decode(self, subinstruction):
        '''Decodes the instruction as opcode, arguments'''
        opcode = alu_instruction_mapping[subinstruction & 0b1111]
        arguments = alu_instruction >> 5
        return opcode, arguments
    def execute(self, opcode, arguments):
        '''Executes the decoded instruction'''
        to_call = getattr(self, opcode)
        to_call(arguments, destination, source)
    def ADD(self, arg, dst, src):
        return dst + src
    def SUB(self, arg, dst, src):
        return dst - src
    def MUL(self, arg, dst, src):
        return dst * src
    def DIV(self, arg, dst, src):
        return dst // src
    def LSH(self, arg, dst, src):
        return src << arg
    def RSH(self, arg, dst, src):
        return src >> arg
    def AND(self, arg, dst, src):
        return src & dst
    def OR(self, arg, dst, src):
        return src | dst
    def XOR(self, arg, dst, src):
        return src ^ dst
    def NOT(self, arg, dst, src):
        return 0xFF - src