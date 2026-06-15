# Run from root with: python -m examples.sweep_dc
import time
import sys
import csv
import pyvisa
from ctypes import *
import dwfconstants
import time
import numpy as np
import matplotlib.pyplot as plt
from scpi_simple.instruments.psu import Psu
from scpi_simple.instruments.osc import Osc

sys.path.append("helper")
sys.path.append("dataset")

sys.path.append("uC-chip-interface/")

from Generate_pattern_DPSS_2DE import *
from uC_api import *
from array_functions import *
from overlapping_pattern import *

SIGNAL_PARAMETER_CHANGE = 32 #30
SIGNAL_LABEL = 33 #29
TARGET_NEURON = 6
NO_EXPERIMENTS = 60
duration = 5

logging.basicConfig(level=logging.INFO)

rm = pyvisa.ResourceManager()
psu = Psu(rm, "TCPIP0::169.254.58.10::gpib0,1::INSTR")
osc = Osc(rm, "TCPIP0::169.254.58.10::gpib0,4::INSTR")

print("Configuring PSU...")
psu.apply.set("P6V", 1.8, 0.02)
psu.apply.set("P25V", 1.8, 0.02)
psu.output.state.set(1)
psu.system.beep()

print("Configuring Oscilloscope...")
osc.data.source.set(1)
osc.data.encoding.set("RIBinary")
osc.data.data_width.set(2)
osc.data.start.set(1)
osc.data.stop.set(10000)
osc.data.channel_scale.set(1, 0.1)
osc.horizontal.scale.set(duration / 10)
osc.horizontal.position.set(0)

# Read scaling factors
x_incr = float(osc.data.x_increment.get())  # seconds per sample
x_zero = float(osc.data.x_zero.get())  # timestamp of first sample
y_mult = float(osc.data.y_multiplier.get())  # volts per ADC count
y_off  = float(osc.data.y_offset.get())   # offset in counts
y_zero = float(osc.data.y_zero.get())  # voltage reference

if input("Load teensy?: y/n: " ) == "y":
    print("Initializing teensy...")
    time.sleep(20)

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

## run
for i in range(NO_EXPERIMENTS):
    try:
        
        uc.pin[33].send(value=1, time=1)
        send_dac_config(uc, sweep=i)
       
        print(f"Experiment {i+1}/{NO_EXPERIMENTS}")
        
        uc.async_to_chip[0].data_to_chip_and_clear() 
        uc.async_from_chip[0].data_from_chip_and_clear()

        #generate_spikes(uc, 50+50*i, duration*1000, TARGET_NEURON, type="exc") 
        uc.start_experiment()

        osc.acquire.stop_after.set("SEQUENCE")
        osc.acquire.state.set(1)

        logging.info("\nExperiment started")

        sleep(duration) # time it takes to run the experiment
        uc.stop_experiment()
        uc.pin[33].send(value=0, time=0)

        raw     = numpy.array(osc.data.get_curve())
        #raw     = numpy.array(scope.query_binary_values('CURVE?', datatype='h', is_big_endian=True))
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
        #
        #plt.figure(figsize=(12, 4))
        #plt.plot(time_ax * 1000, voltage)          # *1000 to convert seconds → milliseconds
        #plt.xlabel("Time (ms)")
        #plt.ylabel("Voltage (V)")
        #plt.title(f"Scope capture — Experiment {i+1}")
        #plt.grid(True)
        #plt.tight_layout()
        #plt.show()

    except Exception as e:
        uc.close_connection()
        raise Exception(f"Error in experiment {i+1}") from e

## Plot all experiments overlaid
plt.figure(figsize=(12, 4))
colors = plt.cm.tab10.colors  # up to 10 distinct colors

for i in range(NO_EXPERIMENTS):
    try:
        data    = numpy.loadtxt(f"spike_data_scope_{i+1}.csv", delimiter=',', skiprows=1)
        time_ax = data[:, 0]
        voltage = data[:, 1]
        plt.plot(time_ax * 1000, voltage, color=colors[i % len(colors)], label=f"Experiment {i+1}", alpha=0.5)
    except FileNotFoundError:
        print(f"No data file for experiment {i+1}, skipping")

plt.xlabel("Time (ms)")
plt.ylabel("Voltage (V)")
plt.title("Scope capture — All Experiments")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

## Calculate frequencies
for i in range(NO_EXPERIMENTS):
    n = 0
    try:
        with open(f'spike_data_{i+1}.csv', mode='r') as experiment:
            min_t = None
            max_t = None
            csvFile = csv.reader(experiment, delimiter=" ")
            for spike in csvFile:
                if spike[0] == '6':
                    if min_t is None:
                        min_t = max_t = int(spike[1])
                    elif int(spike[1]) > max_t:
                        max_t = int(spike[1])
                    n += 1

        if min_t is None or max_t == min_t:
            print(f"Experiment {i+1}: no spikes detected for neuron 6")
        else:
            frequency = n / (max_t - min_t) * 1_000_000
            print(f"Experiment {i+1}, neuron 6 freq: {frequency} Hz")

    except Exception as e:
        uc.close_connection()
        raise Exception(f"An error occurred in experiment {i+1}") from e

uc.close_connection()

print(uc.async_to_chip[0].errors)
