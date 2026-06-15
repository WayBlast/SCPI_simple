from Generate_bitstream import *
are_parameters_MS2LS = True
preappend = None
postappend = None

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
    {'par': 100e-9, 'type': 'ntype', 'name': 'bias_NI'},
    {'par': 1e-9, 'type': 'ntype', 'name': 'refr_osc_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'leak_osc_NI'},
    {'par': 200e-12, 'type': 'ptype', 'name': 'input_osc_PI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'thr_osc_NI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'w_syn_NI'},
    {'par': 5e-12, 'type': 'ptype', 'name': 'tau_syn_PI'},
    {'par': 100e-12, 'type': 'ptype', 'name': 'thr_syn_PI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'pw_NI', 'reset': True},
    {'par': 100e-9, 'type': 'ntype', 'name': 'st_NI', 'reset': True},
    {'par': 100e-9, 'type': 'ptype', 'name': 'st_PI', 'reset': True},
    {'par': 5e-9, 'type': 'ntype', 'name': 'refr_tde_NI'},
    {'par': 10e-12, 'type': 'ntype', 'name': 'leak_tde_NI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'rest_tde_PI'},
    {'par': 10e-12, 'type': 'ntype', 'name': 'thr_tde_NI'},
    {'par': 10e-9, 'type': 'ntype', 'name': 'Fac_w_NI'},
    {'par': 50e-12, 'type': 'ntype', 'name': 'Trg_w_NI'},
    {'par': 20e-12, 'type': 'ptype', 'name': 'Trg_tau_PI', 'reset': True},
    {'par': 10e-12, 'type': 'ptype', 'name': 'Fac_tau_PI', 'reset': True}, #LSB
    {'par': 700e-9, 'type': 'ntype', 'name': 'Buffer_drive_NI'},
]

generate_bitstream(parameters, are_parameters_MS2LS=are_parameters_MS2LS, preappend=preappend, postappend=postappend)
generate_labels(parameters, are_parameters_MS2LS=are_parameters_MS2LS)


