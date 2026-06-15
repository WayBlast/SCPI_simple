# import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
# import os

get_bin = lambda x, n: format(x, 'b').zfill(n)
# Current_PATH = os.getcwd()
# FILE_PATH = os.path.dirname(os.getcwd())
# DATA_PATH = os.path.join(FILE_PATH, 'Data')
file_current = 'helper/parametergen_current_levels.csv'
data_pressure = pd.read_csv(file_current, sep=',')


def generate_bitstream(parameters, are_parameters_MS2LS=False, preappend=None, postappend=None, channelsnumber = 31, selected = False, should_return = False, printout = False):
    final_concatenated = ''
    final_concatenated_collection = []
    try:
        assert (len(parameters) == channelsnumber), "The number of channels is not " + str(channelsnumber) + ". If it's correct then put the variable channelsnumber to the expected number of channels"
    except AssertionError:
        print('ciao')
        raise AssertionError
    for k in range(len(parameters)):
        if are_parameters_MS2LS == True:
            h = len(parameters) - 1 - k
        else:
            h = k
        par = parameters[h]['par']
        type = parameters[h]['type']
        name = parameters[h]['name']
        # type = 'ptype'
        state = 'incomplete'
        volt = 0
        # print(h)
        if type =='voltage':
            volt = 1
            if par <= 0.9:
                type = 'ntype'
            else:
                type = 'ptype'

        if type != 'Off':
            for i in range(6):
                if volt and int(type == 'ptype'):
                    if (par > data_pressure[data_pressure.columns[i + 1 + volt * 12 + int(type == 'ptype') * 6]][0]) & (
                            state != 'completed'):
                        for j in range(256):
                            if (par <
                                data_pressure[data_pressure.columns[i + 1 + volt * 12 + int(type == 'ptype') * 6]][
                                    j]) & (
                                    state != 'completed'):
                                code = get_bin(int(data_pressure[data_pressure.columns[0]][j]), 8)
                                if printout == True:
                                    print('Wanted: ' + str(par) + '. Real: ' + str(
                                        data_pressure[data_pressure.columns[i + 1 + volt * 12 + int(type == 'ptype') * 6]][
                                            j]) + '. Error = ' + str(round(100 * (
                                            par - data_pressure[
                                        data_pressure.columns[i + 1 + volt * 12 + int(type == 'ptype') * 6]][
                                        j]) / par, 2)) + '%')
                                state = 'completed'
                                code_with_details = get_bin(i, 3) + str(code) + str(int(type == 'ntype'))
                elif (par < data_pressure[data_pressure.columns[i + 1 + volt * 12 + int(type == 'ptype') * 6]][0]) & (
                        state != 'completed'):
                    for j in range(256):

                        if (par > data_pressure[data_pressure.columns[i + 1 + volt * 12 + int(type == 'ptype') * 6]][j]) & (
                                state != 'completed'):
                            code = get_bin(int(data_pressure[data_pressure.columns[0]][j]), 8)
                            if printout == True:
                                print(name + ' | Wanted: ' + str(par) + '. Real: ' + str(
                                    data_pressure[data_pressure.columns[i + 1 + volt * 12 + int(type == 'ptype') * 6]][
                                        j]) + '. Error = ' + str(round(100 * (
                                        par - data_pressure[data_pressure.columns[i + 1 + volt * 12 + int(type == 'ptype') * 6]][
                                    j]) / par, 2)) + '% Code is: ' + get_bin(i, 3) + "|" + str(code)+ "|" + str(int(type == 'ntype')))
                            state = 'completed'
                            code_with_details = get_bin(i, 3) + str(code) + str(int(type == 'ntype'))

            if state == 'incomplete':
                if printout == True:
                    print('Wanted: ' + str(par) + ' Didn\'t find any good values for this. I am taking ' + str(
                        data_pressure[data_pressure.columns[5 + 1 + volt * 12 +  int(type == 'ptype') * 6]][0]))
                if volt and int(type == 'ptype'):
                    code_with_details = get_bin(0, 3) + get_bin(0, 8) + str(int(type == 'ntype'))
                else:
                    code_with_details = get_bin(5, 3) + get_bin(255, 8) + str(int(type == 'ntype'))

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
    flipped_final_concatenated = final_concatenated[::-1]
    if preappend != None:
        flipped_final_concatenated = preappend + flipped_final_concatenated
    if postappend != None:
        flipped_final_concatenated = flipped_final_concatenated + postappend
    if printout == True:
        print('-------------------------------')
        print('Strings to copy-paste...')
        print('bitpattern:')
        print(str(len(final_concatenated)) + '\'b' + str(final_concatenated))
        print('number of bits:')
        print(str(len(final_concatenated)))
    if selected == True:
        if should_return == True:
            return flipped_final_concatenated
    else:
        return [0 for i in range(len(final_concatenated))]

