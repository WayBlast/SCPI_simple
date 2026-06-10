VALID_CHANNELS = {"P6V", "N6V", "P25V", "N25V"}

class Apply:
    
    def __init__(self, instrument):
        self._inst = instrument
    
    def set(self, channel: str, voltage: float, current: float):
        if channel not in VALID_CHANNELS:
            raise ValueError(f"Invalid channel '{channel}'. Must be one of {VALID_CHANNELS}")
        if voltage < 0 or current < 0:
            raise ValueError("Voltage and current must be non-negative")
        self._inst.write(f"APPL {channel}, {voltage}, {current}")