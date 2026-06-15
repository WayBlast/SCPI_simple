import sys
sys.path.append("api")
from packet import *
from header import *
import time

def sendPacket(ArduinoUnoSerial, Packet):
    packetBytes = Packet.to_bytearray()
    ArduinoUnoSerial.write(packetBytes)

def send_AER(ArduinoUnoSerial, input_array):
    for input in input_array:
        sendPacket(ArduinoUnoSerial, Data32bitPacket(header = Data32bitHeader.IN_AER_TO_CHIP0, value = input))

def send_SPI0(ArduinoUnoSerial, input_array):
    SPI0_POWER = 14

    sendPacket(ArduinoUnoSerial, PinPacket( header = PinHeader.IN_PIN, pin_id = SPI0_POWER, value = 1))

    for input in input_array:
        sendPacket(ArduinoUnoSerial, Data8bitPacket(header = Data8bitHeader.IN_SPI0, value = input))

    sendPacket(ArduinoUnoSerial, PinPacket( header = PinHeader.IN_PIN, pin_id = SPI0_POWER, value = 0))    

def send_SPI1(ArduinoUnoSerial, input_array):
    SPI1_POWER = 0

    sendPacket(ArduinoUnoSerial, PinPacket( header = PinHeader.IN_PIN, pin_id = SPI1_POWER, value = 1))                                         # set pin HIGH.

    for input in input_array:
        sendPacket(ArduinoUnoSerial, Data8bitPacket(header = Data8bitHeader.IN_SPI1, value = input))

    sendPacket(ArduinoUnoSerial, PinPacket( header = PinHeader.IN_PIN, pin_id = SPI1_POWER, value = 0))    

def read_buffer(ArduinoUnoSerial):
    sendPacket(ArduinoUnoSerial, Data32bitPacket(header = Data32bitHeader.IN_READ))
    time.sleep(1)
    while(ArduinoUnoSerial.in_waiting > 8):
        packetRead = ArduinoUnoSerial.read(size = 9)
        message = Packet.from_bytearray(packetRead)
        print("read back:", message)
