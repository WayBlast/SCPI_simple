import time
import sys
import csv
import pyvisa
from ctypes import *
import dwfconstants
import time
import numpy as np
import matplotlib.pyplot as plt
from scpi_simple import tektronix_tds3024b as tektronix
from scpi_simple.instruments.psu import Psu
from scpi_simple.instruments.osc import Osc

sys.path.append("helper")
sys.path.append("dataset")

sys.path.append("uC-chip-interface/")

from Generate_pattern_DPSS_2DE import *
from uC_api import *
from array_functions import *
#from wave_regression import *
#from wbcancer import *
from overlapping_pattern import *

SIGNAL_PARAMETER_CHANGE = 32 #30
SIGNAL_LABEL = 33 #29
TARGET_NEURON = 6
NO_EXPERIMENTS = 1
duration = 3

#logging.basicConfig(filename='out.log', encoding='utf-8',level=logging.INFO)
logging.basicConfig(level=logging.INFO)

rm = pyvisa.ResourceManager()
psu = Psu(rm, "TCPIP0::169.254.58.10::gpib0,1::INSTR")
osc = Osc(rm, "TCPIP0::169.254.58.10::gpib0,4::INSTR")
#power_supply = psu.Psu(rm=rm, address="TCPIP0::169.254.58.10::gpib0,1::INSTR")
osc = tektronix.Tektronix_tds3024b(rm=rm, address="TCPIP0::169.254.58.10::gpib0,4::INSTR")
#rm = pyvisa.ResourceManager()  
#print(rm.list_resources())
#psu = rm.open_resource("TCPIP0::169.254.58.10::gpib0,1::INSTR")
#psu.timeout = 5000
#psu.read_termination = "\n"
#psu.write_termination = "\n"

scope = rm.open_resource("TCPIP0::169.254.58.10::gpib0,4::INSTR")
scope.timeout = 5000

print("Configuring PSU...")
psu.apply.set("P6V", 1.8, 0.02)
psu.apply.set("P25V", 1.8, 0.02)
psu.output.state.set(1)
psu.system.beep()

#power_supply.apply("P6V", 1.8, 0.02)
#power_supply.apply("P25V", 1.8, 0.02)
#power_supply.set_output(1)
#power_supply.beep()
#psu.write("APPL P6V, 1.8, 0.02")
#psu.write("APPL P25V, 1.8, 0.02")
#psu.write("OUTP ON") # Enable PSU
#psu.write("SYSTem:BEEPer:IMMEdiate")

print("Configuring Oscilloscope...")
#osc.set_data_source(1)
#osc.set_encoding("RIBinary")
#osc.set_data_width(2)
#osc.set_data_start(1)
#osc.set_data_stop(10000)
#osc.set_channel_scale(1, 0.1)
#osc.set_horizontal_scale(duration/10)
#osc.set_horizontal_position(0)
#osc.beep()

scope.write('DATA:SOURCE CH1')        # Read data from channel 1
scope.write('DATA:ENCDG RIBINARY')    # Binary encoding, faster than ASCII over GPIB
scope.write('DATA:WIDTH 2')           # 2 bytes per sample, more precision than 1 byte
scope.write('DATA:START 1')           # Start from first sample point
scope.write('DATA:STOP 10000')        # Up to 10000 sample points per capture
scope.write('CH1:SCALE 0.1')   # 100mV/div → 800mV range
scope.write("SYSTem:BEEPer:IMMEdiate")
scope.write(f'HORIZONTAL:SCALE {duration / 10}')  # duration(s) / 10 divisions = s/div
scope.write('HORIZONTAL:POSITION 0')               # capture full duration from trigger
scope.write('HORIZONTAL:POSITION 10')  # trigger at 10% from left                                

# Read scaling factors

x_incr = float(scope.query('WFMPRE:XINCR?'))  # seconds per sample
x_zero = float(scope.query('WFMPRE:XZERO?'))  # timestamp of first sample
y_mult = float(scope.query('WFMPRE:YMULT?'))  # volts per ADC count
y_off  = float(scope.query('WFMPRE:YOFF?'))   # offset in counts
y_zero = float(scope.query('WFMPRE:YZERO?'))  # voltage reference

