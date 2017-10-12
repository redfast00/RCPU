import sys

class KernelException(Exception):
    pass

class Kernel:
    def __init__(self, ram, stack):
        self.RAM = ram
        self.stack = stack
        self.filenumber_mapping = {
            0: sys.stdin,
            1: sys.stdout
        }

    def read_string(self, memory_address):
        '''Helper function to read null-terminated string from memory'''
        result = ''
        for charcode in self.RAM.get_raw()[memory_address:]:
            if charcode == 0:
                break
            result += chr(charcode)
        return result

    def write_string(self, memory_address, string):
        '''Helper function to write a string followed by a null-terminator to memory'''
        for i, char in enumerate(string):
            self.RAM.set(memory_address + i, ord(char))
        self.RAM.set(memory_address + len(string), 0)

    def get_file(self, filenumber):
        if filenumber not in self.filenumber_mapping.keys():
            raise NotImplementedError("File descriptor: {}".format(filenumber))
        else:
            return self.filenumber_mapping[filenumber]

    def syscall(self):
        call_number = self.stack.pop()
        # This return value only exists to make testing easier
        return self.call_syscall_by_number(call_number)

    def call_syscall_by_number(self, number):
        return getattr(self, "syscall_" + str(number))()

    def syscall_0(self):
        '''printf: formatstring, [arguments]
        Prints the formatstring formatted with values from stack to stdout.
        This only accepts %s, %d and %% in the format string.
        '''
        format_string = self.read_string(self.stack.pop())
        iterator = iter(format_string)
        result = ''
        for char in iterator:
            if char == '%':
                next_char = next(iterator)
                if next_char == '%':
                    result += '%'
                elif next_char == 'd':
                    result += str(self.stack.pop())
                elif next_char == 's':
                    result += self.read_string(self.stack.pop())
                else:
                    raise KernelException("Error in printf: '{}'".format(format_string))
            else:
                result += char
        sys.stdout.write(result)
        return result

    def syscall_1(self):
        '''fgets: *str, size, stream_num
        Gets a string from the stream specified by stream_num. Stops when either
         size - 1 are read (keep place for the NUL), a newline is encountered or
         the end-of-file is reached.
        The string is then placed in memory, starting at *str.
        Returns the number of characters read.
        '''
        memory_addr = self.stack.pop()
        size = self.stack.pop()
        stream_num = self.stack.pop()
        infile = self.get_file(stream_num)
        result = ''
        read = 0

        while True:
            c = infile.read(1)
            if not c:
                # EOF encountered
                break
            elif c == '\n':
                # End of the line
                break
            elif read >= size - 1:
                # Maximum size reached
                break
            else:
                result += c
                read += 1
        self.write_string(memory_addr, result)
        # Return number of characters read
        self.stack.push(read)

    def syscall_2(self):
        '''getc: stream_num
        Gets a single character from the stream specified by stream_num. Blocks
         until a character is read.
        Returns the ascii code of the character read.
        '''
        stream_num = self.stack.pop()
        infile = self.get_file(stream_num)
        char = infile.read(1)
        self.stack.push(ord(char))


