from ..instruments.base import SCPIParameter

class Acquire:
    """Acquire subsystem 

    For the configuration and retrieval of data acquisition settings on the oscilloscope. 
    This includes setting the acquisition mode, number of acquisitions, and controlling the acquisition state.
    """
    params:      SCPIParameter
    mode:        SCPIParameter
    number:      SCPIParameter
    number_env:  SCPIParameter
    state:       SCPIParameter
    stop_after:  SCPIParameter
    
    def __init__(self, instrument):
        """Subsystem for controlling acquisition on the instrument."""
        object.__setattr__(self, "_inst", instrument)

        object.__setattr__(self, "params",      SCPIParameter(getter=self._get_params,    setter=None))
        object.__setattr__(self, "mode",        SCPIParameter(getter=None,               setter=self._set_mode))
        object.__setattr__(self, "number",      SCPIParameter(getter=self._get_number,    setter=self._set_number))
        object.__setattr__(self, "number_env",  SCPIParameter(getter=None,               setter=self._set_number_env))
        object.__setattr__(self, "state",       SCPIParameter(getter=None,               setter=self._set_state))
        object.__setattr__(self, "stop_after",  SCPIParameter(getter=None,               setter=self._set_stop_after))
    
    def __setattr__(self, name, value):
        if isinstance(value, SCPIParameter):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                f"Cannot assign to '{name}' directly. Use .set() instead."
            )
  
    def _get_params(self):
        """Query the current acquisition parameters."""
        return self._inst.query("ACQuire?")
    
    def _set_mode(self, mode):
        """Set the acquisition mode. Valid modes are: normal, peak, average, envelope.
        
        Args:       
            mode (str): The acquisition mode to set.
        """
        match mode.lower():
            case "normal":
                self._inst.write("ACQuire:MODE NORMal")
            case "peak":
                self._inst.write("ACQuire:MODE PEAK")
            case "average":
                self._inst.write("ACQuire:MODE AVErage")
            case "envelope":
                self._inst.write("ACQuire:MODE ENVelope")
            case _:
                raise Exception(f"Acquire mode: {mode} not defined: Pick normal, peak, average or envelope")

    def _get_number(self):
        """Query the number of acquisitions to perform.

        Returns:
            int: The number of acquisitions to perform.
        """
        return self._inst.query("ACQuire:NUMACq?")
    
    def _set_number(self, acqs: int):
        """Set the number of acquisitions to perform. Must be a positive integer.

        args: 
            acqs (int): The number of acquisitions to perform.
        """
        try:
            self._inst.write(f"ACQuire:NUMACq {acqs}")
        except Exception as e:
            raise Exception(f"Error setting acquire number: {e}")

    def _set_number_env(self, acqs: int):
        """Set the number of acquisitions to envelope mode.
        args:
            acqs (int): The number of acquisitions to envelope mode."""
        try:
            self._inst.write(f"ACQuire:NUMACq ENVelope {acqs}")
        except Exception as e:
            raise Exception(f"Error setting acquire number to envelope: {e}")

    def _set_state(self, state: int):
        """Set the acquisition state. Valid states are 0 (off) and 1 (on).
        Args:            
            state (int): The acquisition state to set.
        """
        if state == 1:
            self._inst.write(f"ACQuire:STATE ON")
        elif state == 0:
            self._inst.write(f"ACQuire:STATE OFF")
        else:
            raise Exception("Acquire state not defined")

    def _set_stop_after(self, stop):
        """Set the acquisition stop condition. Valid options are: runstop, sequence.
        Args:
            stop (str): The acquisition stop condition to set.
        """
        match stop.lower():
            case "runstop":
                self._inst.write("ACQuire:STOPAfter RUNSTop")
                
            case "sequence":
                self._inst.write("ACQuire:STOPAfter SEQUENCE")
                
            case _:
                raise Exception("Acquisition stop not defined")
            

            
        
        