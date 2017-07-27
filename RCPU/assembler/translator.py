import RCPU.architecture as arch

reverse_instruction_mapping = {i:b for b,i in arch.instruction_mapping.items()}
reverse_register_mapping = {i:b for b,i in arch.register_mapping.items()}

def reg_to_bin(reg):
    '''Converts a register (like 'A') to the register value '0b00'.'''
    try:
        return reverse_register_mapping[reg.upper()]
    # Hardcoded unused registers in expanders
    except KeyError as k:
        if reg == '0':
            return 0
        else:
            raise

class InstructionTranslator:
    '''Translates instructions into binary. Doesn't support symbolic arguments'''

    @classmethod
    def translate(cls, instruction, arguments):
        binary_opcode = reverse_instruction_mapping[instruction.upper()]
        binary_arguments = getattr(cls, instruction)(arguments) << 4
        return binary_opcode | binary_arguments

    @staticmethod
    def error():
        raise Exception("Error in translating binary") #TODO make special error class

    @classmethod
    def MOV(cls, arg):
        D = reg_to_bin(arg[0])
        S = reg_to_bin(arg[1])
        return D | (S << 2)

    @classmethod
    def LDV(cls, arg):
        D = reg_to_bin(arg[0])
        V = int(arg[1])
        if V > arch.MAX_VALUE_LDV or V < 0:
            cls.error()
        return D | (V << 2)

    @classmethod
    def LDA(cls, arg):
        D = reg_to_bin(arg[0])
        M = int(arg[1])
        if M > arch.MAX_MEM_LDA or M < 0:
            cls.error()
        return D | (M << 2)

    @classmethod
    def LDM(cls, arg):
        D = reg_to_bin(arg[0])
        M = int(arg[1])
        if M > arch.MAX_MEM_LDM or M < 0:
            cls.error()
        return D | (M << 2)

    @classmethod
    def LDR(cls, arg):
        D = reg_to_bin(arg[0])
        S = reg_to_bin(arg[1])
        return D | (S << 2)

    @classmethod
    def ATH(cls, arg):
        D = reg_to_bin(arg[0])
        S = reg_to_bin(arg[1])
        OP = int(arg[2]) # Just O might be confused with 0
        M = int(arg[3])
        B = int(arg[4])
        if OP > 0b1111 or OP < 0:
            cls.error()
        if M not in [0b0, 0b1]:
            cls.error()
        if B > 0b111 or B < 0:
            cls.error()
        return D | (S << 2) | (OP << 4) | (M << 8) | (B << 9)

    @classmethod
    def CAL(cls, arg):
        D = reg_to_bin(arg[0])
        return D

    @classmethod
    def RET(cls, arg):
        return 0

    @classmethod
    def JLT(cls, arg):
        D = reg_to_bin(arg[0])
        S = reg_to_bin(arg[1])
        return D | (S << 2)

    @classmethod
    def PSH(cls, arg):
        S = reg_to_bin(arg[0])
        return S << 2

    @classmethod
    def POP(cls, arg):
        D = reg_to_bin(arg[0])
        return D

    @classmethod
    def SYS(cls, arg):
        return 0

    @classmethod
    def HLT(cls, arg):
        return 0

    @classmethod
    def JMP(cls, arg):
        M = int(arg[0])
        if M > arch.MAX_MEM_JMP or M < 0:
            cls.error()
        return (M << 2)

    @classmethod
    def JMR(cls, arg):
        S = reg_to_bin(arg[0])
        return S << 2