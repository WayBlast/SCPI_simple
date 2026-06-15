from Generate_bitstream import *

are_parameters_MS2LS = False
preappend = None
postappend = None
parameter_size = 372
parameter_config_size = 12

parameters_D = [
    {'par': 700e-12, 'type': 'ntype', 'name': 'Buffer_drive_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'post_trace_tau2_PI', 'reset': True},     # parameter0<0>
    {'par': 1e-12, 'type': 'ptype', 'name': 'post_trace_gain2_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'post_trace_gain1_PI'}, 
    {'par': 1e-12, 'type': 'ntype', 'name': 'post_trace_tau1_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ntype', 'name': 'post_trace_w_NI'}, 
    {'par': 1e-12, 'type': 'ntype', 'name': 'post_trace_pulsewidth_NI'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'soma_refractory_NI'},  #8
    {'par': 1e-12, 'type': 'ptype', 'name': 'soma_leak_NI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'soma_dc_PI'},  #10
    {'par': 1e-12, 'type': 'ntype', 'name': 'soma_gain_NI'}, #fix is nmos
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_conductance_inh_g_dc_NI'},        # parameter0<10>
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_conductance_e_const_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_conductance_inh_e_const_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_conductance_g_dc_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_inh_tau2_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_inh_gain2_PI'},                   # parameter0<15>
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_tau2_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_gain2_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_gain1_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_inh_gain1_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_tau1_PI', 'reset': True},         # parameter0<20>
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_inh_tau1_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_w_NI'},       #fo measurement
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_inh_w_NI'},   #fo measurement 
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_pulsewidth_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyninh_condactance_e_const_PI'},           # parameter0<25>
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyninh_condactance_g_dc_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyn_error_drive_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_error_drive_NI'},

]
parameters_C = [
    {'par': 700e-12, 'type': 'ntype', 'name': 'Buffer_drive_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyninh_error_offset_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyninh_error_offset_NI'},                  # parameter0<30>
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyninh_tau2_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyninh_gain2_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dynext_tau2_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dynext_gain2_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dynext_gain1_PI'},                         # parameter0<35>
    {'par': 1e-12, 'type': 'ntype', 'name': 'dynext_tau1_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyninh_gain1_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyninh_tau1_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_bias_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_weightbase_NI'},                     # parameter0<40>
    {'par': 1e-12, 'type': 'ntype', 'name': 'dynext_weighton_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyninh_weighton_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dynext_drift_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyninh_drift_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dynext_drift_NI'},                         # parameter0<45>
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyninh_drift_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_pulsewidth_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dynext_conductance_e_const_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dynext_conductance_g_dc_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dynext_error_offset_PI'},                  # parameter0<50>
    {'par': 1e-12, 'type': 'ntype', 'name': 'dynext_error_offset_NI'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 100e-12, 'type': 'Off', 'name': 'Unused Channels'},

]
parameters_E = [
    {'par': 25000e-9, 'type': 'ntype', 'name': 'Buffer_drive_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'soma_dc_PI'},                              # parameter1<8>  constant direct current to neuron
    {'par': 6000e-12, 'type': 'ntype', 'name': 'soma_gain_NI'},                         # parameter1<9>       multiplier on all inputs (inverted - lower value leads to higher gain)
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_conductance_inh_g_dc_NI'},          # parameter1<10>
    {'par': 80000e-12, 'type': 'ptype', 'name': 'static_conductance_e_const_PI'},         # parameter1<11>
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_conductance_inh_e_const_PI'},     # parameter1<12>
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_conductance_g_dc_PI'},              # parameter1<13>
    {'par': 20e-12, 'type': 'ptype', 'name': 'static_inh_tau2_PI', 'reset': True},      # parameter1<14>
    {'par': 100e-12, 'type': 'ptype', 'name': 'static_inh_gain2_PI'},                   # parameter1<15>
    {'par': 40e-12, 'type': 'ptype', 'name': 'static_tau2_PI', 'reset': True},          # parameter1<16>
    {'par': 100e-12, 'type': 'ptype', 'name': 'static_gain2_PI'},                       # parameter1<17>
    {'par': 100e-12, 'type': 'ptype', 'name': 'static_gain1_PI'},                       # parameter1<18>
    {'par': 100e-12, 'type': 'ptype', 'name': 'static_inh_gain1_PI'},                   # parameter1<19>
    {'par': 40e-12, 'type': 'ptype', 'name': 'static_tau1_PI', 'reset': True},          # parameter1<20>
    {'par': 20e-12, 'type': 'ptype', 'name': 'static_inh_tau1_PI', 'reset': True},      # parameter1<21>
    {'par': 1800e-12, 'type': 'ntype', 'name': 'static_w_NI'},                           # parameter1<22>
    {'par': 250e-12, 'type': 'ntype', 'name': 'static_inh_w_NI'},                       # parameter1<23>
    {'par': 100e-12, 'type': 'ntype', 'name': 'static_pulsewidth_NI'},                  # parameter1<24>
    {'par': 100e-12, 'type': 'ptype', 'name': 'dyn_condactance_e_const_PI'},           # parameter1<25>
    {'par': 100000e-12, 'type': 'ptype', 'name': 'dyn_condactance_g_dc_PI'},                # parameter1<26>
    {'par': 1000e-12, 'type': 'ptype', 'name': 'dyn_error_drive_PI'},                    # parameter1<27>
    {'par': 1500e-12, 'type': 'ntype', 'name': 'dyn_error_drive_NI'},                    # parameter1<28>
    {'par': 1500e-12, 'type': 'ptype', 'name': 'dyninh_error_offset_up_PI'},                  # parameter1<29>
    {'par': 1000e-12, 'type': 'ntype', 'name': 'dyninh_error_offset_down_NI'},                  # parameter1<30>
    {'par': 40e-12, 'type': 'ptype', 'name': 'dyninh_tau2_PI', 'reset': True},            # parameter1<31>
    {'par': 50e-12, 'type': 'ptype', 'name': 'dyninh_gain2_PI'},                         # parameter1<32>
    {'par': 40e-12, 'type': 'ptype', 'name': 'dynext_tau2_PI', 'reset': True},            # parameter1<33>
    {'par': 200e-12, 'type': 'ptype', 'name': 'dynext_gain2_PI'},                         # parameter1<34>
    {'par': 50e-12, 'type': 'ptype', 'name': 'dynext_gain1_PI'},                         # parameter1<35>
    {'par': 40e-12, 'type': 'ptype', 'name': 'dynext_tau1_PI', 'reset': True},            # parameter1<36>
    {'par': 100e-12, 'type': 'ptype', 'name': 'dyninh_gain1_PI'},                         # parameter1<37>

]
parameters_F = [
    {'par': 700e-9, 'type': 'ntype', 'name': 'Buffer_drive_NI'},                      
    {'par': 40e-19, 'type': 'ptype', 'name': 'dyninh_tau1_PI', 'reset': True},            # parameter1<38>
    {'par': 10e-12, 'type': 'ntype', 'name': 'dyn_bias_NI'},                           # parameter1<39>
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_weightbase_NI'},                       # parameter1<40>
    {'par': 90e-12, 'type': 'ntype', 'name': 'dynext_weighton_NI'},                        # parameter1<41>
    {'par': 45e-12, 'type': 'ntype', 'name': 'dyninh_weighton_NI'},                        # parameter1<42>
    {'par': 500e-12, 'type': 'ptype', 'name': 'dynext_drift_PI'},                         # parameter1<43>    
    {'par': 500e-12, 'type': 'ptype', 'name': 'dyninh_drift_PI'},                         # parameter1<44>
    {'par': 200e-12, 'type': 'ntype', 'name': 'dynext_drift_NI'},                         # parameter1<45>
    {'par': 200e-12, 'type': 'ntype', 'name': 'dyninh_drift_NI'},                         # parameter1<46>
    {'par': 50e-12, 'type': 'ntype', 'name': 'dyn_pulsewidth_NI'},                     # parameter1<47>
    {'par': 1e-12, 'type': 'ntype', 'name': 'c2f_gain_NI'},                           # parameter2<0>
    {'par': 1e-12, 'type': 'ptype', 'name': 'c2f_dc_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'c2f_refractory_NI'},
    {'par': 1e-10, 'type': 'ntype', 'name': 'c2f_leak_NI', 'reset': True},
    {'par': 1e-12, 'type': 'ntype', 'name': 'c2f_gain_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'c2f_dc_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'c2f_refractory_NI'},
    {'par': 1e-10, 'type': 'ntype', 'name': 'c2f_leak_NI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'c2f_drive_PI'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 20e-12, 'type': 'ptype', 'name': 'post_trace_tau2_PI', 'reset': True},      # parameter1<0>
    {'par': 300e-12, 'type': 'ptype', 'name': 'post_trace_gain2_PI'},                   # parameter1<1>
    {'par': 150e-12, 'type': 'ptype', 'name': 'post_trace_gain1_PI'},                   # parameter1<2>
    {'par': 20e-12, 'type': 'ptype', 'name': 'post_trace_tau1_PI', 'reset': True},      # parameter1<3>
    {'par': 180e-12, 'type': 'ntype', 'name': 'post_trace_w_NI'},                        # parameter1<4>
    {'par': 100e-12, 'type': 'ntype', 'name': 'post_trace_pulsewidth_NI'},              # parameter1<5>
    {'par': 1000e-12, 'type': 'ntype', 'name': 'soma_refractory_NI'},                    # parameter1<6>  Period of sleep after spike
    {'par': 12e-12, 'type': 'ntype', 'name': 'soma_leak_NI', 'reset': True},            # parameter1<7>   Loss of charge in capacitor (exponential)
]

parameters_I = [                                                                         # BCaLL parameters
    {'par': 700e-12, 'type': 'ntype', 'name': 'Buffer_drive_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyninhib_tau2_PI', 'reset': True},       # parameter<29>
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_pw_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_inhib_w_NI'},                     
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_excit_w_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_inhib_tau1_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_excit_tau1_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_inhib_gain1_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_excit_gain1_PI'},    
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_excit_gain2_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_excit_tau2_PI', 'reset': True},    # parameter<20>
    {'par': 1e-12, 'type': 'ptype', 'name': 'static_inhib_gain2_PI'},                          
    {'par': 1e-12, 'type': 'ntype', 'name': 'static_inhib_tau2_PI', 'reset': True},                          
    {'par': 1e-12, 'type': 'ntype', 'name': 'stop_trace_w_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'stop_trace_tau1_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'stop_trace_gain1_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'stop_trace_gain2_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'stop_trace_tau2_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'soma_dc_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'soma_leak_NI', 'reset': True},
    {'par': 1e-12, 'type': 'ntype', 'name': 'soma_refr_NI'},                           # parameter<10>
    {'par': 1e-12, 'type': 'ptype', 'name': 'soma_gain_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'soma_pw_NI'},     
    {'par': 1e-12, 'type': 'ptype', 'name': 'stop_learn_u_thr_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'stop_learn_l_thr_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'stop_learn_bias_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'post_trace_w_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'post_trace_tau_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'post_trace_gain_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'post_trace_thr_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'post_trace_bias_NI'},
]

parameters_J = [                                                                         # BCaLL parameters
    {'par': 700e-9, 'type': 'ntype', 'name': 'Buffer_drive_NI'},
    {'par': 700e-9, 'type': 'ntype', 'name': 'mon_mux_bias_NI'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'Off', 'name': 'Unused Channels'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_pw_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_pre_trace_w_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_pre_trace_tau_PI', 'reset': True},    # parameter<48>
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyn_pre_trace_gain_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyn_pre_trace_thr_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_bias_wta_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_pre_jump_neg_NI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyn_drift_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_post_jump_neg_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_drift_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_bias_NI'},                            # parameter<40>
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_excit_w1_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyninhib_w1_NI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_w0_NI'},
    {'par': 1e-11, 'type': 'ntype', 'name': 'dyninhib_tau1_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyninhib_gain1_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_excit_tau1_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyn_excit_gain1_PI'},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyn_excit_gain2_PI'},
    {'par': 1e-12, 'type': 'ntype', 'name': 'dyn_excit_tau2_PI', 'reset': True},
    {'par': 1e-12, 'type': 'ptype', 'name': 'dyninhib_gain2_PI'},
]

parameters_config_A = [                                             # DPSS
        {'par': 0, 'name': 'g_const_static_inhib'},                 # conf0
        {'par': 1, 'name': 'g_dendrite_static_excit'},              # conf1
        {'par': 1, 'name': 'g_dendrite_static_inhib'},              # conf2
        {'par': 1, 'name': 'e_const_static_excit'},                 # conf3
        {'par': 0, 'name': 'e_dendrite_static_excit'},              # conf4
        {'par': 1, 'name': 'e_const_static_inhib'},                 # conf5
        {'par': 0, 'name': 'g_const_static_excit'},                 # conf6
        {'par': 0, 'name': 'e_dendrite_static_inhib'},              # conf7
        {'par': 0, 'name': 'g_dendrite_dyn1'},                      # conf8
        {'par': 0, 'name': 'g_dendrite_dyn2'},                      # conf9
        {'par': 0, 'name': 'e_const_dyn1'},                         # conf10
        {'par': 0, 'name': 'e_const_dyn2'},                         # conf11
]
parameters_config_B = [                                             # DPSS
        {'par': 1, 'name': 'e_dendrite_dyn1'},                      # conf12
        {'par': 1, 'name': 'e_dendrite_dyn2'},                      # conf13
        {'par': 1, 'name': 'g_const_dyn1'},                         # conf14
        {'par': 1, 'name': 'g_const_dyn2'},                         # conf15
        {'par': 0, 'name': 'syn_invert_dyn1'},                      # conf16
        {'par': 0, 'name': 'syn_invert_dyn2'},                      # conf17
        {'par': 0, 'name': ''},                                     # conf18
        {'par': 0, 'name': ''},                                     # conf19
        {'par': 0, 'name': ''},                                     # conf20
        {'par': 0, 'name': ''},                                     # conf21
        {'par': 0, 'name': ''},                                     # conf22
        {'par': 0, 'name': ''},                                     # conf23
]

parameters_config_G = [                                             # DPSS
        {'par': 0, 'name': 'g_const_static_inhib'},                 # conf24
        {'par': 1, 'name': 'g_dendrite_static_excit'},              # conf25
        {'par': 1, 'name': 'g_dendrite_static_inhib'},              # conf26
        {'par': 1, 'name': 'e_const_static_excit'},                 # conf27
        {'par': 0, 'name': 'e_dendrite_static_excit'},              # conf28
        {'par': 1, 'name': 'e_const_static_inhib'},                 # conf29
        {'par': 0, 'name': 'g_const_static_excit'},                 # conf30
        {'par': 0, 'name': 'e_dendrite_static_inhib'},              # conf31
        {'par': 0, 'name': 'g_dendrite_dyn'},                       # conf32
        {'par': 0, 'name': 'e_const_dyn1'},                         # conf33
        {'par': 1, 'name': 'e_dendrite_dyn'},                       # conf34
        {'par': 1, 'name': 'g_const_dyn'},                          # conf35
]

parameters_config_H = [                                             # DPSS
        {'par': 1, 'name': 'syn_not_invert_excit'},                     # conf36
        {'par': 0, 'name': 'syn_not_invert_inhib'},                     # conf37
        {'par': 0, 'name': 'multiply_c2f_A0'},                      # conf38
        {'par': 0, 'name': 'multiply_c2f_A1'},                      # conf39
        {'par': 0, 'name': 'multiply_c2f_A2'},                      # conf40
        {'par': 0, 'name': 'multiply_c2f_A3'},                      # conf41
        {'par': 0, 'name': 'multiply_c2f_A4'},                      # conf42
        {'par': 0, 'name': 'multiply_c2f_B0'},                      # conf43
        {'par': 0, 'name': 'multiply_c2f_B1'},                      # conf44
        {'par': 0, 'name': 'multiply_c2f_B2'},                      # conf45
        {'par': 0, 'name': 'multiply_c2f_B3'},                      # conf46
        {'par': 0, 'name': 'multiply_c2f_B4'},                      # conf47
]

parameters_config_K = [                                             # BCaLL
        {'par': 0, 'name': 'en_inhib_static'},                      # conf0
        {'par': 0, 'name': 'en_inhib_dyn'},                         # conf1
        {'par': 0, 'name': 'syn_invert_inhib'},                     # conf2
        {'par': 0, 'name': 'syn_invert_excit'},                     # conf3
        {'par': 0, 'name': ''},                                     # conf4
        {'par': 0, 'name': ''},                                     # conf5
        {'par': 0, 'name': ''},                                     # conf6
        {'par': 0, 'name': ''},                                     # conf7
        {'par': 0, 'name': ''},                                     # conf8
        {'par': 0, 'name': ''},                                     # conf9
        {'par': 0, 'name': ''},                                     # conf10
        {'par': 0, 'name': ''},                                     # conf11
]

parameters_config_L = [                                             # Async
        {'par': 1, 'name': 'dly_out_0'},                            # conf0
        {'par': 1, 'name': 'dly_out_1'},                            # conf1
        {'par': 1, 'name': 'dly_out_2'},                            # conf2
        {'par': 0, 'name': 'dly_out_3'},                            # conf3
        {'par': 1, 'name': 'dly_in_0'},                             # conf4
        {'par': 0, 'name': 'dly_in_1'},                             # conf5
        {'par': 0, 'name': 'dly_in_2'},                             # conf6
        {'par': 0, 'name': 'dly_in_3'},                             # conf7
        {'par': 1, 'name': 'dly_0'},                                # conf8
        {'par': 1, 'name': 'dly_1'},                                # conf9
        {'par': 1, 'name': 'dly_2'},                                # conf10
        {'par': 1, 'name': 'dly_3'},                                # conf11
]

### FAST FIFO
#MSB to LSB
#
parameters_config_0 = [                                    # mon_switch_x displaying stuff (what r u looking at)
        {'par': 0, 'name': 'Unused'},                      # conf0
        {'par': 0, 'name': 'BCall_???'},                   # conf1
        {'par': 1, 'name': 'dynexc_pdpi_x'},               # conf2      mon 4
        {'par': 0, 'name': 'dyninh_pdpi_x'},               # conf3      mon 4
        {'par': 0, 'name': 'post_dpi_x'},                  # conf4      mon 3
        {'par': 0, 'name': 'inh_dpi_x'},                   # conf5      mon 3
        {'par': 1, 'name': 'exc_dpi_x'},                   # conf6      mon 3
        {'par': 0, 'name': 'update2'},                     # conf7      mon 1&2
        {'par': 1, 'name': 'update1'},                     # conf8      mon 1&2
        {'par': 1, 'name': 'soma_mem'},                    # conf9      mon 0
        {'par': 0, 'name': 'dyninh_w_x'},                  # conf10     mon 0
        {'par': 0, 'name': 'dynexc_w_x'},                  # conf11     mon 0
]

parameters_config_1 = [                                             # block_enable which neuron block u r looking at (we r always looking at the same neuron)
        {'par': 0, 'name': 'BCall_y_3'},                      # conf0
        {'par': 0, 'name': 'BCall_y_2'},                         # conf1
        {'par': 0, 'name': 'BCall_y_1'},                     # conf2
        {'par': 0, 'name': 'Bcall_y_0'},                     # conf3
        {'par': 0, 'name': 'dpss_inh_inv_co'},                                     # conf4
        {'par': 1, 'name': 'dpss_inh_y_2'},                                     # conf5
        {'par': 0, 'name': 'dpss_inh_y_1'},                                     # conf6
        {'par': 0, 'name': 'dpss_inh_y_0'},                                     # conf7
        {'par': 0, 'name': 'dpss_inv_co'},                                     # conf8
        {'par': 0, 'name': 'dpss_y_2'},                                     # conf9
        {'par': 0, 'name': 'dpss_y_1'},                                     # conf10
        {'par': 0, 'name': 'dpss_y_0'},                                     # conf11
]

parameters_config_2 = [                                             # fo_so_dpi different synapse 
        {'par': 0, 'name': 'syn_5'},                      # conf0
        {'par': 0, 'name': 'syn_4'},                         # conf1
        {'par': 0, 'name': 'syn_3'},                     # conf2
        {'par': 1, 'name': 'syn_2'},                     # conf3
        {'par': 0, 'name': 'syn_1'},                                     # conf4
        {'par': 0, 'name': 'syn_0'},                                     # conf5
        {'par': 1, 'name': 'dyn_so_dpi'},                                     # conf6
        {'par': 0, 'name': 'dyn_fo_dpi'},                                     # conf7
        {'par': 1, 'name': 'static_so_dpi'},                                     # conf8
        {'par': 0, 'name': 'static_fo_dpi'},                                     # conf9
        {'par': 1, 'name': 'soma_so_dpi'},                                     # conf10
        {'par': 0, 'name': 'soma_fo_dpi'},                                     # conf11
]

parameters_config_3 = [                                             # fo_so_dpi
        {'par': 0, 'name': 'syn_17'},                      # conf0
        {'par': 0, 'name': 'syn_16'},                         # conf1
        {'par': 0, 'name': 'syn_15'},                     # conf2
        {'par': 0, 'name': 'syn_14'},                     # conf3
        {'par': 0, 'name': 'syn_13'},                                     # conf4
        {'par': 0, 'name': 'syn_12'},                                     # conf5
        {'par': 0, 'name': 'syn_11'},                                     # conf6
        {'par': 0, 'name': 'syn_10'},                                     # conf7
        {'par': 0, 'name': 'syn_9'},                                     # conf8
        {'par': 0, 'name': 'syn_8'},                                     # conf9
        {'par': 0, 'name': 'syn_7'},                                     # conf10
        {'par': 0, 'name': 'syn_6'},                                     # conf11
]

parameters_config_4 = [                                             # fo_so_dpi
        {'par': 0, 'name': 'syn_29'},                      # conf0
        {'par': 0, 'name': 'syn_28'},                         # conf1
        {'par': 0, 'name': 'syn_27'},                     # conf2
        {'par': 0, 'name': 'syn_26'},                     # conf3
        {'par': 0, 'name': 'syn_25'},                                     # conf4
        {'par': 0, 'name': 'syn_24'},                                     # conf5
        {'par': 0, 'name': 'syn_23'},                                     # conf6
        {'par': 0, 'name': 'syn_22'},                                     # conf7
        {'par': 0, 'name': 'syn_21'},                                     # conf8
        {'par': 0, 'name': 'syn_20'},                                     # conf9
        {'par': 0, 'name': 'syn_19'},                                     # conf10
        {'par': 0, 'name': 'syn_18'},                                     # conf11
]

parameters_config_5 = [                                             # fo_so_dpi
        {'par': 0, 'name': 'syn_30'},                      # conf0
        {'par': 0, 'name': 'reset_SI'},                         # conf1
        {'par': 0, 'name': 'Unused'},                     # conf2
        {'par': 0, 'name': 'Unused'},                     # conf3
        {'par': 0, 'name': 'Unused'},                                     # conf4
        {'par': 0, 'name': 'Unused'},                                     # conf5
        {'par': 0, 'name': 'Unused'},                                     # conf6
        {'par': 0, 'name': 'Unused'},                                     # conf7
        {'par': 0, 'name': 'Unused'},                                     # conf8
        {'par': 0, 'name': 'Unused'},                                     # conf9
        {'par': 0, 'name': 'Unused'},                                     # conf10
        {'par': 0, 'name': 'Unused'},                                     # conf11
]

def convert_to_Bytearray(input_string):
    input_string = (len(input_string) % 8) * '0' + input_string
    array = []
    for i in range(len(input_string) // 8):
        x = input_string[8*i:8*(i+1)]
        array.append(int(x[::-1],2))
    return array

def create_SPI0_input(loop = 10):
    bitstream = parameter_size * '0'

    for i in range(12):
        bitstream += str(parameters_config_L[i]['par'])

    bitstream += (3*parameter_size + 12) * '0'


    list_of_parameters = [parameters_config_A, parameters_config_B, parameters_C, parameters_D, parameters_E, parameters_F, parameters_config_G, parameters_config_H, parameters_I, parameters_J, parameters_config_K]

    for parameter in list_of_parameters[::-1]:

        if parameter == parameters_E:
            parameter[1]["par"] = 10e-12 + 500000e-12*loop

        if parameter in [parameters_config_A, parameters_config_B, parameters_config_G, parameters_config_H, parameters_config_K]:
            for bit in parameter:
                bitstream += str(bit['par'])
        else:
            bitstream += generate_bitstream(parameter, are_parameters_MS2LS=are_parameters_MS2LS, preappend=preappend, postappend=postappend, selected=True, should_return=True)

            
            #if parameter == parameters_E:
            #
            #    __ = generate_bitstream(parameter, are_parameters_MS2LS=are_parameters_MS2LS, preappend=preappend, postappend=postappend, selected=True, should_return=True,printout=True)
  
    bitstream += 7 * parameter_size * '0'

    return convert_to_Bytearray(bitstream)



def create_SPI1_input():
    bitstream = parameter_config_size * '0'
    
    list_of_parameters = [parameters_config_0, parameters_config_1, parameters_config_2, parameters_config_3, parameters_config_4, parameters_config_5]
    for parameter in list_of_parameters[::-1]:
        for bit in parameter:
            bitstream += str(bit['par'])

    bitstream += 7 * parameter_config_size * '0'

    return convert_to_Bytearray(bitstream)
