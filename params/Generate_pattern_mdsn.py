from Generate_bitstream import *
are_parameters_MS2LS = True
preappend = None
postappend = None

parameters = [
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'}, #MSB <29> far right
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},

    {'par': 100e-9, 'type': 'ntype', 'name': 'bias_NI'},

    {'par': 20e-12, 'type': 'ntype', 'name': 'learnDepDelay_NI', 'reset': True},
    {'par': 30e-12, 'type': 'ntype', 'name': 'learnPotDelay_NI', 'reset': True},
    {'par': 50e-12, 'type': 'ntype', 'name': 'learnNoneDelay_NI', 'reset': True},
    {'par': 1e-9, 'type': 'ntype', 'name': 'nrn2syn_pw_NI', 'reset': True},
    {'par': 20e-9, 'type': 'ntype', 'name': 'nrn_dump_NI', 'reset':True},
    {'par': 10e-12, 'type': 'ntype', 'name': 'nrn_ref_NI'},
    {'par': 10e-12, 'type': 'ntype', 'name': 'nrn_leak_NI', 'reset': True},
    {'par': 100e-12, 'type': 'ptype', 'name': 'nrn_rest_PI'},
    {'par': 100e-12, 'type': 'ntype', 'name': 'nrn_thr_NI'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<9>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<6>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<3>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<10>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<7>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<0>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<11>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<4>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<1>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_ext_NI'}, #LSB
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<8>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<5>'},
    {'par': 2e-9, 'type': 'ntype', 'name': 'syn_w_NI_<2>'},
    {'par': 1e-9, 'type': 'ptype', 'name': 'syn_thr_PI'},
    {'par': 20e-12, 'type': 'ptype', 'name': 'syn_tau_PI', 'reset':True},
    {'par': 700e-9, 'type': 'ntype', 'name': 'Buffer_drive_NI'},

]

parameters_config0 = [
        {'par': 1, 'name': 'conf0'},  # conf0
        {'par': 0, 'name': 'conf1'},  # conf1
        {'par': 0, 'name': 'conf2'},  # conf2
        {'par': 0, 'name': 'conf3'},  # conf3
        {'par': 0, 'name': 'conf4'},  # conf4
        {'par': 0, 'name': 'conf5'},  # conf5
        {'par': 0, 'name': 'conf6'},  # conf6
        {'par': 0, 'name': 'conf7'},  # conf7
        {'par': 0, 'name': 'conf8'},  # conf8
        {'par': 0, 'name': 'conf9'},  # conf9
        {'par': 0, 'name': 'conf10'},  # conf10
        {'par': 0, 'name': 'conf11'},  # conf11
]

parameters_config1 = [
        {'par': 1, 'name': 'conf0'},  # conf0
        {'par': 0, 'name': 'conf1'},  # conf1
        {'par': 0, 'name': 'conf2'},  # conf2
        {'par': 0, 'name': 'conf3'},  # conf3
        {'par': 0, 'name': 'conf4'},  # conf4
        {'par': 0, 'name': 'conf5'},  # conf5
        {'par': 0, 'name': 'conf6'},  # conf6
        {'par': 0, 'name': 'conf7'},  # conf7
        {'par': 0, 'name': 'conf8'},  # conf8
        {'par': 0, 'name': 'conf9'},  # conf9
        {'par': 0, 'name': 'conf10'},  # conf10
        {'par': 0, 'name': 'conf11'},  # conf11
]

parameters_config2 = [
        {'par': 1, 'name': 'conf0'},  # conf0
        {'par': 0, 'name': 'conf1'},  # conf1
        {'par': 0, 'name': 'conf2'},  # conf2
        {'par': 0, 'name': 'conf3'},  # conf3
        {'par': 0, 'name': 'conf4'},  # conf4
        {'par': 0, 'name': 'conf5'},  # conf5
        {'par': 0, 'name': 'conf6'},  # conf6
        {'par': 0, 'name': 'conf7'},  # conf7
        {'par': 0, 'name': 'conf8'},  # conf8
        {'par': 0, 'name': 'conf9'},  # conf9
        {'par': 0, 'name': 'conf10'},  # conf10
        {'par': 0, 'name': 'conf11'},  # conf11
]

parameters_config3 = [
        {'par': 1, 'name': 'conf0'},  # conf0
        {'par': 0, 'name': 'conf1'},  # conf1
        {'par': 0, 'name': 'conf2'},  # conf2
        {'par': 0, 'name': 'conf3'},  # conf3
        {'par': 0, 'name': 'conf4'},  # conf4
        {'par': 0, 'name': 'conf5'},  # conf5
        {'par': 0, 'name': 'conf6'},  # conf6
        {'par': 0, 'name': 'conf7'},  # conf7
        {'par': 0, 'name': 'conf8'},  # conf8
        {'par': 0, 'name': 'conf9'},  # conf9
        {'par': 0, 'name': 'conf10'},  # conf10
        {'par': 0, 'name': 'conf11'},  # conf11
]

parameters_config4 = [
        {'par': 1, 'name': 'conf0'},  # conf0
        {'par': 0, 'name': 'conf1'},  # conf1
        {'par': 0, 'name': 'conf2'},  # conf2
        {'par': 0, 'name': 'conf3'},  # conf3
        {'par': 0, 'name': 'conf4'},  # conf4
        {'par': 0, 'name': 'conf5'},  # conf5
        {'par': 0, 'name': 'conf6'},  # conf6
        {'par': 0, 'name': 'conf7'},  # conf7
        {'par': 0, 'name': 'conf8'},  # conf8
        {'par': 0, 'name': 'conf9'},  # conf9
        {'par': 0, 'name': 'conf10'},  # conf10
        {'par': 0, 'name': 'conf11'},  # conf11
]
generate_bitstream(parameters, are_parameters_MS2LS=are_parameters_MS2LS, preappend=preappend, postappend=postappend)
generate_labels(parameters, are_parameters_MS2LS=are_parameters_MS2LS)



