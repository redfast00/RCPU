from RCPU.architecture import alu_instruction_mapping, MAX_VALUE
class ALU:
    def __init__(self):
        pass
    def calculate(self, subinstruction, destination, source):
        opcode, shift_amount = self.decode(subinstruction)
        return self.execute(opcode, shift_amount, destination, source) % (MAX_VALUE + 1)
    def decode(self, subinstruction):
        '''Decodes the instruction as opcode, arguments'''
        opcode = alu_instruction_mapping[subinstruction & 0b1111]
        shift_amount = subinstruction >> 5
        return opcode, shift_amount
    def execute(self, opcode, shift_amount, destination, source):
        '''Executes the decoded instruction'''
        to_call = getattr(self, opcode)
        return to_call(shift_amount, destination, source)
    def ADD(self, shift_amount, dst, src):
        return dst + src
    def SUB(self, shift_amount, dst, src):
        return dst - src
    def MUL(self, shift_amount, dst, src):
        return dst * src
    def DIV(self, shift_amount, dst, src):
        return dst // src
    def LSH(self, shift_amount, dst, src):
        return src << shift_amount
    def RSH(self, shift_amount, dst, src):
        return src >> shift_amount
    def AND(self, shift_amount, dst, src):
        return src & dst
    def OR(self, shift_amount, dst, src):
        return src | dst
    def XOR(self, shift_amount, dst, src):
        return src ^ dst
    def NOT(self, shift_amount, dst, src):
        return MAX_VALUE - src
    def INC(self, shift_amount, dst, src):
        return dst + 1
    def DEC(self, shift_amount, dst, src):
        return dst - 1