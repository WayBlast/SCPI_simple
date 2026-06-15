import pyvisa

class Instrument:
    """Base class for VISA-compatible instruments.

    Wraps a pyvisa resource to provide basic connection handling and command/query methods.
    """
    
    def __init__(self, address, rm, timeout=5000, read_termination="\n", write_termination="\n"):
        """Open a connection to the instrument."""
        try:  
            self.rm = rm
            self.resource = self.rm.open_resource(address)
            self.resource.timeout = timeout
            self.resource.read_termination = read_termination
            self.resource.write_termination = write_termination
        except pyvisa.errors.VisaIOError as e:
            raise ConnectionError(
                f"Could not connect to instrument at '{address}': {e}"
            ) from e
        
    @classmethod
    def connect(cls, adr: str):
        """Alternate constructor method to connect to an instrument with default pyvisa settings."""
        rm = pyvisa.ResourceManager()
        return cls(address = adr, rm = rm)
    
    def write(self, cmd: str):
        """Send a command to the instrument."""
        self.resource.write(cmd)

    def query(self, cmd: str) -> str:
        """Send a query to the instrument and return the response."""
        return self.resource.query(cmd)
    
    def query_binary_values(self, cmd, datatype='h', is_big_endian=True):
        return self.resource.query_binary_values(cmd, datatype=datatype, is_big_endian=is_big_endian)
    
    def close(self):
        """Close the connection to the instrument."""
        self.resource.close()

class SCPIParameter:
    def __init__(self, getter, setter):
        object.__setattr__(self, '_getter', getter)
        object.__setattr__(self, '_setter', setter)

    def get(self, *args):
        if self._getter is None:
            raise AttributeError("This parameter is set-only")
        return self._getter(*args)

    def set(self, *args):
        if self._setter is None:
            raise AttributeError("This parameter is read-only")
        return self._setter(*args)

    def __setattr__(self, name, value):
        raise AttributeError(f"Cannot assign to '{name}' directly. Use .set() instead.")