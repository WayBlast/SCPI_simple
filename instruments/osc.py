from ..subsystems.acquire import Acquire
from ..subsystems.data import Data
from ..subsystems.display import Display
from ..subsystems.horizontal import Horizontal
from .base import Instrument

class Osc(Instrument):
    """Interface for controlling a Tektronix Osciloscope.

    Wraps a pyvisa resource to provide methods for configuring
    data acquisition, display settings, channel selection etc.
    """

    def __init__(self, rm, address):
        """Open a connection to the oscilloscope.

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
        self.acquire = Acquire(self)
        self.data  = Data(self)
        self.horizontal = Horizontal(self)
        self.display = Display(self)
    
    