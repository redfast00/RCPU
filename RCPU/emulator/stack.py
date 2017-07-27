class Stack:
    def __init__(self, registers):
        self._stack = []
        self._reg = registers
    def push(self, value):
        self._stack.append(value)
        self._reg.sp += 1
    def pop(self):
        self._reg.sp -= 1
        return self._stack.pop()
