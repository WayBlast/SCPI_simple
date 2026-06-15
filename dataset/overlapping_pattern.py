import numpy

def oj_200ms(regular=True,invert=False,disable_teacher=False, seed=2):
    epochs= 4
    duration = 3000
    pre_rep = 1
    post_rep = 1


    #Neurons generating a stochastic, repeating input signal - each is connected to the neuron of interest with one synapse
    numpy.random.seed(seed)                                                              #seed for pseudo-randomness 

    N_signals_per_plastic = int(60*(duration/1000))    #total number of input spikes per period
    print(N_signals_per_plastic)
    N_signals_per_teacher = int(300*(duration/1000)) 	 # number for exc and inh teacher	
    N_signals_per_teacher_inh = int(120*(duration/1000)) 	 # number for inh teacher	                                            
    N_input_exc = 30	
    N_input_inh = 30	
    N_input = N_input_exc+N_input_inh			                                             #number of input synapses

    # count goes from 0 to 29 for 5x6 pattern, with sorter side counted first
    
    pattern_j_30 = [] #no need to use
    pattern_l_30 = [] #no need to use
    pattern__30 = []
    pattern_o_30 = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28] #checker 1 (blue, pixel_0 = 1)
    pattern_I_30 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29] # checker 2 (green, pixel_0 = 0)




    #pattern_o_30 = [2, 6, 8, 10, 14, 15, 17, 19, 21, 23] # heart
    #pattern_I_30 = [7, 11, 13, 15, 19, 21, 23, 27] # diamond
    #previous patterns
    #pattern_o_30 = [1, 2, 3, 5, 9, 10, 14, 15, 19, 20, 24, 26, 27, 28] # o
    #pattern_I_30 = [2, 7, 12, 17, 22, 27, 3, 16, 18] # this pattern is actually a "t" shape with the last 3 elements.
   




     			                                                   #period of the signal (in ms)
    indexes = numpy.array([])
    times = numpy.array([])
    labels = numpy.empty((0,2),dtype=int)
    
    start_time_us = 1                                       

    for runnumber in range(epochs):
        if regular:
            times_o = numpy.array([])
            index_o = numpy.array([])
            times_j = numpy.array([])
            index_j = numpy.array([])
            for i in range(len(pattern_I_30)):
                times_o = numpy.hstack((times_o,numpy.linspace(start=0, stop=10*duration, num=N_signals_per_plastic, dtype=int)))
                index_o = numpy.hstack((index_o,numpy.full(N_signals_per_plastic,pattern_I_30[i])))	 
            for i in range(len(pattern_o_30)):
                times_j = numpy.hstack((times_j,numpy.linspace(start=0, stop=10*duration, num=N_signals_per_plastic, dtype=int)))
                index_j = numpy.hstack((index_j,numpy.full(N_signals_per_plastic,pattern_o_30[i])))        
            times_t = numpy.linspace(start=0, stop=10*duration, num=N_signals_per_teacher, dtype=int)	           #Choose <N_signals> random times at which a neuron fires, each time occurs only once to avoid that one neuron fires twice at the same timE
            times_i = numpy.linspace(start=0, stop=10*duration, num=N_signals_per_teacher_inh, dtype=int)
        else:
            times_o = numpy.random.choice(10*duration,N_signals_per_plastic*len(pattern_o_30))	           #Choose <N_signals> random times at which a neuron fires, each time occurs only once to avoid that one neuron fires twice at the same time
            index_o = numpy.random.choice(pattern_o_30,size=times_o.size)	
            #times_j = numpy.random.choice(10*duration,N_signals_per_plastic*len(pattern_j_30))	           #Choose <N_signals> random times at which a neuron fires, each time occurs only once to avoid that one neuron fires twice at the same time
            #index_j = numpy.random.choice(pattern_j_30,size=times_j.size)	
            times_j = numpy.random.choice(10*duration, N_signals_per_plastic * len(pattern_o_30))
            index_j = numpy.random.choice(pattern_o_30, size=times_j.size)
            times_t = numpy.random.choice(10*duration,N_signals_per_teacher)	           #Choose <N_signals> random times at which a neuron fires, each time occurs only once to avoid that one neuron fires twice at the same time
            times_i = numpy.linspace(start=0, stop=10*duration, num=N_signals_per_teacher_inh, dtype=int)

        times_o = times_o*100
        times_j = times_j*100
        times_t = times_t*100
        times_i = times_i*100

        tmp_label = numpy.empty((2,2),dtype=int)
        tmp_label[0][0] = start_time_us
        tmp_label[0][1] = int(invert)

        indexes = numpy.hstack((indexes,index_o+2))
        times = numpy.hstack((times,times_o+start_time_us))
        if runnumber >= pre_rep and runnumber < epochs-post_rep and not disable_teacher:
            if invert:
                indexes = numpy.hstack((indexes,numpy.full(times_t.shape,1,dtype=int)))
                times = numpy.hstack((times,times_t+start_time_us))
            indexes = numpy.hstack((indexes,numpy.full(times_i.shape,0,dtype=int)))
            times = numpy.hstack((times,times_i+start_time_us))
        start_time_us += 1000*duration
        tmp_label[1][0] = start_time_us
        tmp_label[1][1] = int(not invert)
                
        indexes = numpy.hstack((indexes,index_j+2))
        times = numpy.hstack((times,times_j+start_time_us))
        if runnumber >= pre_rep and runnumber < epochs-post_rep and not disable_teacher:
            if not invert:
                indexes = numpy.hstack((indexes,numpy.full(times_t.shape,1,dtype=int)))
                times = numpy.hstack((times,times_t+start_time_us))
            indexes = numpy.hstack((indexes,numpy.full(times_i.shape,0,dtype=int)))
            times = numpy.hstack((times,times_i+start_time_us))

        labels = numpy.append(labels,tmp_label,axis=0)
        start_time_us += 1000*duration



    spike_array = numpy.stack((times,indexes),axis=-1)

    return (spike_array[spike_array[:,0].argsort()],labels,duration*2*1000*(epochs-post_rep),duration*2*1000*pre_rep,duration*2*1000*epochs)

