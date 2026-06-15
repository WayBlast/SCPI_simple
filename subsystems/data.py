from ..instruments.base import SCPIParameter

class Data:
    """
    Data subsystem for retrieving and setting data-related parameters on the instrument.
    This includes configuring the data source, encoding, data width, and retrieving waveform preamble information such as x increment and y scaling factors.
    """
    source:          SCPIParameter
    encoding:        SCPIParameter
    data_width:      SCPIParameter
    start:           SCPIParameter
    stop:            SCPIParameter
    x_increment:     SCPIParameter
    x_zero:          SCPIParameter
    y_multiplier:   SCPIParameter
    y_offset:        SCPIParameter
    y_zero:          SCPIParameter

    def __init__(self, instrument):

        object.__setattr__(self, '_inst', instrument)

        object.__setattr__(self, 'source', SCPIParameter(
            getter=self._get_source,
            setter=self._set_source
        ))
        object.__setattr__(self, 'encoding', SCPIParameter(
            getter=self._get_encoding,
            setter=self._set_encoding
        ))
        object.__setattr__(self, 'data_width', SCPIParameter(
            getter=self._get_data_width,
            setter=self._set_data_width
        ))
        object.__setattr__(self, 'start', SCPIParameter(
            getter=self._get_start,
            setter=self._set_start
        ))
        object.__setattr__(self, 'stop', SCPIParameter(
            getter=self._get_stop,
            setter=self._set_stop
        ))
        object.__setattr__(self, 'channel_scale', SCPIParameter(
            getter=self._get_channel_scale,
            setter=self._set_channel_scale
        ))
        object.__setattr__(self, 'x_increment', SCPIParameter(
            getter=self._get_x_increment,
            setter=None
        ))
        object.__setattr__(self, 'x_zero', SCPIParameter(
            getter=self._get_x_zero,
            setter=None
        ))
        object.__setattr__(self, 'y_multiplier', SCPIParameter(
            getter=self._get_y_multiplier,
            setter=None
        ))
        object.__setattr__(self, 'y_offset', SCPIParameter(
            getter=self._get_y_offset,
            setter=None
        ))
        object.__setattr__(self, 'y_zero', SCPIParameter(
            getter=self._get_y_zero,
            setter=None
        ))


    def __setattr__(self, name, value):
        if isinstance(value, SCPIParameter):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                f"Cannot assign to '{name}' directly. Use .set() instead."
            )

    def _get_source(self):
        """Query the current data source channel.
        
        Returns:
            int: The current data source channel number (1-4).
        """
        return self._inst.query("DATa:SOURCE?")

    def _set_source(self, source: int):
        """ Set the data source channel. Valid channels are 1-4, corresponding to CH1-CH4 on the oscilloscope.

        args: 
            source (int):
                The channel number to set as the data source. Must be an integer from 1 to 4.
        """
        match source:
            case 1: self._inst.write('DATa:SOURCE CH1')
            case 2: self._inst.write('DATa:SOURCE CH2')
            case 3: self._inst.write('DATa:SOURCE CH3')
            case 4: self._inst.write('DATa:SOURCE CH4')
            case _: raise ValueError(f"Channel {source} not defined: Pick channel 1-4")

    def _get_encoding(self):
        """Query the current data encoding format.

        Returns:
            str: The current data encoding format, typically 'ASCII', 'RIBinary' or 'SRIBinary'.
        """
        return self._inst.query("DATa:ENCDG?")

    def _set_encoding(self, enc: str):
        """Set the data encoding format. Valid encodings are 'ASCII', 'RIBinary' and 'SRIBinary'.

        args:
            enc (str): The data encoding format to set. Must be 'ASCII', 'R
        """
        match enc.lower():
            case "ascii":    self._inst.write('DATa:ENCDG ASCI')
            case "ribinary": self._inst.write('DATa:ENCDG RIBINARY')
            case "sribinary":self._inst.write('DATa:ENCDG SRIBINARY')
            case _: raise ValueError(f"Encoding '{enc}' not defined - must be 'ASCII', 'RIBinary' or 'SRIBinary'")

    def _get_data_width(self):
        """Query the current data width in bytes per point.

        Returns:
            int: The current data width in bytes per point, typically 1 or 2 depending on the encoding format.
        """
        return self._inst.query("DATa:WIDth?")

    def _set_data_width(self, width: int):
        """Set the data width in bytes per point. Valid widths are typically 1 or 2, depending on the encoding format.

        args:
            width (int): The data width to set in bytes per point. Must be a positive
        """
        if width < 1:
            raise ValueError("Data width cannot be less than one byte per point")
        self._inst.write(f'DATa:WIDth {width}')

    def _get_start(self):
        """Query the current data start point index.

        Returns:
            int: The current data start point index, which is the index of the first data point.

        """
        return self._inst.query("DATa:STARt?")

    def _set_start(self, start: int):
        """Set the data start point index. This is the index of the first data point to retrieve when querying waveform data.

        args:
            start (int): The data start point index to set. Must be a non-negative integer
        """
        if start < 0:
            raise ValueError("Data start cannot be before first point")
        self._inst.write(f'DATa:STARt {start}')

    def _get_stop(self):
        """Query the current data stop point index.

        Returns:
            int: The current data stop point index, which is the index of the last data point.
        """
        return self._inst.query("DATa:STOP?")

    def _set_stop(self, stop: int):
        """Set the data stop point index. This is the index of the last data point to retrieve when querying waveform data.
        
        args:            
            stop (int): The data stop point index to set. Must be a non-negative integer and cannot be less than the start index.
        """
        if stop < 0:
            raise ValueError("Data stop cannot be before first point")
        self._inst.write(f'DATa:STOP {stop}')

    def _set_channel_scale(self, channel: int, scale: float):
        """Set the scale factor for the specified channel. 

        args:
            channel (int): The channel number to set the scale for. Must be an integer from 1 to 4.
            scale (float): The scale factor to set for the channel. Must be a positive number representing volts per division.
        """
        match channel:
            case 1:
                if not (scale < 0):
                    self._inst.write(f'CH1:SCALE {scale}')
                else:
                    raise Exception("Data scale cannot be less than 0")  
            case 2:
                if not (scale < 0):
                    self._inst.write(f'CH2:SCALE {scale}')
                else:
                    raise Exception("Data scale cannot be less than 0") 
            case 3:
                if not (scale < 0):
                    self._inst.write(f'CH3:SCALE {scale}')
                else:
                    raise Exception("Data scale cannot be less than 0") 
            case 4:
                if not (scale < 0):
                    self._inst.write(f'CH4:SCALE {scale}')
                else:
                    raise Exception("Data scale cannot be less than 0") 
            case _:
                raise Exception(f"Channel: {channel} not defined: Pick channel 1-4")
    
    def _get_channel_scale(self, channel: int):
        """Query the scale factor for the specified channel. 

        args:
            channel (int): The channel number to query the scale for. Must be an integer from 1 to 4.

        Returns:
            float: The scale factor for the specified channel.
        """
        if channel not in range(1, 5):
            raise Exception(f"Channel: {channel} not defined: Pick channel 1-4")
        return self._inst.query(f'CH{channel}:SCALE?')

    def _get_x_increment(self):
        """Query the x increment (time per sample) from the waveform preamble.

        Returns:
            float: The x increment in seconds per sample, which can be used to convert sample indices to time values.
        """
        return self._inst.query("WFMPRE:XINCR?")

    def _get_x_zero(self):
        """Query the x zero (starting time) from the waveform preamble.

        Returns:
            float: The x zero in seconds, which is the timestamp of the first sample.
        """
        return self._inst.query("WFMPRE:XZERO?")
    
    def _get_y_multiplier(self):
        """Query the y multiplier (volts per ADC count) from the waveform preamble.

        Returns:
            float: The y multiplier in volts per ADC count, which can be used to convert raw data points to voltage values.
        """
        return self._inst.query("WFMPRE:YMULT?")
    
    def _get_y_offset(self):
        """Query the y offset (voltage offset) from the waveform preamble.
        Returns:
            float: The y offset in ADC counts, which can be used to convert raw data points to voltage values.
        """
        return self._inst.query("WFMPRE:YOFF?")
    
    def _get_y_zero(self):
        """Query the y zero (voltage zero) from the waveform preamble.
        Returns:
            float: The y zero in volts, which is the voltage reference point for the waveform data.
        """
        return self._inst.query("WFMPRE:YZERO?")
    
    def get_curve(self):
        """Query the waveform data points as python integers.
        
        Convert to voltage as follows:
        voltage = (raw - y_off) * y_mult + y_zero

        Returns:
            list[int]: The raw waveform data points as integers, which can be converted to voltage values.
        """
        return self._inst.query_binary_values('CURVe?', datatype='h', is_big_endian=True)