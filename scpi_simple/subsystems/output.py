from ..instruments.base import SCPIParameter

class Output:
    """Subsystem for controlling the output state of the instrument. This includes turning the output on or off and querying the current output state."""
    state: SCPIParameter
    
    def __init__(self, instrument):
        object.__setattr__(self, "_inst", instrument)
        object.__setattr__(self, "state", SCPIParameter(
            getter=self._get_state,
            setter=self._set_state
        ))

    def __setattr__(self, name, value):
        if isinstance(value, SCPIParameter):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                f"Cannot assign to '{name}' directly. Use .set() instead."
            )

    def _get_state(self):
        """Query the current output state of the instrument. Returns 1 if the output is on, and 0 if it is off.
        
        Returns:
            int: The current output state (1 for on, 0 for off).

        """

        return self._inst.query("OUTP?")

    def _set_state(self, state: int):
        """Set the output state of the instrument. 1 for on, 0 for off.
        
        args:
            state (int): The output state to set (1 for on, 0 for off).
        """
        match state:
            case 1:
                self._inst.write("OUTP ON")
            case 0:
                self._inst.write("OUTP OFF")
            case _:
                raise ValueError("State must be 0 or 1")