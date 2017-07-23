class Registers:
    def __init__(self):
        self._gp = [0,0,0,0]
        self.ip = 0
        self.sp = 0
    def set(self, register, value):
        self._gp[register] = value
    def get(self, register):
        return self._gp[register]
    def __str__(self):
        return str(self._gp) + " IP={}, SP={}".format(self.ip, self.sp)