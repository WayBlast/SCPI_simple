from Generate_bitstream import *
are_parameters_MS2LS = False

# postappend = None
#
#
parameters_POSFET = [
    {'par': 700e-9, 'type': 'ntype','name': 'buffer'}, # Buffer drive strength param
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #Unused Channels
    {'par': 500e-9, 'type': 'ntype', 'name': 'bias_NI'},
    {'par': 50e-12, 'type': 'ntype', 'name': 'vbn'},    
    {'par': 1.45e-9, 'type': 'ntype', 'name': 'Vdoff'},
    {'par': 800e-12, 'type': 'ntype', 'name': 'Vdiff'},
    {'par': 50e-12 , 'type': 'ntype', 'name': 'VgOff'},
    {'par': 500e-12, 'type': 'ntype', 'name': 'Vdon'},
    {'par': 50e-12 , 'type': 'ptype', 'name': 'Vref'},
    {'par': 50e-12 , 'type': 'ptype', 'name': 'VgcOn'},
    {'par': 500e-12, 'type': 'ptype', 'name': 'pVsf'},
    # {'par': 50e-12 / 0.38, 'type': 'ptype'},    # Vref
    # {'par': 50e-12 / 0.22, 'type': 'ptype'},    #VgcOn
    # {'par': 50e-12 / 0.66, 'type': 'ntype'},    # VgOff
    # {'par': 1.45e-9 / 0.66, 'type': 'ntype'},   # Vdoff
    # {'par': 500e-12 / 0.66, 'type': 'ntype'},   # Vdon
    # {'par': 800e-12 / 0.66, 'type': 'ntype'},   # Vdiff
    # {'par': 500e-12 / 0.38, 'type': 'ptype'},   # pVsf
    # {'par': 50e-12/0.98, 'type': 'ntype'},      # vbn
]

config_POSFET = [
        {'par': 1, 'name': 'conf0'},  # conf0
        {'par': 0, 'name': 'conf1'},  # conf1
        {'par': 0, 'name': 'conf2'},  # conf2
        {'par': 0, 'name': 'conf3'},  # conf3
        {'par': 0, 'name': 'conf4'},  # conf4
        {'par': 0, 'name': 'conf5'},  # conf5
        {'par': 0, 'name': 'conf6'},  # conf6
        {'par': 0, 'name': 'conf7'},  # conf7
        {'par': 0, 'name': 'conf8'},  # conf8
        {'par': 0, 'name': 'conf9'},  # conf9
        {'par': 0, 'name': 'conf10'},  # conf10
        {'par': 1, 'name': 'conf11'},  # conf11
]
    #config_POSFET =  '100000000001'
# preappend = '100000000001'
# generate_bitstream(parameters, are_parameters_MS2LS=are_parameters_MS2LS, preappend=preappend, postappend=postappend)
# generate_labels(parameters, are_parameters_MS2LS=are_parameters_MS2LS)

######  ATIS #####

# are_parameters_MS2LS = False
# preappend = '100000000000'
# postappend = None
# config_ATIS = '100000000001'
config_ATIS = [
        {'par': 1, 'name': 'conf0'},  # conf0
        {'par': 0, 'name': 'conf1'},  # conf1
        {'par': 0, 'name': 'conf2'},  # conf2
        {'par': 0, 'name': 'conf3'},  # conf3
        {'par': 0, 'name': 'conf4'},  # conf4
        {'par': 0, 'name': 'conf5'},  # conf5
        {'par': 0, 'name': 'conf6'},  # conf6
        {'par': 0, 'name': 'conf7'},  # conf7
        {'par': 0, 'name': 'conf8'},  # conf8
        {'par': 0, 'name': 'conf9'},  # conf9
        {'par': 0, 'name': 'conf10'},  # conf10
        {'par': 1, 'name': 'conf11'},  # conf11
]
parameters_ATIS = [
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #MSB <29>
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    # {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 800e-12/ 0.66, 'type': 'ntype', 'name': 'nbiasLeak'},
    {'par': 100e-9/ 0.66, 'type': 'ntype', 'name': 'Bias_NI'},
    {'par': 0.5, 'type': 'voltage', 'name': 'Vlow'}, #LSB
    {'par': 1.5, 'type': 'voltage', 'name': 'Vhigh'},
]
# generate_bitstream(parameters, are_parameters_MS2LS=are_parameters_MS2LS, preappend=preappend, postappend=postappend)
# generate_labels(parameters, are_parameters_MS2LS=are_parameters_MS2LS)


######  Cap-Intensity #####