"""
# Starting Osciloscope
# 1. Load the SDK library
dwf = cdll.LoadLibrary("libdwf.so")
 
# 2. Open the first connected device
hdwf = c_int()
dwf.FDwfDeviceOpen(-1, byref(hdwf))

if hdwf.value == dwfconstants.hdwfNone.value:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print("Device open failed:", str(szerr.value))
    quit()
#declare ctype variables

sts = c_byte()
hzAcq = c_double(100000)
nSamples = 10000
rgdSamples = (c_double*nSamples)()
cAvailable = c_int()
cLost = c_int()
cCorrupted = c_int()
fLost = 0
fCorrupted = 0
# 3. Configure the oscilloscope (AnalogIn)
dwf.FDwfAnalogInAcquisitionModeSet(hdwf, c_int(3))  # 3 = record mode
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(sample_rate))  # sample rate
dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double(duration)) # record duration
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_int(1))  # enable CH1
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(0.5))  # ±200 mV range
"""


if input("Load teensy?: y/n: " ) == "y":
    print("Initializing teensy...")
    sleep(20)

print("program start")
uc = uC_api('/dev/ttyACM0',2)

setup(uc)
print("Setup completed")

## set config and monitorsDwfStateC
print("Configs started")
# set monitors
send_fast_config(uc)
# set parameters
send_dac_config(uc,sweep=10)
print("Configs completed")


uc.pin[SIGNAL_PARAMETER_CHANGE].activate(pin_mode="OUTPUT")
uc.pin[SIGNAL_LABEL].activate(pin_mode="OUTPUT")

sleep(5)
## read weights after power up (debbuggig only)
# uc.pin[Spsu.write("INST P25V")IGNAL_PARAMETER_CHANGE].send(value=1)
# cycle_through_synapses(uc, neuron=TARGET_NEURON)
# uc.pin[SIGNAL_PARAMETER_CHANGE].send(value=0)
# print("synapses cycled")

## set weights
#init_dpss_weights(uc, neuron=TARGET_NEURON, force_0=False)
#uc.start_experiment()
#print("starting experiment, setting weights")
#sleep(10)
#print("stopping experiment")
#uc.stop_experiment()

## read set weights
# uncomment 6 linesbelow to read weight before training
# sleep(20)
# uc.pin[SIGNAL_PARAMETER_CHANGE].send(value=1)
# cycle_through_synapses(uc, neuron=TARGET_NEURON)s223946@ma-322125a ~/Project/repo $ git clon
# uc.pin[SIGNAL_PARAMETER_CHANGE].send(value=0)
# print("synapses cycled")
# sleep(20)

## experiment

## create spikes from paterns
#spike_array, label_array, start_validation, end_baseline, end_t = oj_200ms(invert=True,disable_teacher=False)
## send spikes to chip
#create_AER_input_from_dataset(uc, spike_array, start_validation, end_baseline, end_t, None, SIGNAL_PARAMETER_CHANGE, SIGNAL_LABEL, TARGET_NEURON)
## clear data before run
#uc.async_from_chip[0].data_from_chip_and_clear()

