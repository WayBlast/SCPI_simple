# subsystems/set.py
from scpi_simple.instruments.base import SCPIParameter


class SetPoint:
    """Subsystem for controlling the setpoint of a power supply. 
    
    This includes setting and querying the voltage and current setpoints."""
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
        """Query the voltage setpoint from the power supply.

        Returns:
            float: The voltage setpoint in volts.
        """
        return float(self._inst.query("VOLT?"))

    def _set_voltage(self, voltage: float):
        """Set the voltage setpoint on the power supply.

        Args:
            voltage (float): The voltage setpoint to set in volts. Must be a non-negative
        """
        if voltage < 0:
            raise ValueError("Voltage must be non-negative")
        self._inst.write(f"VOLT {voltage}")

    def _get_current(self):
        """Query the current setpoint from the power supply.

        Returns:
            float: The current setpoint in amps.
        """
        return float(self._inst.query("CURR?"))

    def _set_current(self, current: float):
        """Set the current setpoint on the power supply.

        args:
            current (float): The current setpoint to set in amps. Must be a non-negative
        """ 
        if current < 0:
            raise ValueError("Current must be non-negative")
        self._inst.write(f"CURR {current}")