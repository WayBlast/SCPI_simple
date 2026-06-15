# import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
# import os
import os, sys
import logging
sys.path.append(os.path.join('parse_csv'))

get_bin = lambda x, n: format(x, 'b').zfill(n)
# Current_PATH = os.getcwd()
# FILE_PATH = os.path.dirname(os.getcwd())
# DATA_PATH = os.path.join(FILE_PATH, 'Data')
file_current = '../params/parametergen_current_levels.csv'
data_pressure = pd.read_csv(file_current, sep=',')
def string_2_sciNotation(x = ''):
	try:
		x_unit = x[-1]
		x_val = float(x[:-1])
	except:
		return float(x)

	res = any(chr.isdigit() for chr in x_unit)

	if res:
		return float(x)

	if x_unit == 'm':
		x_val = x_val/1000
		sciNot = '{:e}'.format(x_val)
	elif x_unit == 'u':
		x_val = x_val/1000000
		sciNot = '{:e}'.format(x_val)
	elif x_unit == 'n':
		x_val = x_val/1000000000
		sciNot = '{:e}'.format(x_val)
	elif x_unit == 'p':
		x_val = x_val/1000000000000
		sciNot = '{:e}'.format(x_val)
	elif x_unit == 'f':
		x_val = x_val/1000000000000000
		sciNot = '{:e}'.format(x_val)

	return float(sciNot)
class code_for_DAC:
    def __init__(self,CBIAS,param,np):
        self.CBIAS = CBIAS
        self.param = param
        self.np = np
    def combine_code(self,LSB_first = True):
        output = str(self.CBIAS) + str(self.param) + str(self.np)
        if LSB_first == True:
            output = output[::-1]
        return output
