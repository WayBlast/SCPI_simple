import time
import sys
sys.path.append("api")
from packet import *
from header import *
from Packet_sender import *

SPI0_RESET = 14
SPI1_RESET = 0
AER_TO_CHIP_RESET = 31
AER_FROM_CHIP_RESET = 32

def setup_reset(ArduinoUnoSerial): 
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_PIN, config_header = ConfigSubHeader.CONF_OUTPUT, value = SPI0_RESET))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_PIN, config_header = ConfigSubHeader.CONF_OUTPUT, value = SPI1_RESET))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_PIN, config_header = ConfigSubHeader.CONF_OUTPUT, value = AER_FROM_CHIP_RESET))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_PIN, config_header = ConfigSubHeader.CONF_OUTPUT, value = AER_TO_CHIP_RESET))

# def set_reset_pins_low(ArduinoUnoSerial):
#     sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = SPI0_RESET, value = 0))
#     sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = SPI1_RESET, value = 0))
#     sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = AER_TO_CHIP_RESET, value = 0))
#     sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = AER_FROM_CHIP_RESET, value = 0))

# def set_reset_pins_high(ArduinoUnoSerial):
#     sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = SPI0_RESET, value = 1))
#     sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = SPI1_RESET, value = 1))
#     sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = AER_TO_CHIP_RESET, value = 1))
#     sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = AER_FROM_CHIP_RESET, value = 1))

def set_AER_pins_low(ArduinoUnoSerial):
    sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = AER_TO_CHIP_RESET, value = 0))
    sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = AER_FROM_CHIP_RESET, value = 0))

def set_AER_pins_high(ArduinoUnoSerial):
    sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = AER_TO_CHIP_RESET, value = 1))
    sendPacket(ArduinoUnoSerial, PinPacket(header = PinHeader.IN_PIN, pin_id = AER_FROM_CHIP_RESET, value = 1))


def resetAll(ArduinoUnoSerial):
    set_reset_pins_low(ArduinoUnoSerial)
    time.sleep(0.5)
    set_reset_pins_high(ArduinoUnoSerial)


def resetAER(ArduinoUnoSerial):
    set_AER_pins_low(ArduinoUnoSerial)
    time.sleep(0.2)
    set_AER_pins_high(ArduinoUnoSerial)
