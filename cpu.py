import ram
import registers
import stack
import alu
from architecture import instruction_mapping

import sys

class CPU:
    def __init__(self):
        self.RAM = ram.RAM(2^16)
        self.registers = registers.Registers()
        self.stack = stack.Stack()
        self.alu = alu.ALU()
    def debug(self):
        print self.registers
    def fetch(self):
        '''Gets the instruction to execute'''
        return self.RAM.get(self.registers.ip)
    def decode(self, instruction):
        '''Decodes the instruction as opcode, arguments'''
        opcode = instruction_mapping[instruction & 0b1111]
        arguments = instruction >> 4
        return opcode, arguments
    def execute(self, opcode, arguments):
        '''Executes the decoded instruction'''
        to_call = getattr(self, opcode)
        to_call(arguments)
    def step(self):
        '''Does one instruction cycle'''
        instruction = self.fetch()
        opcode, arguments = self.decode(instruction)
        self.execute(opcode, arguments)
        self.registers.ip += 1
    # Instructions

    def MOV(self, arguments):
        destination = arguments & 0b11
        source = (arguments >> 2) & 0b11
        self.registers.set(destination, self.registers.get(source))
    def LDV(self, arguments):
        destination = arguments & 0b11
        value = arguments >> 2
        self.registers.set(destination, value)
    def LDA(self, arguments):
        destination = arguments & 0b11
        memory_address = arguments >> 2
        self.registers.set(destination, self.RAM.get(memory_address))
    def LDM(self, arguments):
        destination = arguments & 0b11
        memory_address = arguments >> 2
        self.RAM.set(memory_address, self.registers.get(destination))
    def LDR(self, arguments):
        destination = arguments & 0b11
        source = (arguments >> 2) & 0b11
        self.registers.set(destination, self.RAM.get(self.registers.get(source)))
    def LDP(self, arguments):
        destination = arguments & 0b11
        source = (arguments >> 2) & 0b11
        self.RAM.set(self.registers.get(destination), self.registers.get(source))
    def ATH(self, arguments):
        destination = arguments & 0b11
        source = (arguments >> 2) & 0b11
        mode = (arguments >> 8) & 0b1
        # Pass the rest on to the ALU core
        subinstruction = arguments >> 4
        dst_val = self.registers.get(destination)
        src_val = self.registers.get(source)
        result = self.alu.calculate(subinstruction, dst_val, src_val)
        if mode:
            # mode == 1, place result in source register
            self.registers.set(source, result)
        else:
            # mode == 0, place result in destination register
            self.registers.set(destination, result)
    def CAL(self, arguments):
        destination = arguments & 0b11
        self.stack.push(self.registers.ip)
        self.registers.ip = self.registers.get(destination)
    def RET(self, arguments):
        self.registers.ip = self.stack.pop()
    def JLT(self, arguments):
        destination = arguments & 0b11
        source = (arguments >> 2) & 0b11
        a_register = 0b00
        if self.registers.get(a_register) < self.registers.get(destination):
            self.registers.ip = self.RAM.get(self.registers.get(source))
    def PSH(self, arguments):
        source = (arguments >> 2) & 0b11
        self.stack.push(self.registers.get(source))
        self.registers.sp += 1
    def POP(self, arguments):
        destination = arguments & 0b11
        self.registers.set(destination, self.stack.pop())
        self.registers.sp -= 1
    def SYS(self, arguments):
        syscall = arguments
        # TODO
    def HLT(self, arguments):
        print("Terminating...")
        sys.exit(0)
    def JMP(self, arguments):
        address = arguments
        self.registers.ip = address
    def JMR(self, arguments):
        source = (arguments >> 2) & 0b11
        self.registers.ip = self.registers.get(source)

if __name__ == '__main__':
    c = CPU()
    c.RAM.load([0b1010101010000001])
    c.step()
    c.debug()