def generate_bitstream(parameters, are_parameters_MS2LS=False, preappend=None, postappend=None, channelsnumber = 31, selected = False, should_return = False, printout = False):
    final_concatenated = ''
    final_concatenated_collection = []
    try:
        assert (len(parameters) == channelsnumber), "The number of channels is not " + str(channelsnumber) + " but is " + str(len(parameters)) + ". If it's correct then put the variable channelsnumber to the expected number of channels"
    except AssertionError:
        logging.error(parameters)
        raise AssertionError
    logging.info('Generating bitstream for ' + str(len(parameters)) + ' channels')

    for k in range(len(parameters)):
        if are_parameters_MS2LS == True:
            h = len(parameters) - 1 - k
        else:
            h = k
        par = parameters[h]['par']
        type = parameters[h]['type']
        name = parameters[h]['name']
        logging.debug('Generating bitstream for ' + name + ' with value ' + str(par) + ' and type ' + type)
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

        if (type != 'Off') & (selected == True):
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
                                code_with_details = code_for_DAC(CBIAS= get_bin(i, 3),param = str(code),np=str(int(type == 'ntype')))
                                parameters[h]['code'] = code_with_details
                                # code_with_details = get_bin(i, 3) + str(code) + str(int(type == 'ntype'))
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
                                    j]) / par, 2)) + '% Code is: ' + get_bin(i, 3) + "|" + str(code)+ "|" + str(int(type == 'ntype')) + '. equivalent volt is '  + str(data_pressure[data_pressure.columns[i + 1 + 12 + int(type == 'ptype') * 6]][
                                        j]))
                            logging.debug('Wanted: ' + str(par) + '. Real: ' + str(
                                data_pressure[data_pressure.columns[i + 1 + volt * 12 + int(type == 'ptype') * 6]][
                                    j]) + '. Error = ' + str(round(100 * (
                                    par - data_pressure[data_pressure.columns[i + 1 + volt * 12 + int(type == 'ptype') * 6]][
                                j]) / par, 2)) + '% Code is: ' + get_bin(i, 3) + "|" + str(code)+ "|" + str(int(type == 'ntype')) + '. equivalent volt is '  + str(data_pressure[data_pressure.columns[i + 1 + 12 + int(type == 'ptype') * 6]][
                                    j]))
                            state = 'completed'
                            # code_with_details = get_bin(i, 3) + str(code) + str(int(type == 'ntype'))
                            code_with_details = code_for_DAC(CBIAS=get_bin(i, 3), param=str(code),
                                                             np=str(int(type == 'ntype')))
                            parameters[h]['code'] = code_with_details

            if state == 'incomplete':

                if par < data_pressure[data_pressure.columns[0 + 1 + volt * 12 +  int(type == 'ptype') * 6]][0]:
                    if printout == True:
                        print(name + ' | Wanted: ' + str(
                            par) + ' Didn\'t find any good values for this. I am taking the lower possible ' + str(
                            data_pressure[data_pressure.columns[0 + 1 + volt * 12 + int(type == 'ptype') * 6]][255]) + '. Error = ' + str((
                                        -par + data_pressure[data_pressure.columns[0 + 1 + volt * 12 + int(type == 'ptype') * 6]][
                                    255])) + ' Code is: ' + get_bin(0, 3) + "|" + get_bin(255, 8) + "|" + str(int(type == 'ntype')) + '. equivalent volt is '  + str(data_pressure[data_pressure.columns[0 + 1 + 12 + int(type == 'ptype') * 6]][
                                        255]))
                    logging.debug(name + ' | Wanted: ' + str(
                        par) + ' Didn\'t find any good values for this. I am taking the lower possible ' + str(
                        data_pressure[data_pressure.columns[0 + 1 + volt * 12 + int(type == 'ptype') * 6]][255]) + '. Error = ' + str((
                                    -par + data_pressure[data_pressure.columns[0 + 1 + volt * 12 + int(type == 'ptype') * 6]][
                                255])) + ' Code is: ' + get_bin(0, 3) + "|" + get_bin(255, 8) + "|" + str(int(type == 'ntype')) + '. equivalent volt is '  + str(data_pressure[data_pressure.columns[0 + 1 + 12 + int(type == 'ptype') * 6]][
                                    255]))
                    code_with_details = code_for_DAC(CBIAS=get_bin(0, 3), param=str(get_bin(255, 8)),
                                                     np=str(int(type == 'ntype')))
                    parameters[h]['code'] = code_with_details
                elif par > data_pressure[data_pressure.columns[5 + 1 + volt * 12 +  int(type == 'ptype') * 6]][255]:
                        # code_with_details = get_bin(0, 3) + get_bin(255, 8) + str(int(type == 'ntype'))
                    # print(name + ' | Wanted: ' + str(par) + ' Didn\'t find any good values for this. I am taking ' + str(
                    #     data_pressure[data_pressure.columns[5 + 1 + volt * 12 +  int(type == 'ptype') * 6]][0]))
                # if volt and int(type == 'ptype'):
                #     code_with_details = get_bin(0, 3) + get_bin(0, 8) + str(int(type == 'ntype'))
                # else:
                #     code_with_details = get_bin(5, 3) + get_bin(255, 8) + str(int(type == 'ntype'))
                    code_with_details = code_for_DAC(CBIAS=get_bin(7, 3), param=str(get_bin(0, 8)),
                                                     np=str(int(type == 'ntype')))
                    parameters[h]['code'] = code_with_details
                    logging.debug(name + ' | Wanted: ' + str(
                        par) + ' Didn\'t find any good values for this. I am taking the higher possible ' + str(
                        data_pressure[data_pressure.columns[5 + 1 + volt * 12 + int(type == 'ptype') * 6]][0]) + '. Error = ' + str((
                                    par - data_pressure[data_pressure.columns[5 + 1 + volt * 12 + int(type == 'ptype') * 6]][
                                0])) + ' Code is: ' + get_bin(7, 3) + "|" + get_bin(0, 8) + "|" + str(int(type == 'ntype')) + '. equivalent volt is '  + str(data_pressure[data_pressure.columns[5 + 1 + 12 + int(type == 'ptype') * 6]][
                                    0]))
                else:
                    raise ValueError
        else:
            code = get_bin(0, 8)
            prefix = get_bin(0,3)
            suffix = 0
            # code_with_details = str(prefix) + str(code) + str(suffix)
            code_with_details = code_for_DAC(CBIAS=prefix, param=str(code),
                                             np=str(suffix))
            parameters[h]['code'] = code_with_details
            i = 0
            # code = code[::-1]

        # final_concatenated = code_with_details + final_concatenated
        # final_concatenated_collection.append(code_with_details)
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
    if printout == True:
        print('-------------------------------')
        # print('Strings to copy-paste...')
        # print('bitpattern:')
        # print(str(len(final_concatenated)) + '\'b' + str(final_concatenated))
        # print('number of bits:')
        # print(str(len(final_concatenated)))
    return parameters

