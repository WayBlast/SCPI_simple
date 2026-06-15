class Display:
    """Subsystem for controlling display settings on the oscilloscope.
    
    Provides method for clearing the display
    """
    def __init__(self, instrument):
        self._inst = instrument

    def clear_menu(self):
        """Clear the display menu on the oscilloscope. This can be used to remove any on-screen menus or overlays that may be present.
        """
        self._inst.write("CLEARMenu")

    