are_parameters_MS2LS = False
# preappend = '100000000000'
# postappend = None
config_capinsensity = '100000000000'
config_capinsensity = [
        {'par': 0, 'name': 'conf0'},  # conf0
        {'par': 0, 'name': 'conf1'},  # conf1
        {'par': 0, 'name': 'conf2'},  # conf2
        {'par': 0, 'name': 'conf3'},  # conf3
        {'par': 0, 'name': 'conf4'},  # conf4
        {'par': 0, 'name': 'conf5'},  # conf5
        {'par': 0, 'name': 'conf6'},  # conf6
        {'par': 0, 'name': 'conf7'},  # conf7
        {'par': 0, 'name': 'conf8'},  # conf8
        {'par': 1, 'name': 'conf9'},  # Transmission gate for Offset (1 for low and 0 for high)
        {'par': 1, 'name': 'conf10'},  # Gate/Diff<1>
        {'par': 0, 'name': 'conf11'},  # Gate/Diff<0>
]
parameters_capintensity = [
    {'par': 700e-9, 'type': 'ntype', 'name': 'Buffer'}, #MSB <29>
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-9, 'type': 'ntype', 'name': 'ref_NI'},
    {'par': 3.0e-12, 'type': 'ntype', 'name': 'leak_NI'}, #LSB
    {'par': 1e-12, 'type': 'ptype', 'name': 'rest_PI'},
    {'par': 1e-9, 'type': 'ntype', 'name': 'thr_NI'},	
    {'par': 0.7, 'type': 'voltage', 'name': 'OffsetL'},
    {'par': 1.0, 'type': 'Off', 'name': 'OffsetH'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'Vdiff'},
]
# generate_bitstream(parameters, are_parameters_MS2LS=are_parameters_MS2LS, preappend=preappend, postappend=postappend)
# generate_labels(parameters, are_parameters_MS2LS=are_parameters_MS2LS)


# 100001010101011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000011111111000110011100101001001101000001001101000100000011000100101010010101110111100110110100010000000111100100000011000100000000001




# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import os
# get_bin = lambda x, n: format(x, 'b').zfill(n)
# # Current_PATH = os.getcwd()
# # FILE_PATH = os.path.dirname(os.getcwd())
# # DATA_PATH = os.path.join(FILE_PATH, '/Data')
# file_current = 'parametergen_current_levels.csv'
# # file_parameters = 'TDE_mod_module_tb_param.csv'
# data_pressure = pd.read_csv(file_current, sep=',')
# # data_param = pd.read_csv(os.path.join(DATA_PATH, file_parameters), sep=',')
#
#
# parameters = [
#     {'par': 200e-9, 'type': 'ntype'}, # Buffer drive strength param
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'}, #Unused Channels
#     {'par': 100e-12, 'type': 'Off'},
#     {'par': 500e-9, 'type': 'ntype'},
#     {'par': 50e-12 / 0.38, 'type': 'ptype'},
#     {'par': 50e-12 / 0.22, 'type': 'ptype'},
#     {'par': 50e-12 / 0.66, 'type': 'ntype'},
#     {'par': 1.45e-9 / 0.66, 'type': 'ntype'},
#     {'par': 500e-12 / 0.66, 'type': 'ntype'},
#     {'par': 800e-12 / 0.66, 'type': 'ntype'},
#     {'par': 500e-12 / 0.38, 'type': 'ptype'},
#     {'par': 50e-12/0.98, 'type': 'ntype'},
# ]
#
# final_concatenated = ''
# for h in range(31):
#     par = parameters[h]['par']
#     type = parameters[h]['type']
#     # type = 'ptype'
#     state = 'incomplete'
#     # print(h)
#     if type != 'Off':
#         for i in range(6):
#             if (par < data_pressure[data_pressure.columns[i+1+ int(type=='ptype')*5] ][0]) & (state != 'completed'):
#                 for j in range(255):
#                     if (par > data_pressure[data_pressure.columns[i+1+ int(type=='ptype')*5]][j]) & (state != 'completed'):
#                         code = get_bin(int(data_pressure[data_pressure.columns[0]][j]),8)
#                         print('Wanted: ' + str(par) + '. Real: ' + str(
#                             data_pressure[data_pressure.columns[i + 1 + int(type == 'ptype') * 5]][
#                                 j]) + '. Error = ' + str(100*(par - data_pressure[data_pressure.columns[i+1+ int(type=='ptype')*5]][j]) / par))
#                         state = 'completed'
#         if state == 'incomplete':
#             print('Wanted: ' + str(par) + ' Didn\'t find any good values for this. I am taking ' + str(data_pressure[data_pressure.columns[5+1+ int(type=='ptype')*5] ][0]))
#     else:
#         code = '11111111'
#         i = 0
#         # code = code[::-1]
#     code_with_details = get_bin(i, 3) + str(code) + str(int(type == 'ptype'))
#     final_concatenated = code_with_details + final_concatenated
#         # print(i)
# # print(j)
# # plt.plot(data_pressure[data_pressure.columns[0]][j],data_pressure[data_pressure.columns[i+1+ int(type=='ptype')*5] ][j],'.')
# # plt.plot(data_pressure[data_pressure.columns[0]],data_pressure[data_pressure.columns[i+1+ int(type=='ptype')*5-1]], label = 'low')
# # plt.plot(data_pressure[data_pressure.columns[0]],data_pressure[data_pressure.columns[i+1+ int(type=='ptype')*5]], label = 'right')
# # plt.plot(data_pressure[data_pressure.columns[0]][j],par1,'.')
#
# # plt.legend()
# # print(final_concatenated)
# flipped_final_concatenated = final_concatenated[::-1]+'100000000001'
# print(len(flipped_final_concatenated))
# print(flipped_final_concatenated)
#
