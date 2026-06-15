import pyvisa

class Psu():
    """Interface for controlling a VISA-compatible bench power supply.

    Wraps a pyvisa resource to provide simple methods for configuring
    voltage, current, channel selection, and output state.

    Attributes:
        rm: The pyvisa ResourceManager instance.
        psu: The open pyvisa resource representing the power supply.
    """

    def __init__(self, rm, address, timeout=5000, read_termination="\n", write_termination="\n"):
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
        try:
            self.rm = rm
            self.psu = self.rm.open_resource(address)
            self.psu.timeout = timeout
            self.psu.read_termination = read_termination
            self.psu.write_termination = write_termination
        except:
            raise Exception("Error starting power supply - check device connection")

    def set_voltage(self, voltage):
        """Set the output voltage.

        Args:
            voltage: Desired voltage in volts.
        """
        self.psu.write(f"VOLT {voltage}")

    def set_channel(self, channel):
        """Select the active channel.

        Not yet implemented.

        Args:
            channel: The channel to select.
        """
        pass

    def apply(self, channel: str, voltage: float, current: float):
        """Set voltage and current limit on a specific channel.

        Sends an APPL command to configure the given channel. Does nothing
        if either voltage or current is negative.

        Args:
            channel: The channel to configure. One of 'P6V', 'N6V', 'P25V', 'N25V'.
            voltage: Desired output voltage in volts. Must be non-negative.
            current: Desired current limit in amps. Must be non-negative.

        Raises:
            Exception: If the channel name is not one of the supported options.
        """
        if not (voltage < 0) and not (current < 0):
            match channel:
                case "P6V":
                    self.psu.write(f"APPL P6V, {voltage}, {current}")
                case "N6V":
                    self.psu.write(f"APPL N6V, {voltage}, {current}")
                case "P25V":
                    self.psu.write(f"APPL P25V, {voltage}, {current}")
                case "N25V":
                    self.psu.write(f"APPL N25V, {voltage}, {current}")
                case _:
                    raise Exception("Channel in apply command not defined")

    def set_output(self, state):
        """Enable or disable the power supply output.

        Args:
            state: 1 to turn output on, 0 to turn output off.
        """
        match state:
            case 1:
                self.psu.write("OUTP ON")
            case 0:
                self.psu.write("OUTP OFF")

    def beep(self):
        """Trigger the power supply's audible beeper."""
        self.psu.write("SYSTem:BEEPer:IMMEdiate")
        
#print("Configuring PSU...")
#psu.write("APPL P6V, 1.8, 0.02")
#psu.write("APPL P25V, 1.8, 0.02")
#psu.write("OUTP ON") # Enable PSU
#psu.write("SYSTem:BEEPer:IMMEdiate")