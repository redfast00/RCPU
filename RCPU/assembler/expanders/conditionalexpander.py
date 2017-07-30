from RCPU.assembler.expanders.baseexpander import BaseExpander
from .helpers import get_free_register, generate_label, fill_instructions

class ConditionalExpander(BaseExpander):

    @BaseExpander.instruction
    def JGE(arg):
        '''Jump to memory address pointed at by the source register,
           if value in the A register is greater than or equal to to
           the value in destination register
           '''
        destination = arg[0]
        source = arg[1]
        free_register = get_free_register([destination, source, "A"])
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
            free_register=free_register,failure=failure)