from Generate_bitstream import *
are_parameters_MS2LS = True
preappend = None
postappend = None

parameters = [
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name' : 'Unused Channels'},
    {'par': 500e-9, 'type': 'ntype', 'name' : 'bias_NI'},
    {'par': 1e-9, 'type': 'ntype', 'name': 'ref_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name' : 'leak_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'rest_PI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'thr_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'Trg_tau_PI'},
    {'par': 10000e-12, 'type': 'ntype', 'name' : 'Trg_w_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'Fac_tau_PI'},
    {'par': 100-12, 'type': 'ntype', 'name' : 'Fac_w_NI'},
    {'par': 100e-12, 'type': 'ptype', 'name' : 'Fac_gain_PI'},
    {'par': 700e-9, 'type': 'ntype', 'name' : 'Buffer drive strength param'}
]
generate_bitstream(parameters, are_parameters_MS2LS=are_parameters_MS2LS, preappend=preappend, postappend=postappend,selected=True, printout=True)
generate_labels(parameters, are_parameters_MS2LS=are_parameters_MS2LS)