## run
for i in range(NO_EXPERIMENTS):
    try:
        
        uc.pin[33].send(value=1, time=1)
        send_dac_config(uc, sweep=i)
        #spike_array, label_array, start_validation, end_baseline, end_t = oj_200ms(invert=True,disable_teacher=False, regular=False, seed=i)
        #spike_array,end_baseline, start_validation, end_t  = generate_spike_times(6_000_000)
        
        #print(f"spike_array:\n{spike_array}\n\nlabel_array:\n{label_array}\n\nstart_validation: {start_validation}\nend_baseline: {end_baseline}\nend_t: {end_t}")
        print(f"Experiment {i+1}/{NO_EXPERIMENTS}")
        #sleep(15)
        
        uc.async_to_chip[0].data_to_chip_and_clear() 
        uc.async_from_chip[0].data_from_chip_and_clear()
        #create_AER_input_simple(uc, spike_array, start_validation, end_baseline, end_t, None, SIGNAL_PARAMETER_CHANGE, SIGNAL_LABEL, TARGET_NEURON)
        #create_AER_input_from_dataset(uc, spike_array, start_validation, end_baseline, end_t, None, SIGNAL_PARAMETER_CHANGE, SIGNAL_LABEL, TARGET_NEURON)
        generate_spikes(uc, 300, duration*1000, TARGET_NEURON, regular=False) 
        uc.start_experiment()

        scope.write('ACQUIRE:STOPAFTER SEQUENCE')
        scope.write('ACQUIRE:STATE ON')

        logging.info("\nExperiment started")

        sleep(duration) # time it takes to run the experiment
        uc.stop_experiment()
        uc.pin[33].send(value=0, time=0)

        raw     = numpy.array(scope.query_binary_values('CURVE?', datatype='h', is_big_endian=True))
        time_ax = x_zero + x_incr * numpy.arange(len(raw))
        voltage = (raw - y_off) * y_mult + y_zero

        numpy.savetxt(f"spike_data_scope_{i+1}.csv", numpy.array([time_ax, voltage]).T, header='time_s,voltage_v', delimiter=',')

        spike_data, spike_time = uc.async_from_chip[0].data_from_chip_and_clear()
        numpy.savetxt(f"spike_data_{i+1}.csv", numpy.array([spike_data, spike_time]).T, fmt='%d %d', delimiter=',')
        spike_data_out, spike_time_out = uc.async_to_chip[0].data_to_chip_and_clear()
        numpy.savetxt(f"spike_data_out_{i+1}.csv", numpy.array([spike_data_out, spike_time_out]).T, fmt='%d %d', delimiter=',')

        data = numpy.loadtxt(f"spike_data_scope_{i+1}.csv", delimiter=',', skiprows=1)
        time_ax = data[:, 0]
        voltage = data[:, 1]

        # Plot
        plt.figure(figsize=(12, 4))
        plt.plot(time_ax * 1000, voltage)          # *1000 to convert seconds → milliseconds
        plt.xlabel("Time (ms)")
        plt.ylabel("Voltage (V)")
        plt.title("Scope capture — Experiment 1")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        uc.close_connection()
        raise Exception(f"Error in experiment {i+1}") from e

