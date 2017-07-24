class RAM:
    def __init__(self, size):
        self._memory = [ 0 for cell in range(size) ]
    def get(self, address):
        # TODO: make sure this is within bounds
        return self._memory[address]
    def set(self, address, value):
        self._memory[address] = value
    def load(self, memory_to_load, base_address = 0):
        '''Copies given memory into RAM'''
        size = len(memory_to_load)
        self._memory[base_address:base_address+size] = memory_to_load[:]