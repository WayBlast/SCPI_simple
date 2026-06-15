from ..instruments.base import SCPIParameter

class Horizontal:
    """Subsystem for controlling horizontal settings on the oscilloscope.
    """
    scale:      SCPIParameter
    position:   SCPIParameter
    settings:   SCPIParameter

    def __init__(self, instrument):

        object.__setattr__(self, '_inst', instrument)

        object.__setattr__(self, 'scale', SCPIParameter(
            getter=self._get_scale,
            setter=self._set_scale
        ))
        object.__setattr__(self, 'position', SCPIParameter(
            getter=self._get_position,
            setter=self._set_position
        ))
        object.__setattr__(self, 'settings', SCPIParameter(
            getter=self._get_settings,
            setter=None
        ))
        
    def __setattr__(self, name, value):
        if isinstance(value, SCPIParameter):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                f"Cannot assign to '{name}' directly. Use .set() instead."
            )

    def _get_scale(self):
        """Query the horizontal scale (time per division) from the oscilloscope.

            Returns:
                float: The horizontal scale in seconds per division.

        """
        response = self._inst.query("HORizontal:SCAle?")
        return float(response)

    def _set_scale(self, value: int):
        """Set the horizontal scale (time per division) on the oscilloscope.

        args:            
            value (float): The horizontal scale to set in seconds per division. Must be a positive number
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Scale must be positive integer")
        self._inst.write(f"HORizontal:SCAle {value}")
    
    def _get_position(self):
        """Query the horizontal position (time offset) from the oscilloscope.

        Returns:
            float: The horizontal position in seconds, which represents the time offset of the waveform display.
        """
        response = self._inst.query("HORizontal:POSition?")
        return float(response)
    
    def _set_position(self, position: int):
        """Set the horizontal position (time offset) on the oscilloscope.

        args:
            position (float): The horizontal position to set in seconds.
        """
        if isinstance(position, int):
            self._inst.write(f'HORIZONTAL:POSITION {position}') 
        else:
            raise Exception("Position must be int")
        
    def _get_settings(self):
        """Query the current horizontal settings from the oscilloscope.

        Returns:
            str: The current horizontal settings as a string, which may include information about the scale.
        """
        return self._inst.query("HORizontal?")
    
