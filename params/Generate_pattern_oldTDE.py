from Generate_bitstream import *
are_parameters_MS2LS = True

parameters = [
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
    {'par': 10e-9, 'type': 'ntype', 'name': 'bias_NI'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-9, 'type': 'ntype', 'name': 'refr_NI'},
    {'par': 10e-12, 'type': 'ntype', 'name': 'leak_NI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'rest_PI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'thr_NI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'Fac_gain_NI'},
    {'par': 120e-12, 'type': 'ntype', 'name': 'Trg_gain_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'tau_trg_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'tau_fac_PI', 'reset': True}, #LSB
    {'par': 700e-9, 'type': 'ntype', 'name': 'Buffer_drive_NI'},
]
generate_bitstream(parameters, are_parameters_MS2LS=are_parameters_MS2LS)
generate_labels(parameters, are_parameters_MS2LS=are_parameters_MS2LS)


