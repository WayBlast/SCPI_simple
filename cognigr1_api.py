import enum
import logging
import sys
import os
import time
import csv
import pandas as pd
import difflib
print(os.getcwd())
sys.path.append('../')
sys.path.append('../params')
import Generate_pattern_SynapseNorm as SYNORM
import Generate_pattern_oldTDE as oldTDE
import Generate_pattern_TDEmod as TDEDPI
import Generate_pattern_TDEmod as TDECAPPED
import Generate_pattern_PLL as PLL
import GeneratePatternDVS as Ella
import Generate_pattern_mdsn as WTA
import Generate_pattern_bistable_w_lb as BCall
import Generate_pattern_DPSS_2DE as Neuron_Array
import Generate_pattern_piezo as Piezo
from Generate_bitstream import generate_bitstream
import numpy as np
import time
sys.path.append('../uC-chip-interface-teensy41')
from uC_api import *
import serial, sys, time, struct
import serial.tools.list_ports

get_bin = lambda x, n: format(x, 'b').zfill(n)


@enum.unique
class PinLocations(enum.IntEnum) :
    """
    Enum class for the pin locations on the Teensy 4.1.
    """

    def __new__(cls, value, doc=None):
      """
      overwrite to enable __doc__ strings for enum elements as second argument.
      """
      self = int.__new__(cls, value)  # calling super().__new__(value) here would fail
      self._value_ = value
      if doc is not None:
          self.__doc__ = doc
      return self
    
    DIG_I0 = 14
    DIG_I1 = 15
    DIG_I2 = 16
    DIG_I3 = 17
    DIG_I4 = 18
    DIG_I5 = 28
    DIG_I6 = 30
    DIG_I7 = 31
    DIG_I8 = 34
    DIG_I9 = 35
    DIG_I10 = 36
    DIG_I11 = 37
    DIG_I12 = 38
    DIG_I13 = 39
    DIG_I14 = 40
    DIG_I15 = 41
    DIG_I16 = 19
    DIG_I17 = 20
    
    DIG_O0 = 3
    DIG_O1 = 4
    DIG_O2 = 5
    DIG_O3 = 6
    DIG_O4 = 7
    DIG_O5 = 8
    DIG_O6 = 9
    DIG_O7 = 2
    
    SPI0_0 = 26
    SPI0_1 = 1
    SPI0_2 = 0
    SPI0_3 = 27
    
    SPI1_0 = 11
    SPI1_1 = 12
    SPI1_2 = 10
    SPI1_3 = 13
    
    MUX0 = 21
    MUX1 = 22
    MUX2 = 23
    



class dac:
    def __init__(self, fifo_position, fifo_type, parameters, are_parameters_MS2LS, preappend=None,
                 postappend=None):
        self.fifo_position = fifo_position
        self.parameters = parameters
        self.are_parameters_MS2LS = are_parameters_MS2LS
        self.preappend = preappend
        self.postappend = postappend
        self.fifo_type = fifo_type

class config_flipflop:
    def __init__(self, fifo_position, fifo_type, parameters, are_parameters_MS2LS):
        self.fifo_position = fifo_position
        self.fifo_type = fifo_type
        self.parameters = parameters
        self.are_parameters_MS2LS = are_parameters_MS2LS

class pin:
    def __init__(self, name,gpio,pintype = '', direction = '',pad = '', initial_value = ''):
        self.name = name
        self.gpio = gpio
        self.initial_value = initial_value
        if (type(pintype) != str)| (type(direction) != str):
            self.extract_info_from_name()
        else:
            self.type = pintype
            self.direction = direction
    def extract_info_from_name(self):
        if 'vdd' in self.name:
            self.type = 'power_in'
            self.direction = 'to_chip'
        elif self.name == 'gnd!':
            self.type = 'power_in'
            self.direction = 'to_chip'
        elif 'vss' in self.name:
            self.type = 'power_in'
            self.direction = 'to_chip'
        elif '_VFO' in self.name:
            self.type = 'analog'
            self.direction = 'from_chip'
        elif '_AI' in self.name:
            self.type = 'digital'
            self.direction = 'to_chip'
        elif '_AO' in self.name:
            self.type = 'digital'
            self.direction = 'from_chip'
        elif '_VI' in self.name:
            self.type = 'analog'
            self.direction = 'to_chip'
        else:
            self.type = 'unknown'
            self.direction = 'unknown'
    def __str__(self):
        return 'Pin name: ' + str(self.name) + ' gpio: ' + str(self.gpio) + ' type: ' + str(self.type) + ' direction: ' + str(self.direction) + ' initial_value: ' + str(self.initial_value)
class aer:
    def __init__(self,type,req,ack,bus_size,data_pins,mode,req_delay,time):
        self.type = type
        self.req = req
        self.ack = ack
        self.bus_size = bus_size
        self.data_pins = data_pins
        self.mode = mode
        self.req_delay = req_delay
        self.time = time
    def __str__(self):
        return 'AER type: ' + str(self.type) + ' req: ' + str(self.req) + ' ack: ' + str(self.ack) + ' bus_size: ' + str(self.bus_size) + ' data_pins: ' + str(self.data_pins) + ' mode: ' + str(self.mode) + ' req_delay: ' + str(self.req_delay) + ' time: ' + str(self.time)
