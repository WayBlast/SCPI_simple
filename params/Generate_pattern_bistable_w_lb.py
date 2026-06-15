import os, sys
from Generate_bitstream import *

sys.path.append(os.path.join('../params/parse_csv'))

from csv_2_params import *

are_parameters_MS2LS = False
preappend = None
postappend = None
channels = 31

filename = '../params/bistable_w_lb_module_dac_params.csv'

parameters = csv_2_params(
    filename = filename, 
    are_parameters_MS2LS = are_parameters_MS2LS,
    channels = channels)

# generate_bitstream(parameters, are_parameters_MS2LS=are_parameters_MS2LS, preappend=preappend, postappend=postappend)
# generate_labels(parameters, are_parameters_MS2LS=are_parameters_MS2LS)


