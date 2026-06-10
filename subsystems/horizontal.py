from ..instruments.base import SCPIParameter

class Horizontal:
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
        response = self._inst.query("HORizontal:SCAle?")
        return float(response)

    def _set_scale(self, value: int):
        if value <= 0:
            raise ValueError("Scale must be positive")
        self._inst.write(f"HORizontal:SCAle {value}")
    
    def _get_position(self):
        response = self._inst.query("HORizontal:POSition?")
        return float(response)
    
    def _set_position(self, position: int):
        if isinstance(position, int):
            self._inst.write(f'HORIZONTAL:POSITION {position}') 
        else:
            raise Exception("Position must be int")
        
    def _get_settings(self):
        return self._inst.query("HORizontal?")
    
