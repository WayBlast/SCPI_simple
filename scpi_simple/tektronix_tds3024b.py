import pyvisa

class Tektronix_tds3024b():
    def __init__(self, rm, address, timeout=5000, read_termination = "\n", write_termination = "\n"):
        try:
            self.rm = rm
            self.osc = self.rm.open_resource(address)
            self.osc.timeout = 5000
            self.osc.read_termination = read_termination
            self.osc.write_termination = write_termination
        except:
            raise Exception("Error starting oscilloscope - check device connection")
        
    def set_data_source(self, source_channel: int):
        match source_channel:
            case 1:
                self.osc.write('DATA:SOURCE CH1')
            case 2:
                self.osc.write('DATA:SOURCE CH2')  
            case 3:
                self.osc.write('DATA:SOURCE CH3')  
            case 4:
                self.osc.write('DATA:SOURCE CH4') 
            case _:
                raise Exception(f"Channel {source_channel} not defined: Pick channel 1-4")

    def set_encoding(self, type: str):
        # "Sets or returns the format of the waveform data"
        match type.lower():
            case "ascii":
                self.osc.write('DATA:ENCDG ASCI') 
            case "ribinary":
                self.osc.write('DATA:ENCDG RIBINARY')   
            case "sribinary":
                self.osc.write('DATA:ENCDG SRIBINARY') 
            case _:
                raise Exception(f"Encoding type {type} not defined - must be 'ASCII', 'RIBinary' or 'SRIBinary'")

    def set_channel_scale(self, channel: int, scale: float):
        match channel:
            case 1:
                if not (scale < 0):
                    self.osc.write(f'CH1:SCALE {scale}')
                else:
                    raise Exception("Data scale cannot be less than 0")  
            case 2:
                if not (scale < 0):
                    self.osc.write(f'CH2:SCALE {scale}')
                else:
                    raise Exception("Data scale cannot be less than 0") 
            case 3:
                if not (scale < 0):
                    self.osc.write(f'CH3:SCALE {scale}')
                else:
                    raise Exception("Data scale cannot be less than 0") 
            case 4:
                if not (scale < 0):
                    self.osc.write(f'CH4:SCALE {scale}')
                else:
                    raise Exception("Data scale cannot be less than 0") 
            case _:
                raise Exception(f"Channel: {channel} not defined: Pick channel 1-4")
                
    def set_data_width(self, width: int):
        if not (width < 1):
            self.osc.write(f'DATA:WIDTH {width}')
        else:
            raise Exception("Data width cannot be less than one byte per point")    
    
    def set_data_start(self, start):
        if not (start < 0):
            self.osc.write(f'DATA:START {start}')
        else:
            raise Exception("Data start cannot be before first point")  
    
    def set_data_stop(self, stop):
        if not (stop < 0):
            self.osc.write(f'DATA:STOP {stop}')
        else:
            raise Exception("Data stop cannot be before first point")  
    
    def set_horizontal_scale(self, scale: int):
        self.osc.write(f'HORIZONTAL:SCALE {scale}')

    def set_horizontal_position(self, position):
        self.osc.write(f'HORIZONTAL:POSITION {position}') 

    
#scope.write('HORIZONTAL:POSITION 0')               # capture full duration from trigger

# Read scaling factors
#x_incr = float(scope.query('WFMPRE:XINCR?'))  # seconds per sample
#x_zero = float(scope.query('WFMPRE:XZERO?'))  # timestamp of first sample
#y_mult = float(scope.query('WFMPRE:YMULT?'))  # volts per ADC count
#y_off  = float(scope.query('WFMPRE:YOFF?'))   # offset in counts
#y_zero = float(scope.query('WFMPRE:YZERO?'))  # voltage reference