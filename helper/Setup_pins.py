import sys
sys.path.append("api")
from packet import *
from header import *
from Packet_sender import sendPacket
from Reset_pins import setup_reset

def setup_SPI0(ArduinoUnoSerial):
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_SPI0, config_header = ConfigSubHeader.CONF_ACTIVE))

def setup_SPI1(ArduinoUnoSerial):
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_SPI1, config_header = ConfigSubHeader.CONF_ACTIVE))


def setup_AER_TO_CHIP(ArduinoUnoSerial):
    AER_ACK = 34
    AER_REQ = 33
    AER_WIDTH = 10
    AER_PINS = [36, 35, 16, 17, 18, 19, 20, 21, 22, 23]
    AER_DELAY = 5
    HS_ACTIVE_LOW = 0

    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_TO_CHIP0, config_header = ConfigSubHeader.CONF_ACK, value = AER_ACK))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_TO_CHIP0, config_header = ConfigSubHeader.CONF_REQ, value = AER_REQ))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_TO_CHIP0, config_header = ConfigSubHeader.CONF_WIDTH, value = AER_WIDTH))
    for pin in range(AER_WIDTH):
        sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_TO_CHIP0, config_header = ConfigSubHeader(pin), value = AER_PINS[pin]))
    
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_TO_CHIP0, config_header = ConfigSubHeader.CONF_REQ_DELAY, value = AER_DELAY))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_TO_CHIP0, config_header = ConfigSubHeader.CONF_HS_ACTIVE_LOW, value = HS_ACTIVE_LOW))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_TO_CHIP0, config_header = ConfigSubHeader.CONF_ACTIVE))

def setup_AER_FROM_CHIP(ArduinoUnoSerial):
    AER_ACK = 8
    AER_REQ = 3
    AER_WIDTH = 4
    AER_PINS = [4, 5, 6, 7]
    AER_DELAY = 5
    HS_ACTIVE_LOW = 0

    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_FROM_CHIP0, config_header = ConfigSubHeader.CONF_ACK, value = AER_REQ))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_FROM_CHIP0, config_header = ConfigSubHeader.CONF_REQ, value = AER_ACK))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_FROM_CHIP0, config_header = ConfigSubHeader.CONF_WIDTH, value = AER_WIDTH))
    for pin in range(AER_WIDTH):
        sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_FROM_CHIP0, config_header = ConfigSubHeader(pin), value = AER_PINS[pin]))
    
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_FROM_CHIP0, config_header = ConfigSubHeader.CONF_REQ_DELAY, value = AER_DELAY))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_FROM_CHIP0, config_header = ConfigSubHeader.CONF_HS_ACTIVE_LOW, value = HS_ACTIVE_LOW))
    sendPacket(ArduinoUnoSerial, ConfigPacket(header = ConfigMainHeader.IN_CONF_AER_FROM_CHIP0, config_header = ConfigSubHeader.CONF_ACTIVE))

def setup(ArduinoUnoSerial):
    setup_SPI0(ArduinoUnoSerial)
    setup_SPI1(ArduinoUnoSerial)
    setup_AER_TO_CHIP(ArduinoUnoSerial)
    setup_AER_FROM_CHIP(ArduinoUnoSerial)
    setup_reset(ArduinoUnoSerial)