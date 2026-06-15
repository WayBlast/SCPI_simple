class System:
    """Subsystem for controlling system-level functions of the instrument, such as beeping."""
    def __init__(self, instrument):
        self._inst = instrument

    def beep(self):
        """Trigger an immediate beep from the instrument. This can be used for audible notifications or alerts.
        
            Note: The availability and behavior of the beep function may depend on the specific instrument model and its configuration.
        """
        self._inst.write("SYSTem:BEEPer:IMMEdiate")