"""
for i in range(NO_EXPERIMENTS):
    try:
        # Reset per-experiment state
        cSamples = 0
        cAvailable = c_int()
        cLost = c_int()
        cCorrupted = c_int()
        fLost = 0
        fCorrupted = 0
        rgdSamples = (c_double * nSamples)()  # clear buffer

        send_dac_config(uc, sweep=i)
        print(f"Experiment {i+1}/{NO_EXPERIMENTS}")
        sleep(15)

        uc.async_from_chip[0].data_from_chip_and_clear()
        uc.start_experiment()

        dwf.FDwfAnalogInConfigure(hdwf, 1, 0)  # apply settings
        time.sleep(2)
        dwf.FDwfAnalogInConfigure(hdwf, 0, 1)  # start acquisition
        logging.info("\nExperiment started")

        while cSamples < nSamples:
            dwf.FDwfAnalogInStatus(hdwf, 1, byref(sts))
            if cSamples == 0 and (
                sts.value == dwfconstants.DwfStateConfig.value or
                sts.value == dwfconstants.DwfStatePrefill.value or
                sts.value == dwfconstants.DwfStateArmed.value
            ):
                continue

            dwf.FDwfAnalogInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))
            cSamples += cLost.value

            if cLost.value:     fLost = 1
            if cCorrupted.value: fCorrupted = 1
            if cAvailable.value == 0: continue

            if cSamples + cAvailable.value > nSamples:
                cAvailable.value = nSamples - cSamples

            dwf.FDwfAnalogInStatusData(hdwf, 0, byref(rgdSamples, sizeof(c_double) * cSamples), cAvailable)
            cSamples += cAvailable.value

        uc.stop_experiment()
        logging.info("Experiment stopped")

        # Save oscilloscope data
        np.savetxt(f"scope_data_{i+1}.csv", np.fromiter(rgdSamples, dtype=float), delimiter=",")

        # Save spike data (same format as commented-out section)
        spike_data, spike_time = uc.async_from_chip[0].data_from_chip_and_clear()
        np.savetxt(f"spike_data_{i+1}.csv", np.array([spike_data, spike_time]).T, fmt='%d %d', delimiter=',')

        print(f"Recording done (experiment {i+1})")
        if fLost:      print("Samples were lost! Reduce frequency")
        if fCorrupted: print("Samples could be corrupted! Reduce frequency")

        # 7. Plot
        samples = np.array(rgdSamples)

        N = nSamples
        time_ms = np.linspace(0, duration * 1000, N)

        plt.plot(time_ms, samples)
        plt.xlabel("Time (ms)")
        plt.ylabel("Voltagasync_to_chipe (V)")
        plt.title("CH1 Recording")
        plt.grid(True)
        plt.show()
    except Exception as e:
        uc.close_connection()
        raise Exception(f"Error in experiment {i+1}") from e

        send_dac_config(uc,sweep=i)
        
        print(f"Experiment {i+1}/{NO_EXPERIMENTS}")
        sleep(15)

        # 4. Arm the oscilloscope and wait for it to finish capturing
        dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))  # 2nd arg=0: apply settings | 3rd arg=1: start capture
        ## clear data before run
        uc.async_from_chip[0].data_from_chip_and_clear()
        uc.start_experiment()
        logging.info("\nExperiment started")

        sleep(5) # time it takes to run the experiment
        uc.stop_experiment()

        spike_data, spike_time = uc.async_from_chip[0].data_from_chip_and_clear()
        numpy.savetxt(f"spike_data_{i+1}.csv", numpy.array([spike_data, spike_time]).T, fmt='%d %d', delimiter=',')

        buf = (c_double * int(sample_rate * duration))()
        dwf.FDwfAnalogInStatusData(hdwf, c_int(0), buf, c_int(len(buf)))

        numpy.savetxt("scope_recording.csv", numpy.array(buf), delimiter=",")

        # 6. Close the device
        dwf.FDwfDeviceClose(hdwf)

        # 7. Plot
        samples = np.array(buf)

        N = len(samples)
        time_ms = np.linspace(0, duration * 1000, N)

        plt.plot(time_ms, samples)
        plt.xlabel("Time (ms)")
        plt.ylabel("Voltagasync_to_chipe (V)")
        plt.title("CH1 Recording")
        plt.grid(True)
        plt.show()"""
     

## Calculate frequencies
for i in range(NO_EXPERIMENTS):
    n = 0
    try:
        with open(f'spike_data_{i+1}.csv', mode='r') as experiment:
            min = None
            max = None
            csvFile = csv.reader(experiment, delimiter = " ")
            for spike in csvFile:
                
                if spike[0] == '6':
                    if min == None:    
                        min = max = int(spike[1])
                    elif int(spike[1]) > max:
                        max = int(spike[1])
                    n += 1
        frequency = n/(max-min) * 1_000_000 
        print(f"Experiment {i+1}, neuron 6 freq: {frequency} Hz")    
    except: 
        uc.close_connection() 
        raise Exception("An error occured") 

""" ## new run
send_dac_config(uc,sweep=10)
sleep(10)
## run
uc.start_experiment()
logging.info("Experiment started")

sleep(15) # time it takes to run the experiment
uc.stop_experiment()

spike_data, spike_time = uc.async_from_chip[0].data_from_chip_and_clear()
numpy.savetxt("spike_data.csv", numpy.array([spike_data, spike_time]).T, fmt='%d %d', delimiter=',')
print(numpy.array([spike_data, spike_time]).T)
 """
## new run

## weights read after

# uncomment 6 linesbelow to read weight after training
# sleep(20)
# uc.pin[SIGNAL_PARAMETER_CHANGE].send(value=1)
# cycle_through_synapses(uc, neuron=TARGET_NEURON)
# uc.pin[SIGNAL_PARAMETER_CHANGE].send(value=0)
# print("synapses cycled")
# sleep(20)

uc.close_connection()
""" # save spike data
spike_data, spike_time = uc.async_from_chip[0].data_from_chip_and_clear()
numpy.savetxt("spike_data.csv", numpy.array([spike_data, spike_time]).T, fmt='%d %d', delimiter=',')
print(numpy.array([spike_data, spike_time]).T) """

print(uc.async_to_chip[0].errors)


#print(uc.errors)