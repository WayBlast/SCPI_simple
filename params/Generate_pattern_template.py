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
    {'par': 10e-9, 'type': 'ntype', 'name': 'bias_NI'},
    {'par': 10e-9, 'type': 'ptype', 'name': 'neuron_offset_thr_PI'},
    {'par': 1e-9, 'type': 'ntype', 'name': 'refr_NI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'leak_NI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'rest_PI'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'ptype', 'name': 'post_w_PI'},
    {'par': 1e-9, 'type': 'ntype', 'name': 'dep_mag_NI'},
    {'par': 10e-9, 'type': 'ntype', 'name': 'vtail_NI'},
    {'par': 1e-9, 'type': 'ptype', 'name': 'pot_mag_PI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'vbis_plus_NI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'pre_w_NI'},
    {'par': 10e-12, 'type': 'ntype', 'name': 'post_tau_NI', 'reset': True},
    {'par': 10e-12, 'type': 'ptype', 'name': 'pre_tau_PI', 'reset': True},
    {'par': 1e-9, 'type': 'ptype', 'name': 'neuron_delta_thr_PI'},
    {'par': 1e-9, 'type': 'ptype', 'name': 'st_PI'},
    {'par': 1e-9, 'type': 'ntype', 'name': 'st_NI'},
    {'par': 1e-9, 'type': 'ptype', 'name': 'syn_w_NI'},
    {'par': 1e-9, 'type': 'ptype', 'name': 'syn_thr_PI'},
    {'par': 1.5, 'type': 'voltage', 'name': 'syn_tau_PI', 'reset': True}, #LSB
    {'par': 700e-9, 'type': 'ntype', 'name': 'Buffer_drive_NI'},
]
generate_bitstream(parameters, are_parameters_MS2LS=are_parameters_MS2LS, preappend=preappend, postappend=postappend)
generate_labels(parameters, are_parameters_MS2LS=are_parameters_MS2LS)


