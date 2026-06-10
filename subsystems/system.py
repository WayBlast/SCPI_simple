class System:
    def __init__(self, instrument):
        self._inst = instrument

    def beep(self):
        self._inst.write("SYSTem:BEEPer:IMMEdiate")