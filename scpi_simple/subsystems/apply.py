VALID_CHANNELS = {"P6V", "N6V", "P25V", "N25V"}

class Apply:
    """ Apply subsystem
    For setting the output voltage and current on the power supply as a unified command. 
    This provides a convenient method for configuring the power supply with a single call, rather than setting voltage and current separately.
    """
    def __init__(self, instrument):
        self._inst = instrument
    
    def set(self, channel: str, voltage: float, current: float):
        """Set the output voltage and current for the specified channel.
        Args:
            channel (str): The channel to set.
            voltage (float): The voltage to set.
            current (float): The current to set.
        """
        if channel not in VALID_CHANNELS:
            raise ValueError(f"Invalid channel '{channel}'. Must be one of {VALID_CHANNELS}")
        if voltage < 0 or current < 0:
            raise ValueError("Voltage and current must be non-negative")
        self._inst.write(f"APPL {channel}, {voltage}, {current}")