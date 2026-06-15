# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import os
# get_bin = lambda x, n: format(x, 'b').zfill(n)
# Current_PATH = os.getcwd()
# FILE_PATH = os.path.dirname(os.getcwd())
# DATA_PATH = os.path.join(FILE_PATH, 'Data')
# file_current = 'parametergen_current_levels.csv'
# data_pressure = pd.read_csv(os.path.join(DATA_PATH, file_current), sep=',')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
get_bin = lambda x, n: format(x, 'b').zfill(n)
# Current_PATH = os.getcwd()
# FILE_PATH = os.path.dirname(os.getcwd())
# DATA_PATH = os.path.join(FILE_PATH, '/Data')
file_current = 'parametergen_current_levels.csv'
# file_parameters = 'TDE_mod_module_tb_param.csv'
data_pressure = pd.read_csv(file_current, sep=',')
# data_param = pd.read_csv(os.path.join(DATA_PATH, file_parameters), sep=',')


parameters = [
    {'par': 700e-9, 'type': 'ntype'}, # Buffer drive strength param
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 100e-12, 'type': 'Off'}, #Unused Channels
    {'par': 500e-9, 'type': 'ntype'}, #bias_NI
    {'par': 50e-12 , 'type': 'ptype'},  # Vref
    {'par': 50e-12 , 'type': 'ptype'},  # VgcOn
    {'par': 50e-12 , 'type': 'ntype'},  # VgOff
    {'par': 1.45e-9, 'type': 'ntype'},  # Vdoff
    {'par': 500e-12, 'type': 'ntype'},  # Vdon
    {'par': 800e-12, 'type': 'ntype'},  # Vdiff
    {'par': 500e-12, 'type': 'ptype'},  # pVsf
    {'par': 50e-12, 'type': 'ntype'},  # vbn
    # {'par': 50e-12 / 0.38, 'type': 'ptype'},    # Vref
    # {'par': 50e-12 / 0.22, 'type': 'ptype'},    #VgcOn
    # {'par': 50e-12 / 0.66, 'type': 'ntype'},    # VgOff
    # {'par': 1.45e-9 / 0.66, 'type': 'ntype'},   # Vdoff
    # {'par': 500e-12 / 0.66, 'type': 'ntype'},   # Vdon
    # {'par': 800e-12 / 0.66, 'type': 'ntype'},   # Vdiff
    # {'par': 500e-12 / 0.38, 'type': 'ptype'},   # pVsf
    # {'par': 50e-12/0.98, 'type': 'ntype'},      # vbn
]
final_concatenated = ''
final_concatenated_collection = []
for h in range(31):
    par = parameters[h]['par']
    type = parameters[h]['type']
    # type = 'ptype'
    state = 'incomplete'
    # print(h)
    if type != 'Off':
        for i in range(6):
            if (par < data_pressure[data_pressure.columns[i+1+ int(type=='ntype')*6] ][0]) & (state != 'completed'):
                for j in range(255):
                    if (par > data_pressure[data_pressure.columns[i+1+ int(type=='ntype')*6]][j]) & (state != 'completed'):
                        code = get_bin(int(data_pressure[data_pressure.columns[0]][j]),8)
                        print('Wanted: ' + str(par) + '. Real: ' + str(
                            data_pressure[data_pressure.columns[i + 1 + int(type == 'ntype') * 6]][
                                j]) + '. Error = ' + str(round(100*(par - data_pressure[data_pressure.columns[i+1+ int(type=='ptype')*5]][j]) / par,2)) + '%')
                        state = 'completed'
                        code_with_details = get_bin(i, 3) + str(code) + str(int(type == 'ntype'))
                        print(i)
                        print(j)
        if state == 'incomplete':
            print('Wanted: ' + str(par) + ' Didn\'t find any good values for this. I am taking ' + str(data_pressure[data_pressure.columns[5+1+ int(type=='ptype')*5] ][0]))
    else:
        code_with_details = '000111111110'
        i = 0
        # code = code[::-1]

    final_concatenated = code_with_details + final_concatenated
    final_concatenated_collection.append(code_with_details)
        # print(i)
# print(j)
# plt.plot(data_pressure[data_pressure.columns[0]][j],data_pressure[data_pressure.columns[i+1+ int(type=='ptype')*5] ][j],'.')
# plt.plot(data_pressure[data_pressure.columns[0]],data_pressure[data_pressure.columns[i+1+ int(type=='ptype')*5-1]], label = 'low')
# plt.plot(data_pressure[data_pressure.columns[0]],data_pressure[data_pressure.columns[i+1+ int(type=='ptype')*5]], label = 'right')
# plt.plot(data_pressure[data_pressure.columns[0]][j],par1,'.')

# plt.legend()
# print(final_concatenated)
flipped_final_concatenated = final_concatenated[::-1]
flipped_final_concatenated = final_concatenated[::-1]+'100000000001'
clock_code = ''
for i in range(len(flipped_final_concatenated)):
    clock_code = clock_code + '0110'
print(flipped_final_concatenated)
print(len(flipped_final_concatenated))
# print(clock_code)





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
