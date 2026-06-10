# subsystems/set.py
from scpi_simple.instruments.base import SCPIParameter


class SetPoint:
    voltage: SCPIParameter
    current: SCPIParameter

    def __init__(self, instrument):
        object.__setattr__(self, '_inst', instrument)

        object.__setattr__(self, 'voltage', SCPIParameter(
            getter=self._get_voltage,
            setter=self._set_voltage
        ))
 
        object.__setattr__(self, 'current', SCPIParameter(
            getter=self._get_current,
            setter=self._set_current
        ))

    def __setattr__(self, name, value):
        if isinstance(value, SCPIParameter):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                f"Cannot assign to '{name}' directly. Use .set() instead."
            )

    def _get_voltage(self):
        return float(self._inst.query("VOLT?"))

    def _set_voltage(self, voltage: float):
        if voltage < 0:
            raise ValueError("Voltage must be non-negative")
        self._inst.write(f"VOLT {voltage}")

    def _get_current(self):
        return float(self._inst.query("CURR?"))

    def _set_current(self, current: float):
        if current < 0:
            raise ValueError("Current must be non-negative")
        self._inst.write(f"CURR {current}")