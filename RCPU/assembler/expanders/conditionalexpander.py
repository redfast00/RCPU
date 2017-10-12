from RCPU.assembler.expanders.baseexpander import BaseExpander
from .helpers import get_free_register, generate_label, fill_instructions


class ConditionalExpander(BaseExpander):

    @BaseExpander.instruction
    def JGE(arg):
        '''Jump to memory address pointed at by the source register,
           if value in the A register is greater than or equal to
           the value in the destination register
        '''
        destination = arg[0]
        source = arg[1]
        free_register = get_free_register([destination, source, 'A'])
        failure = generate_label()
        instructions = [
            "PSH {free_register}",
            "LDV16 {free_register}, {failure}",
            "JLT {destination}, {free_register}",
            # Success, reset everything to how it was and make the jump
            "POP {free_register}",
            "JMR {source}",
            # Failure, reset everything to how it was
            "{failure}",
            "POP {free_register}",
        ]
        return fill_instructions(instructions, destination=destination, source=source,
                                 free_register=free_register, failure=failure)

    @BaseExpander.instruction
    def JEQ(arg):
        '''Jump to memory address pointed at by the source register,
           if value in the A register is equal to the value in the
           destination register
        '''
        destination = arg[0]
        source = arg[1]
        free_register = get_free_register([destination, source, 'A'])
        failure_one = generate_label()
        failure_two = generate_label()
        instructions = [
            "PSH {free_register}",
            "LDV16 {free_register}, {failure_one}",
            "JLT {destination}, {free_register}",
            "SWP A, {destination}",
            "LDV16 {free_register}, {failure_two}",
            "JLT {destination}, {free_register}",
            "POP {free_register}",  # TODO optimise this to use the same register
            "JMR {source}",
            "{failure_two}",
            "SWP A, {destination}",
            "{failure_one}",
            "POP {free_register}"
        ]
        return fill_instructions(instructions, destination=destination, source=source,
                                 free_register=free_register, failure_one=failure_one, failure_two=failure_two)

    @BaseExpander.instruction
    def JNE(arg):
        '''Jump to memory address pointed at by the source register,
           if value in the A register is not equal to the value in the
           destination register
        '''
        destination = arg[0]
        source = arg[1]
        free_register = get_free_register([destination, source, 'A'])
        success = generate_label()
        failure = generate_label()
        instructions = [
            "JLT {destination}, {source}",
            "PSH {free_register}",
            "SWP A, {destination}",
            "LDV16 {free_register}, {success}",
            "JLT {destination}, {free_register}",
            # Registers are equal, JMP to the end of pseudo-instruction
            "LDV16 {free_register}, {failure}",
            "JMR {free_register}",
            "{success}",
            "SWP A, {destination}",
            "POP {free_register}",
            "JMR {source}",
            "{failure}",
            "POP {free_register}"
        ]
        return fill_instructions(instructions, destination=destination, source=source,
                                 free_register=free_register, success=success, failure=failure)

    @BaseExpander.instruction
    def JGT(arg):
        '''Jump to memory address pointed at by the source register,
           if value in the A register is greater than
           the value in the destination register
        '''
        destination = arg[0]
        source = arg[1]
        free_register = get_free_register([destination, source, 'A'])
        failure = generate_label()
        success = generate_label()
        instructions = [
            "PSH {free_register}",
            "SWP A, {destination}",
            "LDV16 {free_register}, {success}",
            "JLT {destination}, {free_register}",
            "LDV16 {free_register}, {failure}",
            "JMR {free_register}",
            "{success}",
            "SWP A, {destination}",
            "POP {free_register}",
            "JMR {source}",
            "{failure}",
            "SWP A, {destination}",
            "POP {free_register}"
        ]
        return fill_instructions(instructions, destination=destination, source=source,
                                 free_register=free_register, failure=failure, success=success)

    @BaseExpander.instruction
    def JLE(arg):
        '''Jump to memory address pointed at by the source register,
           if value in the A register is less than or equal to
           the value in the destination register
        '''
        destination = arg[0]
        source = arg[1]
        free_register = get_free_register([destination, source, 'A'])
        failure = generate_label()
        success = generate_label()
        instructions = [
            # Check less
            "JLT {destination}, {source}",
            # Was not less, check if equal
            "PSH {free_register}",
            "SWP A, {destination}",
            "LDV16 {free_register}, {failure}",
            "JLT {destination}, {free_register}",
            # Success
            "SWP A, {destination}",
            "POP {free_register}",
            "JMR {source}",
            # Failure
            "{failure}",
            "SWP A, {destination}",
            "POP {free_register}"
        ]
        return fill_instructions(instructions, destination=destination, source=source,
                                 free_register=free_register, failure=failure, success=success)
