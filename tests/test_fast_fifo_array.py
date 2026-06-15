import serial
import time
import sys
import subprocess
import sys
from enum import Enum

sys.path.append("helper")

sys.path.append("uC-chip-interface-teensy41/")

from Generate_pattern_DPSS_2DE import *
from uC_api import *
from array_functions import *

logging.basicConfig(level=logging.INFO)

uc = uC_api('/dev/ttyACM0',2)

setup(uc)
uc.start_experiment()
send_fast_config(uc)
sleep(2)
uc.spi[0].data_from_chip_and_clear()
uc.spi[0].data_to_chip_and_clear()
send_fast_config(uc)
sleep(1)

in_pack = uc.spi[0].data_from_chip_and_clear()
out_pack = uc.spi[0].data_to_chip_and_clear()

print(in_pack)
print(out_pack)
print(uc.spi[0])



uc.stop_experiment()
uc.close_connection()

print(uc.errors)

print("programming takes [us]:"+str(in_pack[1][-1]-in_pack[1][0]))
print("RESULT: fifo is working: " + str(all([a == b for a, b in zip(in_pack[0], out_pack[0])])))