def generate_labels(parameters,are_parameters_MS2LS = False, selected = False,return_data = False):
    label_gen = ''
    reststate_gen = ''
    reststate_collector = []
    reststates = ['vssd', 'vdda']
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
    if return_data == True:
        return reststate_collector
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
            print('| ' + parameters[len(reststate_collector)-1-i]['name'] + ' | Rail<' + str(i) + '> | ' + reststate_collector[len(reststate_collector)-1-i] + ' |' + str(parameters[len(reststate_collector)-1-i]['par']) + ' | '+ parameters[len(reststate_collector)-1-i]['type'] + ' |')
    else:
        for i in range(0, len(reststate_collector)):
            print('| ' + parameters[i+1]['name'] + ' | Rail<' + str(i) + '>: ' + reststate_collector[i] + ' |')

def infer_values_from_maestro(maestro_file,parameters,printout = True):
    import csv
    import difflib
    parameters_keys = []
    for parameter in parameters:
        parameters_keys.append(parameter['name'])
    with open(maestro_file, 'r') as csvfile:
       csvreader = csv.reader(csvfile)

       for row in csvreader:
            flag_finish = False
            closest_match = difflib.get_close_matches(row[1], parameters_keys)
            if ('PFI' in row[1]) or ('NFI' in row[1]):
                while flag_finish == False:
                    if len(closest_match) == 0:
                        print('No matches found for',row[1], '. Skipping it')
                        flag_finish = True
                    elif len(closest_match) == 1:
                        print(row[1], 'resembles', closest_match,' Type \'y\' to select it or type a value to overwrite it. Write \'skip\' to skip it.')
                        if row[1] != closest_match:
                            command = input()
                        else:
                            command = 'y'
                            print(row[1],'Directly using this')

                        if command == 'y':
                            my_index = parameters_keys.index(closest_match)
                            parameters[my_index]['par'] = string_2_sciNotation(row[2])
                            parameters[my_index]['modified'] = True
                            flag_finish = True
                        elif command == 'skip':
                            flag_finish = True
                        else:
                            my_index = parameters_keys.index(closest_match)
                            parameters[my_index]['par'] = string_2_sciNotation(command)
                            parameters[my_index]['modified'] = True
                            flag_finish = True
                    elif len(closest_match) > 1:
                        if row[1] != closest_match[0]:
                            print(row[1], 'resembles', closest_match,
                                  ' Type the number to select it or type a value to overwrite it. Write \'skip\' to skip it.')

                            command = input()
                        else:
                            command = '0'
                            if printout == True:
                                print(row[1], '==', closest_match[0],
                                      '. Directly using this (among multiple)')
                        for choice in range(len(closest_match)):
                            if command == str(choice):
                                my_index = parameters_keys.index(closest_match[choice])

                                parameters[my_index]['par'] = string_2_sciNotation(row[2])
                                parameters[my_index]['modified'] = True
                                flag_finish = True
                            elif command == 'skip':
                                flag_finish = True
    return parameters
    print('wee')

#THE FOLLOWING CODE IS BAD, DON'T USE IT
# def from_binstr_to_int(binstr_to_int):
#     my_int = 0
#     mysize = len(binstr_to_int)
#     for binstr_idx,binstr in enumerate(binstr_to_int):
#         my_int += int(binstr)*2**(mysize-1-binstr_idx)
#     return my_int
# def code_to_voltage(parameters,codes):
#     p_or_n = ['ptype','ntype']
#     for code_idx,code in enumerate(codes):
#         # code = code[::-1]
#
#         which_bias = from_binstr_to_int(code[2:0])
#         which_row = from_binstr_to_int(code[10:2])
#         voltage = data_pressure[data_pressure.columns[which_bias + 1 + 12 + (1-int(code[11])) * 6]][which_row]
#
#         print('Param',parameters[len(codes)-code_idx-1]['name'],'Voltage:',voltage,'V','type',p_or_n[int(code[11])])