class mux:
    def __init__(self,name,sel0_n,sel1_n,sel2_n,list_of_modules):
        self.name = name
        self.sels_n = [sel0_n,sel1_n,sel2_n]
        self.list = list_of_modules
    def activate(self,uc_pins):
        for pin in self.sels_n:
            uc_pins[pin].activate(pin_mode="OUTPUT")
    def set_word(self,word,uc_pins):
        for p_idx,pin in enumerate(self.sels_n):
            uc_pins[pin].send(int(get_bin(word,len(self.sels_n))[::-1][p_idx],2))
    def __str__(self):
        return 'MUX name: ' + str(self.name) + ' sel0_n: ' + str(self.sels_n[0]) + ' sel1_n: ' + str(self.sels_n[1]) + ' sel2_n: ' + str(self.sels_n[2]) + ' list of modules: ' + str(self.list)

class spi:
    def __init__(self,clk,mosi,miso):
        self.clk = clk
        self.mosi = mosi
        self.miso = miso
    def __str__(self):
        return 'SPI clk: ' + str(self.clk) + ' mosi: ' + str(self.mosi) + ' miso: ' + str(self.miso)

class module:
        def __init__(self, name, hasfifo = False):
            self.name = name
            self.dacs = []
            self.configs_flipflop = []
            self.pins = []
            self.aers = []
            self.spis = []
            self.muxes = []
            self.active = False
            self.higherfifoposition = {}
            self.higherfifoposition['slow'] = 0
            self.higherfifoposition['fast'] = 0
            self.hasfifo = hasfifo


        def add_dac(self, fifo_position, fifo_type, parameters, are_parameters_MS2LS):
           self.dacs.append(dac(fifo_position, fifo_type, parameters, are_parameters_MS2LS))
           if fifo_position >= self.higherfifoposition[fifo_type]:
                self.higherfifoposition[fifo_type] = fifo_position
        def add_config(self, fifo_position, fifo_type, parameters, are_parameters_MS2LS=True):
            self.configs_flipflop.append(config_flipflop(fifo_position, fifo_type, parameters,are_parameters_MS2LS))

        def add_pin(self, name, type, direction, gpio, initial_value,pad=None):
            self.pins.append(pin(name = name, pintype = type, direction= direction, pad = pad, gpio=gpio, initial_value = initial_value))

        def add_aer(self,type,req,ack,bus_size,data_pins,mode,req_delay,time):
            self.aers.append(aer(type,req,ack,bus_size,data_pins,mode,req_delay,time))
        def add_spi(self,clk,mosi,miso):
            self.spis.append(spi(clk,mosi,miso))
        def add_mux(self,name,sel0_n,sel1_n,sel2_n,list_of_modules):
            self.muxes.append(mux(name,sel0_n,sel1_n,sel2_n,list_of_modules))
