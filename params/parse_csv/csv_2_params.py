import csv
from string_2_sciNotation import *
  
def csv_2_params(filename = '', are_parameters_MS2LS = True, channels = 31):

    parameters_temp = []
    parameters = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        row_counter = 0

        # extracting each data row one by one
        for row in csvreader:
            if row[1] == '':
                par_ = '100p'
            elif row[1] != '':
                par_ = row[1]
            elif row[2] != '':
                par_ = row[2]
            else:
                exit('\nno valid bias value in .csv')

            
            type_ = row[4]
            name_ = row[0]
            reset = False

            # if row[5] == 'TRUE':
            #     reset = True

            dict_ = {
                'par': string_2_sciNotation(par_),
                'type': type_,
                'name': name_,
                'reset': reset,
            }

            parameters_temp.append(dict_)

            row_counter += 1

    if are_parameters_MS2LS:
        for i in range(0, channels - len(parameters_temp) - 1):
            parameters.append({'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'})
        
        for param in parameters_temp:
            parameters.append(param)

        parameters.append({'par': 700e-9, 'type': 'ntype', 'name': 'Buffer_drive_NI'})
    else:
        parameters.append({'par': 700e-9, 'type': 'ntype', 'name': 'Buffer_drive_NI'})

        for i in range(0, channels - len(parameters_temp) - 1):
            parameters.append({'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'})
        
        for param in parameters_temp:
            parameters.append(param)

    return parameters

def param_2_csv(filename,parameters):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row_ix, row, in enumerate(csvreader):
            if row_ix == 0:
                header = row
    with open(filename.replace('.csv','') + 'mod.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f,fieldnames=parameters[30].keys())

        # write the header
        writer.writeheader()
        for data in parameters:
        # write multiple rows
            writer.writerow(data)