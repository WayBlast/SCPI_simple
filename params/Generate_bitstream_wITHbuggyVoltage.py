import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

get_bin = lambda x, n: format(x, 'b').zfill(n)
# Current_PATH = os.getcwd()
# FILE_PATH = os.path.dirname(os.getcwd())
# DATA_PATH = os.path.join(FILE_PATH, 'Data')
file_current = 'parametergen_current_levels.csv'
data_pressure = pd.read_csv(file_current, sep=',')


def generate_bitstream(parameters, are_parameters_MS2LS=False, preappend=None, postappend=None):
    final_concatenated = ''
    final_concatenated_collection = []
    for k in range(len(parameters)):
        if are_parameters_MS2LS == True:
            h = len(parameters) - 1 - k
        else:
            h = k
        par = parameters[h]['par']
        type = parameters[h]['type']
        # type = 'ptype'
        state = 'incomplete'
        # print(h)
        if type =='voltage':
            if par <= 0.9:
                type = 'ntype'
            else:
                type = 'ptype'
            for i in range(6):
                if (par < data_pressure[data_pressure.columns[i + 13 + int(type == 'ptype') * 6]][0]) & (
                        state != 'completed'):
                    for j in range(255):
                        if (par > data_pressure[data_pressure.columns[i + 13 + int(type == 'ptype') * 6]][j]) & (
                                state != 'completed'):
                            code = get_bin(int(data_pressure[data_pressure.columns[0]][j]), 8)
                            print('Wanted: ' + str(par) + '. Real: ' + str(
                                data_pressure[data_pressure.columns[i + 13 + int(type == 'ptype') * 6]][
                                    j]) + '. Error = ' + str(round(100 * (
                                    par - data_pressure[data_pressure.columns[i + 13 + int(type == 'ptype') * 6]][
                                j]) / par, 2)) + '%')
                            state = 'completed'
                            code_with_details = get_bin(i, 3) + str(code) + str(int(type == 'ntype'))

            if state == 'incomplete':
                print('Wanted: ' + str(par) + ' Didn\'t find any good values for this. I am taking ' + str(
                    data_pressure[data_pressure.columns[5 + 13 + int(type == 'ptype') * 5]][0]))
                code_with_details = get_bin(5, 3) + str(255) + str(int(type == 'ntype'))


        elif type != 'Off':
            for i in range(6):
                if (par < data_pressure[data_pressure.columns[i + 1 + int(type == 'ptype') * 6]][0]) & (
                        state != 'completed'):
                    for j in range(255):
                        if (par > data_pressure[data_pressure.columns[i + 1 + int(type == 'ptype') * 6]][j]) & (
                                state != 'completed'):
                            code = get_bin(int(data_pressure[data_pressure.columns[0]][j]), 8)
                            print('Wanted: ' + str(par) + '. Real: ' + str(
                                data_pressure[data_pressure.columns[i + 1 + int(type == 'ptype') * 6]][
                                    j]) + '. Error = ' + str(round(100 * (
                                    par - data_pressure[data_pressure.columns[i + 1 + int(type == 'ptype') * 6]][
                                j]) / par, 2)) + '%')
                            state = 'completed'
                            code_with_details = get_bin(i, 3) + str(code) + str(int(type == 'ntype'))

            if state == 'incomplete':
                print('Wanted: ' + str(par) + ' Didn\'t find any good values for this. I am taking ' + str(
                    data_pressure[data_pressure.columns[5 + 1 + int(type == 'ptype') * 5]][0]))
                code_with_details= get_bin(5, 3) + str(255) + str(int(type == 'ntype'))
        else:
            code = get_bin(0, 8)
            prefix = get_bin(0,3)
            suffix = 0
            code_with_details = str(prefix) + str(code) + str(suffix)
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
    if preappend != None:
        final_concatenated = preappend + final_concatenated
    if postappend != None:
        final_concatenated = final_concatenated + postappend
    # flipped_final_concatenated = final_concatenated[::-1]

    print('Strings to copy-paste...')
    print('bitpattern:')
    print(str(len(final_concatenated)) + '\'b' + str(final_concatenated))
    print('number of bits:')
    print(str(len(final_concatenated)))

def generate_labels(parameters,are_parameters_MS2LS = False):
    label_gen = ''
    reststate_gen = ''
    reststates = ['gnd!', 'vdd!']
    oblivion_count = -1
    for i in range(len(parameters)):
        oblivion_count += int(parameters[i]['type'] == 'Off')

    for h in range(len(parameters)-1):
        if are_parameters_MS2LS == False:
            i = len(parameters) - 1 - h
        else:
            i = h
        if parameters[i]['type'] == 'ntype':
            label_gen = label_gen + parameters[i]['name']
            try:
                if parameters[i]['reset']:
                    reststate_gen = reststate_gen + reststates[1]
                else:
                    reststate_gen = reststate_gen + reststates[0]
            except KeyError:
                reststate_gen = reststate_gen + reststates[0]
        elif parameters[i]['type'] == 'ptype':
            label_gen = label_gen + parameters[i]['name']
            try:
                if parameters[i]['reset']:
                    reststate_gen = reststate_gen + reststates[0]
                else:
                    reststate_gen = reststate_gen + reststates[1]
            except KeyError:
                reststate_gen = reststate_gen + reststates[1]
        elif parameters[i]['type'] == 'Off':
            label_gen = label_gen + 'oblivion<' + str(oblivion_count) + '>'
            reststate_gen = reststate_gen + reststates[0]
            oblivion_count -= 1
        else:
            print('An error occured')
            raise ValueError
        if h < len(parameters)-2:
            label_gen = label_gen + ','
            reststate_gen = reststate_gen + ','
    print('Label Generated:')
    print(label_gen)
    print(reststate_gen)