class cognigr1_interface:
    def __init__(self,name,serial_port = 'auto'):
        self.name = name
        self.modules = {}
        self.active_module = ''
        self.max_fifo = {}
        self.max_fifo['slow'] = 0
        self.max_fifo['fast'] = 0
        if serial_port == 'auto':
            serial_port = self.find_serial_port()
            logging.info('Serial port:', serial_port)
        self.uC = uC_api(serial_port, 2)
        ## Creating registers

        self.last_time_read = 0
        self.last_time_sent = 0

    def find_serial_port(self):
        ports = serial.tools.list_ports.comports(include_links=False)
        for port in ports:
            return port.device

    def setup(self,module):
        '''
        This function sets up the ports on Teensy according to the PCB layout (October 2023)
        '''
        ### AER TO CHIP: Used to send packages to the chip, it's just wired from GPIOs to the chip
        self.setup_aer(module)
        self.setup_pins(module)
        self.setup_spi0()
        self.setup_spi1()
        self.setup_mux()
        self.set_active_module(module)
    def update_parameter_in_dict(self,name:str,value:float):
        '''
        This function updates the value of a parameter in the internal dictionary of the API,
        after finding in which register and bit the parameter they are stored.
        @param name: str, name of the parameter
        @param value: the value of the parameter
        @return:
        '''
        for dac in self.modules[self.active_module].dacs:
            for parameter in dac.parameters:
                if parameter['name'] == name:
                    parameter['par'] = value

    def setup_aer(self,module):
        for aer in self.modules[module].aers:
            logging.info(aer)
            if aer.type == 'from_chip':
                self.uC.async_from_chip[0].activate(
                    req_pin=aer.req,
                    ack_pin=aer.ack,
                    data_width=aer.bus_size,
                    data_pins=aer.data_pins,
                    mode=aer.mode,
                    req_delay=aer.req_delay,
                    time=aer.time)
                logging.info(self.uC.async_from_chip[0])
            elif aer.type == 'to_chip':
                self.uC.async_to_chip[0].activate(
                    req_pin=aer.req,
                    ack_pin=aer.ack,
                    data_width=aer.bus_size,
                    data_pins=aer.data_pins,
                    mode=aer.mode,
                    req_delay=aer.req_delay,
                    time=aer.time)
                logging.info(self.uC.async_to_chip[0])
            else:
                raise ValueError('AER type not recognized')
    def setup_pins(self,module):
        for pin in self.modules[module].pins:
            logging.info(pin)
            if pin.type == 'digital':
                if pin.direction == 'from_chip':
                    self.uC.pin[pin.gpio].activate(pin_mode="INPUT")
                    logging.info(self.uC.pin[pin.gpio])
                elif pin.direction == 'to_chip':
                    self.uC.pin[pin.gpio].activate(pin_mode="OUTPUT")
                    logging.info(self.uC.pin[pin.gpio])
                else:
                    raise ValueError('Pin direction not recognized')
            else:
                raise ValueError('Pin type not recognized')
    def setup_spi0(self):
        for spi in self.modules['FIFO_DAC'].spis:
            logging.info(spi)
            self.uC.spi[0].activate(order='MSBFIRST')
            logging.info(self.uC.spi[0])
        self.setup_pins('FIFO_DAC')
    def setup_spi1(self):
        for spi in self.modules['FIFO_FAST'].spis:
            logging.info(spi)
            self.uC.spi[1].activate(order='MSBFIRST')
            logging.info(self.uC.spi[1])
        self.setup_pins('FIFO_FAST')
    def setup_mux(self):
        for mux in self.modules['MUX'].muxes:
            logging.info(mux)
            mux.activate(self.uC.pin)
    def start_experiment(self):
        self.uC.start_experiment()
        logging.info('Start Experiment')
    def stop_experiment(self):
        self.uC.stop_experiment()
        logging.info('Stop Experiment')
    def summarize_chip(self):
        print('Summary of the chip...')
        for module_key in self.modules.keys():
            print('Module: ' + str(module_key))
            print(' - ' + str(len(self.modules[module_key].dacs)) + ' DACS;')
            print(' - ' + str(len(self.modules[module_key].configs_flipflop)) + ' Config;')
            print(' - ' + str(len(self.modules[module_key].pins)) + ' Pins:')
            print(' - ' + str(len(self.modules[module_key].aers)) + ' AER;')
            for aer in self.modules[module_key].aers:
                print(aer)
            print('   - ' + str(len([pin for pin in self.modules[module_key].pins if pin.type == 'digital'])) + ' digital;')
            print('   - ' + str(len([pin for pin in self.modules[module_key].pins if pin.type == 'analog'])) + ' analog;')
            for pin in self.modules[module_key].pins:
                print(pin)
    def create_testing_string(self,len_word=10000):
            word = ""

            for digit in range(len_word):
                if np.mod(digit, 2) == 0:
                    word += str(0)
                else:
                    word += str(1)

            # word= "1010" + word
            return word

    def test_fifo(self,type = ''):
        if (type == 'slow') | (type == ''):
            word = self.create_testing_string(len_word=10000)
            self.send_fifo(word, type='slow')
        if (type == 'fast') | (type == ''):
            word = self.create_testing_string(len_word=10000)
            self.send_fifo(word, type='fast')
    def summarize_fifo(self,type = 'slow'):
        print('Summary of the fifo...')
        finish = False
        fifo_counter = 0
        self.find_highest_fifo(type)
        while finish == False:
            for module_key in self.modules.keys():
                # print(module_key)
                for dac_ix,dac in enumerate(self.modules[module_key].dacs):

                    if (dac.fifo_position == fifo_counter) & (dac.fifo_type == type):
                        print(str(dac.fifo_position) + ': ' + self.modules[module_key].name + ' dac' + str(dac_ix) + ' channels ' + str(len(dac.parameters)))
                        fifo_counter += 1

                for conf_ix, config_flipflop in enumerate(self.modules[module_key].configs_flipflop):

                    if (config_flipflop.fifo_position == fifo_counter)  & (config_flipflop.fifo_type == type):
                        print(str(config_flipflop.fifo_position) + ': ' + self.modules[module_key].name + ' config' + str(conf_ix) + ' channels ' + str(len(config_flipflop.parameters)))
                        fifo_counter += 1
            if fifo_counter == self.max_fifo[type]+1:
                finish = True
    def add_module(self,name,hasfifo = False):
        self.modules[name] = module(name,hasfifo)
    def set_active_module(self,name):
        self.active_module = name
        self.modules[name].active = True
        self.modules['MUX'].muxes[0].set_word(self.modules['MUX'].muxes[0].list[name],self.uC.pin)
    def find_highest_fifo(self,type):
        for key in self.modules.keys():
            if self.modules[key].higherfifoposition[type] > self.max_fifo[type]:
                    self.max_fifo[type] = self.modules[key].higherfifoposition[type]
    def find_GPIO(self,pin_name,module = '',return_outvalue = False):
        if module == '':
            module = self.active_module
        for pin in self.modules[module].pins:
            if pin.name == pin_name:
                if return_outvalue == False:
                    return int(pin.gpio)
                else:
                    return [int(pin.gpio),pin.outvalue]
    def set_pin_value(self,name,value):
        for module_key in self.modules.keys():
            for pin in self.modules[module_key].pins:
                if pin.name == name:
                    pin.outvalue = value
                    self.uC.pin[pin.gpio].send(value)
    # def read

    def create_fifo(self,type='slow'):
        finish = False
        bitstream_to_send = []
        self.find_highest_fifo(type=type)
        fifo_counter = self.max_fifo[type]
        while finish == False:
            for module_key in self.modules.keys():
                for dac in self.modules[module_key].dacs:
                    if (dac.fifo_position == fifo_counter) & (dac.fifo_type == type):
                        bitstream = generate_bitstream(dac.parameters, are_parameters_MS2LS=dac.are_parameters_MS2LS,
                                                       preappend=dac.preappend,
                                                       postappend=dac.postappend,
                                                       selected=self.modules[module_key].active, should_return=True)
                        for k in range(len(bitstream)):
                            if dac.are_parameters_MS2LS == True:
                                h = len(bitstream) - 1 - k
                            else:
                                h = k
                            bitstream_to_send.append(''.join(bitstream[h]['code'].combine_code(LSB_first=True)))
                        fifo_counter -= 1
                for config_flipflop in self.modules[module_key].configs_flipflop:
                    if (config_flipflop.fifo_position == fifo_counter) & (config_flipflop.fifo_type == type):
                        bitstream = ''
                        for param_idx in range(len(config_flipflop.parameters)):
                            if self.modules[module_key].active:
                                if config_flipflop.are_parameters_MS2LS == True:
                                    h = len(config_flipflop.parameters) - 1 - param_idx
                                else:
                                    h = param_idx
                                bitstream += str(config_flipflop.parameters[h]['par'])
                            else:
                                bitstream += '0'
                        bitstream_to_send.append(''.join(map(str, bitstream)))
                        fifo_counter -= 1

                if fifo_counter == -1:
                    finish = True
        bitstream_joined = ''.join(bitstream_to_send)

        print('Generated bitstream, sending it to fifo ' + type)
        return bitstream_joined
    def send_fifo(self, bitstream_joined,type='slow'):
        '''
        Function that creates the string to be sent to the microcontroller.
        Standard is that the first number in the array (first would be 'p' in 'pippo') represents the LSB in the stream.
        LSB is the first bit being sent to the FIFO
        #TODO probably one day we should invert everything to MSB:LSB
        :param type:
        :return:
        '''

        bitstream_words = []
        stream = bitstream_joined
        fifo_length_size_bits = 8
        current_bit = 0
        fifo_length = len(bitstream_joined)
        first_trash = fifo_length % 8
        counter = 0
        data, length_bin = self.read_from_stream(current_bit, current_bit + fifo_length_size_bits - first_trash, stream,
                                                 dtype=int)
        data = data << first_trash
        bitstream_words.append(data)
        if type == 'slow':
            self.uC.spi[0].send(data)
        elif type == 'fast':
            self.uC.spi[1].send(data)
        # print(data)
        # print('word #',counter,'sent:', str(current_bit)+':'+str(current_bit + fifo_length_size_bits - first_trash), 'data:', data)

        current_bit += fifo_length_size_bits - first_trash
        counter += 1

        while (current_bit < fifo_length):

            data, length_bin = self.read_from_stream(current_bit, current_bit + fifo_length_size_bits, stream,
                                                     dtype=int)
            current_bit += fifo_length_size_bits
            counter += 1
            bitstream_words.append(data)
            if type == 'slow':
                self.uC.spi[0].send(data)
            elif type == 'fast':
                self.uC.spi[1].send(data)
        return bitstream_words
    def check_fifo(self,bitstream,fifotype='slow'):
        type = [1 if fifotype == 'fast' else 0][0]
        self.uC.start_experiment()
        _ = self.uC.spi[type].data_from_chip_and_clear()
        _ = self.uC.spi[type].data_to_chip_and_clear()
        bitstream_words = self.send_fifo(type=fifotype, bitstream_joined=bitstream)
        time.sleep(0.1)
        self.uC.update_state()
        mosi = self.uC.spi[type].data_to_chip_and_clear()
        miso = self.uC.spi[type].data_from_chip_and_clear()
        if miso[0]!=mosi[0]:
            logging.warning('FIFO ' + fifotype + ' is not working properly')
            logging.warning('Sent N# '+str(len(mosi[0]))+' Received N# '+str(len(miso[0])))
            logging.warning('Sent '+str(mosi[0])+' Received ' + str(miso[0]))
        self.uC.stop_experiment()
    def program_fifo(self,bitstream,fifotype = '',check = True):
       if type == 'slow':
           self.send_to_pin('dac_power_down', 1, module_name='FIFO_DAC')
       elif type == 'fast':
           self.send_to_pin('fast_power_down', 1, module_name='FIFO_FAST')
       time.sleep(1)
       self.send_fifo(type = fifotype,bitstream_joined=bitstream)
       if check:
           self.check_fifo(bitstream,fifotype=fifotype)
       time.sleep(1)
       if type == 'slow':
           self.send_to_pin('dac_power_down', 0, module_name='FIFO_DAC')
       elif type == 'fast':
           self.send_to_pin('fast_power_down', 0, module_name='FIFO_FAST')

    def send_to_gpio(self,gpio,value,time=0):
        self.uC.pin[gpio].send(value,time=time)
    def send_to_pin(self, pin_name, content, module_name='',time=0):
        if (module_name != 'FIFO_DAC') & (module_name != 'FIFO_FAST') & (module_name != 'MUX'):
            module = self.modules[self.active_module]
        else:
            module = self.modules[module_name]
        pin_found = False
        for pin in module.pins:
            # print(pin.name)
            if pin.name == pin_name:
                pin_found = True

                if (pin.type == 'digital') & (pin.direction == 'to_chip'):
                    self.send_to_gpio(pin.gpio, content,time=time)
                    print('send', content, 'to pin', pin.name, '(', pin.gpio, ')')
                    # print('TO IMPLEMENT! sending ' + str(content) + ' to pad \'' + str(pin.name) + '\' from module: ' + self.active_module)
                else:
                    print('Pin \'' + str(
                        pin.name) + '\' is either analog or input, cannot send stuff, no operation was performed')
        if pin_found == False:
            print('Pin \'' + str(pin_name) + '\' not found, no operation was performed')
    def read_from_stream(self,begin, end, stream, dtype=None):
        import numpy as np
        end = np.min([len(stream), end])
        if dtype == int:
            to_return = stream[begin:end]
            if to_return == '':
                intize = 0
            else:
                intize = int(to_return, 2)
            return intize, len(to_return)
        else:
            return stream[begin:end]
    def send_spike_raw(self,pin,width,time=0):
        self.send_to_gpio(pin,1,time=time)
        self.send_to_gpio(pin,0,time=time+width)
    def send_spike(self,pin,width,time=0):
        self.send_to_pin(pin,1,time=time)
        self.send_to_pin(pin,0,time=time+width)
    def send_spiketrain(self, pins, times, width):
        gpios = [self.find_GPIO(pin_name=pin,module=self.active_module) for pin in pins]
        for gpio_idx,gpio in enumerate(gpios):
            self.send_spike_raw(gpio,width,time=times[gpio_idx])
    def read_gpios(self):
        gpios_list = []
        times_list = []
        for pin in self.modules[self.active_module].pins:
            if pin.type == 'digital':
                if pin.direction == 'from_chip':
                    value_list,time_list =  self.uC.pin[pin.gpio].data_from_chip_and_clear()
                    time_list = [time_list[i] for i in range(len(time_list)) if value_list[i]==1]
                    gpio_list = [pin.gpio]*len(time_list)
                    gpios_list.extend(gpio_list)
                    times_list.extend(time_list)
        return gpios_list,times_list
    def read_pins(self):
        gpios_list,times_list = self.read_gpios()
        pins_list = []
        for gpio in gpios_list:
            for pin in self.modules[self.active_module].pins:
                if pin.type == 'digital':
                    if pin.direction == 'from_chip':
                        if pin.gpio == gpio:
                            pins_list.append(pin.name)

        return pins_list,times_list


