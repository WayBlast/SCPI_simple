class Display:
    def __init__(self, instrument):
        self._inst = instrument

    def clear_menu(self):
        self._inst.write("CLEARMenu")

    