def generate_labels(parameters,are_parameters_MS2LS = False, selected = False):
    label_gen = ''
    reststate_gen = ''
    reststate_collector = []
    reststates = ['gnd!', 'vdd!']
    oblivion_count = -1
    for i in range(len(parameters)):
        oblivion_count += int(parameters[i]['type'] == 'Off')

    for h in range(len(parameters)-1):

        if are_parameters_MS2LS == False:
            i = len(parameters) - 1 - h
        else:
            i = h
        type = parameters[i]['type']
        if type =='voltage':
            volt = 1
            if parameters[i]['par'] <= 0.9:
                type = 'ntype'
            else:
                type = 'ptype'
        if type == 'ntype':
            label_gen = label_gen + parameters[i]['name']
            try:
                if parameters[i]['reset']:
                    reststate_gen = reststate_gen + reststates[1]
                    reststate_collector.append(reststates[1])
                else:
                    reststate_gen = reststate_gen + reststates[0]
                    reststate_collector.append(reststates[0])
            except KeyError:
                reststate_gen = reststate_gen + reststates[0]
                reststate_collector.append(reststates[0])
        elif type == 'ptype':
            label_gen = label_gen + parameters[i]['name']
            try:
                if parameters[i]['reset']:
                    reststate_gen = reststate_gen + reststates[0]
                    reststate_collector.append(reststates[0])
                else:
                    reststate_gen = reststate_gen + reststates[1]
                    reststate_collector.append(reststates[1])
            except KeyError:
                reststate_gen = reststate_gen + reststates[1]
                reststate_collector.append(reststates[1])
        elif type == 'Off':
            label_gen = label_gen + 'oblivion<' + str(oblivion_count) + '>'
            reststate_gen = reststate_gen + reststates[0]
            oblivion_count -= 1
            reststate_collector.append(reststates[0])
        else:
            print('An error occured')
            raise ValueError
        if h < len(parameters)-2:
            label_gen = label_gen + ','
            reststate_gen = reststate_gen + ','
    if selected == True:
        print('-------------------------------')
        print('Label Generated:')
        print(label_gen)
        print(reststate_gen)
        print('-------------------------------')
        print("Press ENTER 2 times to see rails")
        input()
        generate_vrail_guidance(parameters,reststate_collector, are_parameters_MS2LS)

def generate_vrail_guidance(parameters, reststate_collector, are_parameters_MS2LS):
    if are_parameters_MS2LS:
        for i in range(0, len(reststate_collector)):
            print(parameters[len(reststate_collector)-1-i]['name'] + ' | Rail<' + str(i) + '>: ' + reststate_collector[len(reststate_collector)-1-i])
    else:
        for i in range(0, len(reststate_collector)):
            print(parameters[i+1]['name'] + ' | Rail<' + str(i) + '>: ' + reststate_collector[i])

def generate_wiki_table(parameters, reststate_collector, are_parameters_MS2LS):
    print('^ Parameter Model ^ Rail Number ^ Initial State ^')
    if are_parameters_MS2LS:
        for i in range(0, len(reststate_collector)):
            print('| ' + parameters[len(reststate_collector)-1-i]['name'] + ' | Rail<' + str(i) + '> | ' + reststate_collector[len(reststate_collector)-1-i] + ' |')
    else:
        for i in range(0, len(reststate_collector)):
            print('| ' + parameters[i+1]['name'] + ' | Rail<' + str(i) + '>: ' + reststate_collector[i] + ' |')