def generate_cognigr1():
    cognigr1 = cognigr1_interface('cognigr1')
    cognigr1.add_module(name='FIFO_DAC',hasfifo = False)
    cognigr1.modules['FIFO_DAC'].add_spi(clk=SPI0_3,mosi=SPI0_0,miso=SPI0_1)
    cognigr1.modules['FIFO_DAC'].add_pin(name='dac_power_down',type='digital',direction = 'to_chip',gpio = SPI0_2, initial_value = 1)

    cognigr1.add_module(name='FIFO_FAST',hasfifo = False)
    cognigr1.modules['FIFO_FAST'].add_spi(clk=SPI1_3,mosi=SPI1_0,miso=SPI1_1)
    cognigr1.modules['FIFO_FAST'].add_pin(name='fast_power_down',type='digital',direction = 'to_chip',gpio = SPI1_2, initial_value = 1)

    cognigr1.add_module(name='MUX',hasfifo = False)
    mux_modules = {'SYNORM':0,'TDE_mod':1,'TDE':2,'TDE_capped':1,'PLL':2,'POSFET':None,'ATIS':None,'Cap':None,'WTA':4,'BCall':3,'Neuron_Array':6,'Piezo':5}
    cognigr1.modules['MUX'].add_mux(name='MUX',sel0_n=MUX0,sel1_n=MUX1,sel2_n=MUX2,list_of_modules=mux_modules)

    cognigr1.add_module(name='SYNORM',hasfifo = True)
    cognigr1.modules['SYNORM'].add_dac(fifo_position=0, fifo_type='slow', parameters=SYNORM.parameters,
                                       are_parameters_MS2LS=SYNORM.are_parameters_MS2LS)
    cognigr1.modules['SYNORM'].add_pin(name='PRE1',type='digital',direction = 'to_chip',gpio = DIG_I0, initial_value = 0)
    cognigr1.modules['SYNORM'].add_pin(name='PRE2',type='digital',direction = 'to_chip',gpio = DIG_I1, initial_value = 0)
    cognigr1.modules['SYNORM'].add_pin(name='POST',type='digital',direction = 'to_chip',gpio = DIG_I2, initial_value = 0)
    cognigr1.modules['SYNORM'].add_pin(name='W1', type='digital', direction='from_chip', gpio=DIG_O0, initial_value=0)
    cognigr1.modules['SYNORM'].add_pin(name='W2', type='digital', direction='from_chip', gpio=DIG_O1, initial_value=0)

    cognigr1.add_module(name='TDE_mod',hasfifo = True)
    cognigr1.modules['TDE_mod'].add_dac(fifo_position=1, fifo_type='slow', parameters=TDEDPI.parameters,
                                        are_parameters_MS2LS=TDEDPI.are_parameters_MS2LS)
    cognigr1.modules['TDE_mod'].add_pin(name='TRG', type='digital', direction='to_chip', gpio=DIG_I0, initial_value=0)
    cognigr1.modules[('TDE_mod'
                      '')].add_pin(name='FAC', type='digital', direction='to_chip', gpio=DIG_I1, initial_value=0)

    cognigr1.add_module(name='TDE',hasfifo = True)
    cognigr1.modules['TDE'].add_dac(fifo_position=2, fifo_type='slow', parameters=oldTDE.parameters,
                                    are_parameters_MS2LS=oldTDE.are_parameters_MS2LS)
    cognigr1.modules['TDE'].add_pin(name='FAC', type='digital', direction='to_chip', gpio=DIG_I2, initial_value=0)
    cognigr1.modules['TDE'].add_pin(name='TRG', type='digital', direction='to_chip', gpio=DIG_I3, initial_value=0)

    cognigr1.add_module(name='TDE_capped',hasfifo = True)
    cognigr1.modules['TDE_capped'].add_dac(fifo_position=3, fifo_type='slow', parameters=TDECAPPED.parameters,
                                           are_parameters_MS2LS=TDECAPPED.are_parameters_MS2LS)
    cognigr1.modules['TDE_capped'].add_pin(name='FAC', type='digital', direction='to_chip', gpio=DIG_I0, initial_value=0)
    cognigr1.modules['TDE_capped'].add_pin(name='TRG', type='digital', direction='to_chip', gpio=DIG_I1, initial_value=0)

    cognigr1.add_module(name='PLL',hasfifo = True)
    cognigr1.modules['PLL'].add_dac(fifo_position=4, fifo_type='slow', parameters=PLL.parameters,
                                    are_parameters_MS2LS=PLL.are_parameters_MS2LS)
    cognigr1.modules['PLL'].add_pin(name='IN', type='digital', direction='to_chip', gpio=DIG_I2, initial_value=0)
    cognigr1.modules['PLL'].add_pin(name='FB', type='digital', direction='from_chip', gpio=DIG_O0, initial_value=0)
    cognigr1.modules['PLL'].add_pin(name='TDE', type='digital', direction='from_chip', gpio=DIG_O1, initial_value=0)

    cognigr1.add_module(name='POSFET', hasfifo=True)
    cognigr1.modules['POSFET'].add_dac(fifo_position=5, fifo_type='slow', parameters=Ella.parameters_POSFET,
                                       are_parameters_MS2LS=Ella.are_parameters_MS2LS)
    cognigr1.modules['POSFET'].add_config(fifo_position=0, fifo_type='fast', parameters=Ella.config_POSFET)
    cognigr1.add_module(name='ATIS', hasfifo=True)
    cognigr1.modules['ATIS'].add_dac(fifo_position=6, fifo_type='slow', parameters=Ella.parameters_ATIS,
                                     are_parameters_MS2LS=Ella.are_parameters_MS2LS)
    cognigr1.modules['ATIS'].add_config(fifo_position=1, fifo_type='fast', parameters=Ella.config_ATIS)
    cognigr1.add_module(name='Cap', hasfifo=True)
    cognigr1.modules['Cap'].add_dac(fifo_position=18, fifo_type='slow', parameters=Ella.parameters_capintensity,
                                    are_parameters_MS2LS=Ella.are_parameters_MS2LS)
    cognigr1.modules['Cap'].add_config(fifo_position=2, fifo_type='fast', parameters=Ella.config_capinsensity)
    cognigr1.add_module(name='WTA',hasfifo = True)
    cognigr1.modules['WTA'].add_dac(fifo_position=19, fifo_type='slow', parameters=WTA.parameters,
                                    are_parameters_MS2LS=WTA.are_parameters_MS2LS)
    cognigr1.modules['WTA'].add_config(fifo_position=20, fifo_type='slow', parameters=WTA.parameters_config0)
    cognigr1.modules['WTA'].add_config(fifo_position=3, fifo_type='fast', parameters=WTA.parameters_config1)
    cognigr1.modules['WTA'].add_config(fifo_position=4, fifo_type='fast', parameters=WTA.parameters_config2)
    cognigr1.modules['WTA'].add_config(fifo_position=5, fifo_type='fast', parameters=WTA.parameters_config3)
    cognigr1.modules['WTA'].add_config(fifo_position=6, fifo_type='fast', parameters=WTA.parameters_config4)
    cognigr1.modules['WTA'].add_pin(name='IN0', type='digital', direction='to_chip', gpio=DIG_I0, initial_value=0)
    cognigr1.modules['WTA'].add_pin(name='IN1', type='digital', direction='to_chip', gpio=DIG_I1, initial_value=0)
    cognigr1.modules['WTA'].add_pin(name='IN2', type='digital', direction='to_chip', gpio=DIG_I2, initial_value=0)
    cognigr1.modules['WTA'].add_pin(name='IN3', type='digital', direction='to_chip', gpio=DIG_I3, initial_value=0)

    cognigr1.add_module(name='BCall',hasfifo = True)
    cognigr1.modules['BCall'].add_dac(fifo_position=21, fifo_type = 'slow', parameters=BCall.parameters,
                                       are_parameters_MS2LS=BCall.are_parameters_MS2LS)
    cognigr1.modules['BCall'].add_pin(name='reset', type='digital', direction='to_chip', gpio=DIG_I0, initial_value=0)
    cognigr1.modules['BCall'].add_pin(name='neg', type='digital', direction='to_chip', gpio=DIG_I1, initial_value=0)
    cognigr1.modules['BCall'].add_pin(name='post_inp', type='digital', direction='to_chip', gpio=DIG_I2, initial_value=0)
    cognigr1.modules['BCall'].add_pin(name='pre_inp', type='digital', direction='to_chip', gpio=DIG_I3, initial_value=0)

    cognigr1.add_module(name='Neuron_Array',hasfifo = True)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=7, fifo_type='slow',
                                                parameters=Neuron_Array.parameters_config_A,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=8, fifo_type='slow',
                                                parameters=Neuron_Array.parameters_config_B,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)

    cognigr1.modules['Neuron_Array'].add_dac(fifo_position=9, fifo_type='slow', parameters=Neuron_Array.parameters_C,
                                             are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_dac(fifo_position=10, fifo_type='slow', parameters=Neuron_Array.parameters_D,
                                             are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_dac(fifo_position=11, fifo_type='slow', parameters=Neuron_Array.parameters_E,
                                             are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_dac(fifo_position=12, fifo_type='slow', parameters=Neuron_Array.parameters_F,
                                             are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=13, fifo_type='slow',
                                                parameters=Neuron_Array.parameters_config_G,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=14, fifo_type='slow',
                                                parameters=Neuron_Array.parameters_config_H,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_dac(fifo_position=15, fifo_type='slow', parameters=Neuron_Array.parameters_I,
                                             are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_dac(fifo_position=16, fifo_type='slow', parameters=Neuron_Array.parameters_J,
                                             are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=17, fifo_type='slow',
                                                parameters=Neuron_Array.parameters_config_K,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=22, fifo_type='slow',
                                                parameters=Neuron_Array.parameters_config_L,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=7, fifo_type='fast',
                                                parameters=Neuron_Array.parameters_config_0,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=8, fifo_type='fast',
                                                parameters=Neuron_Array.parameters_config_1,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=9, fifo_type='fast',
                                                parameters=Neuron_Array.parameters_config_2,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=10, fifo_type='fast',
                                                parameters=Neuron_Array.parameters_config_3,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=11, fifo_type='fast',
                                                parameters=Neuron_Array.parameters_config_4,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_config(fifo_position=12, fifo_type='fast',
                                                parameters=Neuron_Array.parameters_config_5,
                                                are_parameters_MS2LS=Neuron_Array.are_parameters_MS2LS)
    cognigr1.modules['Neuron_Array'].add_aer(type='to_chip',req=DIG_I15, ack=DIG_I4, bus_size=10, data_pins=[DIG_I5,DIG_I6,DIG_I7,DIG_I8,DIG_I9,DIG_I10,DIG_I11,DIG_I12,DIG_I13,DIG_I14], mode='4Phase_Chigh_Dhigh', req_delay=0, time=0)
    cognigr1.modules['Neuron_Array'].add_aer(type='from_chip',req=DIG_O2, ack=DIG_O7, bus_size=4, data_pins=[DIG_O3,DIG_O4,DIG_O5,DIG_O6], mode='4Phase_Chigh_Dhigh', req_delay=0, time=0)
    cognigr1.modules['Neuron_Array'].add_pin(name='sr_reset', type='digital', direction='to_chip', gpio=DIG_I16, initial_value=0)
    cognigr1.modules['Neuron_Array'].add_pin(name='pr_reset', type='digital', direction='to_chip', gpio=DIG_I17, initial_value=0)

    cognigr1.add_module(name='Piezo',hasfifo = True)
    cognigr1.modules['Piezo'].add_dac(fifo_position=23, fifo_type='slow', parameters=Piezo.parameters,
                                      are_parameters_MS2LS=Piezo.are_parameters_MS2LS)
    cognigr1.modules['Piezo'].add_config(fifo_position=13, fifo_type='fast',
                                         parameters=Piezo.parameters_config_0)

    return cognigr1
# class texel_interface:
#     """
#     This class is the interface between the texel API and the uC-chip-interface-teensy41
#     """
#     def __init__(self,serial_port,parameters,flags):
#         if serial_port == 'auto':
#             serial_port = self.find_serial_port()
#             logging.info('Serial port:',serial_port)
#         self.uC = uC_api(serial_port,2)
#         ## Creating registers
#
#         self.last_time_read = 0
#         self.last_time_sent = 0
#     def find_serial_port(self):
#         ports = serial.tools.list_ports.comports(include_links=False)
#         for port in ports:
#             return port.device
#     def setup(self):
#         '''
#         This function sets up the ports on Teensy according to the PCB layout (October 2023)
#         '''
#         ### AER TO CHIP: Used to send packages to the chip, it's just wired from GPIOs to the chip
#         self.uC.async_to_chip[0].activate(
#             req_pin = 4,
#             ack_pin = 5,
#             data_width = 32,
#             data_pins = [0,1,14,15,16,17,20,21,22,23,24,25,26,27,6,7,8,9,10,11,12,13,32,28,30,31,34,35,36,37,38,39],
#             mode="4Phase_Chigh_Dhigh",
#             req_delay = 0,
#             time = 0)
#         ### AER FROM CHIP: Used to receive packages from the chip, the communication is done through I2C using two port extenders
#         self.uC.async_from_chip[0].activate(
#             req_pin=2,
#             ack_pin=3,
#             data_width=32,
#             data_pins=[0 for i in range(32)], #useless, just for compatibility
#             mode="4Phase_MCP23017",
#             req_delay=0,
#             time=0)
#         self.uC.pin[PIN_RESET_GLOBAL].activate()
#         self.uC.pin[PIN_RESET_REGISTER].activate()
#         self.uC.pin[PIN_RESET_SYNAPSES].activate()
#     def reset(self, which=None):
#         '''
#         This function resets the ports on Teensy according to the PCB layout (October 2023)
#         Pins are active low
#         '''
#         if which is None:
#             which = ['global', 'register', 'synapses']
#         if 'global' in which:
#             self.uC.pin[PIN_RESET_GLOBAL].send(0)
#             time.sleep(0.1)
#             self.uC.pin[PIN_RESET_GLOBAL].send(1)
#
#         if 'register' in which:
#             self.uC.pin[PIN_RESET_REGISTER].send(0)
#             time.sleep(0.1)
#             self.uC.pin[PIN_RESET_REGISTER].send(1)
#         if 'synapses' in which:
#             self.uC.pin[PIN_RESET_SYNAPSES].send(0)
#             time.sleep(0.1)
#             self.uC.pin[PIN_RESET_SYNAPSES].send(1)
#     def start_experiment(self):
#         self.uC.start_experiment()
#         logging.info('Start Experiment')
#
#     def parse_packet(self,packet):
#         '''
#         This function parses the packet received from the chip
#         '''
#         packet = str(bin(packet)[2:].zfill(32))
#         logging.debug(packet)
#         core = int(packet[0])
#         type = 'register' if packet[1] == '1' else 'spike'
#         if type == 'register':
#             word = int(packet[3:-6],2)
#             address = int(packet[-6:],2)
#             packet = bd(core=core, spike_reg='reg', read_write='read', address=address, word=word)
#         else:
#             address_y = int(packet[-7:-4],2)
#             address_x = int(packet[-4:],2)
#             neuron = address_y*self.neuron_cols+address_x
#             packet = bd(core=core, spike_reg='spike', read_write='read', neuron=neuron)
#         return packet
#     def read_sent_event(self,raw = False):
#         '''
#         This function reads the events to the chip, then convert them into bundle data objects
#         The raw parameter is used to return the raw data from the chip (useful for checking consistency)
#         '''
#         raw_pkgs,times = self.uC.async_to_chip[0].data_to_chip_and_clear()
#         read_pkgs = []
#         for idx,raw_pkg in enumerate(raw_pkgs):
#             if raw:
#                 read_pkgs.append((raw_pkg,times[idx]))
#             else:
#                 read_pkgs.append((self.parse_packet(raw_pkg),times[idx]))
#         return read_pkgs
#     def read_event(self,raw = False):
#         '''
#         This function reads the events from the chip, then convert them into bundle data objects
#         The raw parameter is used to return the raw data from the chip (useful for checking consistency)
#         '''
#         raw_pkgs,times = self.uC.async_from_chip[0].data_from_chip_and_clear()
#         read_pkgs = []
#         for idx,raw_pkg in enumerate(raw_pkgs):
#             if raw:
#                 read_pkgs.append((raw_pkg,times[idx]))
#             else:
#                 read_pkgs.append((self.parse_packet(raw_pkg),times[idx]))
#         if len(times) != 0:
#             self.last_time_read = times[-1]
#         return read_pkgs
#     def get_active_neurons(self):
#         read_pkgs = self.read_event()
#         neurons = []
#         for read_pkg in read_pkgs:
#             if (read_pkg[0].spike_reg == 'spike'):
#                 neurons.append(read_pkg[0].neuron+90*read_pkg[0].core)
#         return list(set(neurons))
#     def report_neural_activity(self):
#         read_pkgs = self.read_event()
#         neurons = []
#         times = []
#         for read_pkg in read_pkgs:
#             if (read_pkg[0].spike_reg == 'spike'):
#                 neurons.append(read_pkg[0].neuron+90*read_pkg[0].core)
#                 times.append(read_pkg[1])
#         return times,neurons
#
#     def print_sent_event(self):
#         '''
#         This function prints the events to the chip, then convert them into bundle data objects
#         '''
#         read_pkgs = self.read_sent_event()
#         for read_pkg in read_pkgs:
#             print('Time:',read_pkg[1],'Pck:',str(read_pkg[0]))
#     def print_event(self,all=False):
#         '''
#         This function prints the events from the chip, then convert them into bundle data objects
#         '''
#         read_pkgs = self.read_event()
#         for read_pkg in read_pkgs:
#             if (int(read_pkg[1]) > int(self.last_time_read)) or all:
#                 print('Time (us)    :',read_pkg[1],'Pck:',str(read_pkg[0]))
#
#
#     ### SPIKE GENERATION
#     def send_spike(self,core,neuron_idx,synapse_idx,time=0):
#         '''
#         This function writes a spike to the synapse of a neuron in one of the core
#         The correspondanding synapse address is calculated knowing how many synapses a neuron has and how many neurons are there
#         he time parameter is used to send the command to the chip at a specific time
#         '''
#         neuron_row = int(neuron_idx//self.neuron_cols)
#         neuron_col = int(neuron_idx%self.neuron_cols)
#         synapse_y = synapse_idx+(neuron_row*58)
#         synapse_x = neuron_col
#         logging.debug('y',synapse_y,'x',synapse_x)
#         spk = bd(core=core, spike_reg='spike', read_write='write',synapse=[synapse_x, synapse_y])
#         spk.gen_bd_in()
#         aer_command = spk.bd_in
#         self.uC.async_to_chip[0].send(word=int(aer_command,2),time=time)
#     def send_spike_raw(self,synapse_x,synapse_y,core=0,time=0):
#         '''
#         This function writes a spike in the synapse matrix (synapse_x,synapse_y) of the core
#         The addressing of the synapses is raw, meaning that the correspondence to the neuron is not calculated
#         The time parameter is used to send the command to the chip at a specific time
#         '''
#         spk = bd(core=core, spike_reg='spike', synapse=[synapse_x, synapse_y])
#         aer_command = spk.gen_bd_out()
#         self.uC.async_to_chip[0].send(word=int(aer_command,2),time=time)
#     def send_spike_train(self,core,neuron_idx,synapse_idx, freq=0, repetition=1):
#         time_to_wait = int(1e6 / freq) #
#         for rep in range(repetition):
#             self.send_spike(neuron_idx=neuron_idx, synapse_idx=synapse_idx, core=core, time=time_to_wait*rep)
#
