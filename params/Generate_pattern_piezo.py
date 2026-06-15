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
    {'par': 10e-9, 'type': 'ntype', 'name': 'bias_opamp_NI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'Vdiff_NI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'Vdon_NI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'vbn_NI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'Vdoff_NI'},
    {'par': 100e-12, 'type': 'ptype', 'name': 'Vsf_PI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'Vgcoff_NI'},
    {'par': 100e-12, 'type': 'ptype', 'name': 'Vref_PI'},
    {'par': 100e-12, 'type': 'ptype', 'name': 'Vgcon_PI'},
    {'par': 1e-9, 'type': 'ntype', 'name': 'refr_NI'},
    {'par': 10e-12, 'type': 'ntype', 'name': 'leak_NI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'rest_PI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'thr_NI'},
    {'par': 10e-9, 'type': 'ntype', 'name': 'bias_NI'},
    {'par': 10e-9, 'type': 'ptype', 'name': 'bias_PI'}, #LSB
    {'par': 700e-9, 'type': 'ntype', 'name': 'Buffer_drive_NI'},
]

parameters_config_0 = [                                             # mon_switch_x
        {'par': 0, 'name': '???'},                      # conf0
        {'par': 0, 'name': '???'},                         # conf1
        {'par': 0, 'name': '???'},                     # conf2
        {'par': 0, 'name': '???'},                     # conf3
        {'par': 0, 'name': '???'},                                     # conf4
        {'par': 1, 'name': '???'},                                     # conf5
        {'par': 0, 'name': '???'},                                     # conf6
        {'par': 0, 'name': '???'},                                     # conf7
        {'par': 0, 'name': '???'},                                     # conf8
        {'par': 0, 'name': '???'},                                     # conf9
        {'par': 0, 'name': '???'},                                     # conf10
        {'par': 0, 'name': '???'},                                     # conf11
]
generate_bitstream(parameters, are_parameters_MS2LS=are_parameters_MS2LS)
generate_labels(parameters, are_parameters_MS2LS=are_parameters_MS2LS)


