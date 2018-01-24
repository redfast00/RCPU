ALLOWED = '<>+-.,[]'

# Register D points to the cell that is currently selected
# Register C contains a bitmask to ensure overflows when incrementing and decrementing

def find_matching_bracket(code, index):
    counter = 0
    print(code, index)
    for idx, char in enumerate(code[index:]):
        if char == "[":
            counter += 1
        elif char == "]":
            counter -= 1
        # Check if we are done
        if counter == 0:
            return idx


class Token:
    def __init__(self, opcode):
        self.opcode = opcode


class Bracket(Token):
    def __init__(self, opcode, match=0):
        self.match = match
        super().__init__(opcode)


class Compiler:
    def __init__(self, infile):
        self.code = infile.read()
        self.out = []

    def emit(self, instructions):
        self.out.extend(instructions)

    def tokenise(self):
        # Clean out non-brainfuck characters
        self.code = [char for char in self.code if char in ALLOWED]
        # Create empty list of same lenght
        self.tokens = [None for char in self.code]
        for idx in range(len(self.tokens)):
            # if there is no token here yet
            if self.tokens[idx] is None:
                if self.code[idx] == '[':
                    match = find_matching_bracket(self.code, idx)
                    self.tokens[idx] = Bracket(self.code[idx], match)
                    # Also generate back bracket
                    self.tokens[match] = Bracket(self.code[match], idx)
                else:
                    # This is a normal token
                    self.tokens[idx] = Token(self.code[idx])

            else:
                # Only back tokens should end up here
                pass


    def translate_tokens(self):
        for token in self.tokens:
            # 'D' register points to current cell
            if token.opcode == '+':
                self.emit([
                    'LDR A, D',
                    'INC A',
                    'AND A, C',
                    'LDP D, A'
                ])
            elif token.opcode == '-':
                self.emit([
                    'LDR A, D',
                    'DEC A',
                    'AND A, C',
                    'LDP D, A'
                ])
            elif token.opcode == '.':
                self.emit([
                    'LDV A, printchar:',
                    'CAL A'
                ])
            elif token.opcode == ',':
                self.emit([
                    'LDV A, readchar:',
                    'CAL A',
                    'LDP A, '
                ])

    def initialise_structures(self):
        self.emit([
            '.data',
            '.fmt string "_"', # placeholder, will be replaced
            '.tape allocate 5000', # TODO: determine this at compiletime
            '.text',
            '.global main:',
            'printchar:',
                'LDV16 B, .fmt',
                'LDR A, D', # load current value into 'A'
                'LDP B, A', # overwrite first character of format string
                'PSH B',
                'LDV A, 0',
                'PSH A',
                'SYS',
                'RET',
            'getchar:',
                'LDV A, 0', # stdin
                'PSH A',
                'LDV A, 2', # getc
                'PSH A',
                'SYS',
                'POP A', # place character in A
                'RET',
            'main:',
                'LDV16 D, .tape',
                'LDV C, 255',
        ])

    def compile(self):
        '''This does all needed steps (naming is hard)'''
        self.tokenise()
        self.initialise_structures()
        self.translate_tokens()
        self.out.append('HLT')
        return '\n'.join(self.out)
