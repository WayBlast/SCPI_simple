from ..subsystems.apply import Apply
from ..subsystems.output import Output
from ..subsystems.setpoint import SetPoint
from ..subsystems.system import System
from .base import Instrument

class Psu(Instrument):
    """Interface for controlling a VISA-compatible bench power supply.

    Wraps a pyvisa resource to provide methods for configuring
    voltage, current, channel selection, and output state.
    """

    def __init__(self, rm, address):
        """Open a connection to the power supply.

        Args:
            rm: A pyvisa ResourceManager instance.
            address: The VISA address of the power supply (e.g. 'USB0::...').
            timeout: Communication timeout in milliseconds. Defaults to 5000.
            read_termination: Line termination character for reads. Defaults to '\\n'.
            write_termination: Line termination character for writes. Defaults to '\\n'.

        Raises:
            Exception: If the resource cannot be opened. Check the device is connected.
        """
        super().__init__(rm=rm, address=address)
        self.setpoint = SetPoint(self)
        self.apply    = Apply(self)
        self.output   = Output(self)
        self.system   = System(self)
    
    