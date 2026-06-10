from ..instruments.base import SCPIParameter

class Data:
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
        return self._inst.query("DATa:SOURCE?")

    def _set_source(self, source: int):
        match source:
            case 1: self._inst.write('DATa:SOURCE CH1')
            case 2: self._inst.write('DATa:SOURCE CH2')
            case 3: self._inst.write('DATa:SOURCE CH3')
            case 4: self._inst.write('DATa:SOURCE CH4')
            case _: raise ValueError(f"Channel {source} not defined: Pick channel 1-4")

    def _get_encoding(self):
        return self._inst.query("DATa:ENCDG?")

    def _set_encoding(self, enc: str):
        match enc.lower():
            case "ascii":    self._inst.write('DATa:ENCDG ASCI')
            case "ribinary": self._inst.write('DATa:ENCDG RIBINARY')
            case "sribinary":self._inst.write('DATa:ENCDG SRIBINARY')
            case _: raise ValueError(f"Encoding '{enc}' not defined - must be 'ASCII', 'RIBinary' or 'SRIBinary'")

    def _get_data_width(self):
        return self._inst.query("DATa:WIDth?")

    def _set_data_width(self, width: int):
        if width < 1:
            raise ValueError("Data width cannot be less than one byte per point")
        self._inst.write(f'DATa:WIDth {width}')

    def _get_start(self):
        return self._inst.query("DATa:STARt?")

    def _set_start(self, start: int):
        if start < 0:
            raise ValueError("Data start cannot be before first point")
        self._inst.write(f'DATa:STARt {start}')

    def _get_stop(self):
        return self._inst.query("DATa:STOP?")

    def _set_stop(self, stop: int):
        if stop < 0:
            raise ValueError("Data stop cannot be before first point")
        self._inst.write(f'DATa:STOP {stop}')

    def _set_channel_scale(self, channel: int, scale: float):
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
        if channel not in range(1, 5):
            raise Exception(f"Channel: {channel} not defined: Pick channel 1-4")
        self.osc.write(f'CH{channel}:SCALE?')
                    

    def _get_x_increment(self):
        return self._inst.query("WFMPRE:XINCR?")

    def _get_x_zero(self):
        return self._inst.query("WFMPRE:XZERO?")
    
    def _get_y_multiplier(self):
        return self._inst.query("WFMPRE:YMULT?")
    
    def _get_y_offset(self):
        return self._inst.query("WFMPRE:YOFF?")
    
    def _get_y_zero(self):
        return self._inst.query("WFMPRE:YZERO?")
    
    def get_curve(self):
        return self._inst.query_binary_values('CURVe?', datatype='h', is_big_endian=True)