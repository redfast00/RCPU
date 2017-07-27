class KernelException(Exception):
    pass

class Kernel:
    def __init__(self, ram, stack):
        self.RAM = ram
        self.stack = stack

    def read_string(self, memory_address):
        result = ''
        for charcode in self.RAM.get_raw()[memory_address:]:
            if charcode == 0:
                break
            result += chr(charcode)
        return result

    def syscall(self):
        call_number = self.stack.pop()
        # This return value only exists to make testing easier
        return self.call_syscall_by_number(call_number)

    def call_syscall_by_number(self, number):
        return getattr(self, "syscall_" + str(number))()

    def syscall_0(self):
        '''printf: formatstring, [arguments]'''
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
        print(result)
        return result


