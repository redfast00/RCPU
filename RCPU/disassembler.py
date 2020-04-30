import argparse


class RCPUDisassembleException(Exception):
    pass


class InvalidRegisterException(RCPUDisassembleException):
    pass


class InvalidOperationException(RCPUDisassembleException):
    pass


class Register:
    _registers = {
        0b00: "A",
        0b01: "B",
        0b10: "C",
        0b11: "D"
    }

    @staticmethod
    def get(code: int) -> str:
        if code in Register._registers.keys():
            return Register._registers[code]
        else:
            raise InvalidRegisterException()


class Operation:
    _operations = {
        0b0000: "ADD",
        0b0001: "SUB",
        0b0010: "MUL",
        0b0011: "DIV",
        0b0100: "LSH",
        0b0101: "RSH",
        0b0110: "AND",
        0b0111: "OR",
        0b1000: "XOR",
        0b1001: "NOT",
        0b1010: "INC",
        0b1011: "DEC"
    }

    @staticmethod
    def get(code: int) -> str:
        if code in Operation._operations.keys():
            return Operation._operations[code]
        else:
            raise InvalidOperationException()


class RCPUInstruction:
    def __init__(self, name: str):
        self.name = name

    def disassemble(self, data) -> str:
        return f"{self.name}"


class RCPUSDInstruction(RCPUInstruction):
    """Source Destination instruction"""
    def disassemble(self, data) -> str:
        return f"{self.name}\t" \
               f"{Register.get((data & 0b0000000000110000) >> 4)}, " \
               f"{Register.get((data & 0b0000000011000000) >> 6)} "


class RCPUMDInstruction(RCPUInstruction):
    """Memory Destination, Value Destination instruction"""
    def disassemble(self, data) -> str:
        return f"{self.name}\t" \
               f"{Register.get((data & 0b0000000000110000) >> 4)}, " \
               f"{(data & 0b1111111111000000) >> 6}"


class RCPUATHInstruction(RCPUSDInstruction):
    """ATH instruction"""
    def disassemble(self, data) -> str:
        return f"{super().disassemble(data)}, " \
               f"{Operation.get((data & 0b0000111100000000) >> 8)}, " \
               f"{(data & 0b0001000000000000) >> 12}, " \
               f"{(data & 0b1110000000000000) >> 13}"


class RCPUSRInstruction(RCPUInstruction):
    """Source Register instruction"""
    def disassemble(self, data) -> str:
        return f"{self.name} \t{Register.get((data & 0b0000000011000000) >> 6)}"


class RCPUDRInstruction(RCPUInstruction):
    """Destination Register instruction"""
    def disassemble(self, data) -> str:
        return f"{self.name} \t{Register.get((data & 0b0000000000110000) >> 4)}"


class RCPUSMInstruction(RCPUInstruction):
    """Single Memory instruction"""
    def disassemble(self, data) -> str:
        return f"{self.name} \t{(data & 0b1111111111000000) >> 6}"


class Disassembler:
    def __init__(self):
        self._opcodes = {
            0b0000: RCPUSDInstruction("MOV"),
            0b0001: RCPUMDInstruction("LDV"),
            0b0010: RCPUMDInstruction("LDA"),
            0b0011: RCPUMDInstruction("LDM"),
            0b0100: RCPUSDInstruction("LDR"),
            0b0101: RCPUSDInstruction("LDP"),
            0b0110: RCPUATHInstruction("ATH"),
            0b0111: RCPUDRInstruction("CAL"),
            0b1000: RCPUInstruction("RET"),
            0b1001: RCPUSDInstruction("JLT"),
            0b1010: RCPUSRInstruction("PSH"),
            0b1011: RCPUDRInstruction("POP"),
            0b1100: RCPUInstruction("SYS"),
            0b1101: RCPUInstruction("HLT"),
            0b1110: RCPUSMInstruction("JMP"),
            0b1111: RCPUSRInstruction("JMR"),
        }

    def disassemble(self, filename, include_binairy=False):
        with open(filename, "rb") as file:
            output = []
            byte = file.read(1)
            buffer = b''
            while byte:
                buffer += byte
                if len(buffer) == 2:
                    asm = self._opcodes[int(buffer[1]) & 0b00001111].disassemble(int.from_bytes(buffer, 'big'))
                    if include_binairy:
                        output.append(f"{int.from_bytes(buffer, 'big'):16b}\t{asm}")
                    else:
                        output.append(asm)
                    buffer = b''
                byte = file.read(1)
            return DisassemblerOutput(output)


class DisassemblerOutput:
    def __init__(self, lines: list):
        self._lines = lines

    def write(self, filename):
        with open(filename, "w") as file:
            file.write("\n".join(self._lines))

    def print(self):
        for line in self._lines:
            print(line)


parser = argparse.ArgumentParser('RCPU disassembler.')
parser.add_argument('--input', type=str, required=True, help='The Input File')
parser.add_argument('--output', type=str, required=False, help='The output file')
parser.add_argument('-b', action='store_true', help='Include binary input')
args = parser.parse_args()

if args.output:
    Disassembler().disassemble(args.input, args.b).write(args.output)
else:
    Disassembler().disassemble(args.input, args.b).print()

