from ..instruments.base import SCPIParameter

class Output:
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
        return self._inst.query("OUTP?")

    def _set_state(self, state: int):
        match state:
            case 1:
                self._inst.write("OUTP ON")
            case 0:
                self._inst.write("OUTP OFF")
            case _:
                raise ValueError("State must be 0 or 1")