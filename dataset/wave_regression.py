import numpy

def wave_regression_200ms(disable_teacher=False):
    multtime=12
    prerep=2
    postrep=3
    N_duration = 200
    N_reps = multtime+prerep+postrep

    #Neurons generating a stochastic, repeating input signal - each is connected to the neuron of interest with one synapse
    numpy.random.seed(2)                                                              #seed for pseudo-randomness 

    N_signals = 512    #total number of input spikes per period
    N_signals_teacher = N_signals/4	 # number for exc and inh teacher		                                            
    N_input_exc = 32	
    N_input_inh = 32	
    N_input = N_input_exc+N_input_inh			                                             #number of input synapses
     			                                                   #period of the signal (in ms)
                                                 #number of repetitions of the signal -1 also defind below


    #Generate random pattern - one timestep is 0.1ms, i.e. 10 elements per ms
    tim = numpy.random.choice(10*N_duration,N_signals,replace = False)	           #Choose <N_signals> random times at which a neuron fires, each time occurs only once to avoid that one neuron fires twice at the same time
    ind = numpy.random.randint(0,N_input, size = N_signals)			           #Choose randomly which neuron fires at each time

    #Repeat the pattern
    indices = ind
    times = tim

    for l in range(N_reps):
    	times = numpy.hstack((times,tim+(1+l)*10*N_duration))
    	indices = numpy.hstack((indices,ind))
    indices += 2 #shift indices by 2 reserve the first two neurons for the teacher

    teacher_e_tim = []
    teach_mem = 0
    for timestep in range(N_duration*10):
        teach_mem += (N_signals_teacher*2/(N_duration*10))*(numpy.sin(numpy.pi*2/(10*N_duration)*timestep)+1)*0.5
        if teach_mem >= 1:
            teach_mem -= 1
            teacher_e_tim.append(timestep)

    teacher_i_tim = numpy.linspace(start=0, stop=N_duration*10, num=len(teacher_e_tim), dtype=int)

    teacher_e_tim = numpy.array(teacher_e_tim)

    teacher_i_times=numpy.array([])
    teacher_e_times=numpy.array([])
    if not disable_teacher:
        for l in range(prerep,N_reps-postrep):

            teacher_i_times = numpy.hstack((teacher_i_times,teacher_i_tim+((1+l)*10*N_duration)))
            teacher_e_times = numpy.hstack((teacher_e_times,teacher_e_tim+((1+l)*10*N_duration)))

    start_validation = (N_reps-postrep)*1000*N_duration
    end_baseline = (prerep)*1000*N_duration

    ## convert to us

    times = times*100
    teacher_e_times = teacher_e_times*100
    teacher_i_times = teacher_i_times*100

    spike_array = numpy.stack((times,indices),axis=-1)
    spike_array = numpy.append(spike_array,numpy.stack((teacher_e_times,numpy.full(teacher_e_times.shape,1,dtype=int)),axis=-1),axis=0)
    spike_array = numpy.append(spike_array,numpy.stack((teacher_i_times,numpy.full(teacher_i_times.shape,0,dtype=int)),axis=-1),axis=0)

    return (spike_array[spike_array[:,0].argsort()],None,start_validation,end_baseline,N_duration*1000*N_reps)


def wave_regression_400ms(disable_teacher=False):
    multtime=28
    prerep=3
    postrep=5
    N_duration = 600
    N_reps = multtime+prerep+postrep

    #Neurons generating a stochastic, repeating input signal - each is connected to the neuron of interest with one synapse
    numpy.random.seed(6)                                                              #seed for pseudo-randomness 

    N_signals = 1024    #total number of input spikes per period
    N_signals_teacher = N_signals/4	 # number for exc and inh teacher		                                            
    N_input_exc = 32	
    N_input_inh = 32	
    N_input = N_input_exc+N_input_inh			                                             #number of input synapses
     			                                                   #period of the signal (in ms)
                                                 #number of repetitions of the signal -1 also defind below


    #Generate random pattern - one timestep is 0.1ms, i.e. 10 elements per ms
    tim = numpy.random.choice(10*N_duration,N_signals,replace = False)	           #Choose <N_signals> random times at which a neuron fires, each time occurs only once to avoid that one neuron fires twice at the same time
    ind = numpy.random.randint(0,N_input, size = N_signals)			           #Choose randomly which neuron fires at each time

    #Repeat the pattern
    indices = ind
    times = tim

    for l in range(N_reps):
    	times = numpy.hstack((times,tim+(1+l)*10*N_duration))
    	indices = numpy.hstack((indices,ind))
    indices += 2 #shift indices by 2 reserve the first two neurons for the teacher

    teacher_e_tim = []
    teach_mem = 0
    for timestep in range(N_duration*10):
        teach_mem += (N_signals_teacher*2/(N_duration*10))*(numpy.sin(numpy.pi*2/(10*N_duration)*timestep)+1)*0.5
        if teach_mem >= 1:
            teach_mem -= 1
            teacher_e_tim.append(timestep)

    teacher_i_tim = numpy.linspace(start=0, stop=N_duration*10, num=len(teacher_e_tim), dtype=int)

    teacher_e_tim = numpy.array(teacher_e_tim)

    teacher_i_times=numpy.array([])
    teacher_e_times=numpy.array([])

    if not disable_teacher:
        for l in range(prerep,N_reps-postrep):
        
            teacher_i_times = numpy.hstack((teacher_i_times,teacher_i_tim+((1+l)*10*N_duration)))
            teacher_e_times = numpy.hstack((teacher_e_times,teacher_e_tim+((1+l)*10*N_duration)))

    start_validation = (N_reps-postrep)*1000*N_duration
    end_baseline = (prerep)*1000*N_duration

    ## convert to us

    times = times*100
    teacher_e_times = teacher_e_times*100
    teacher_i_times = teacher_i_times*100

    spike_array = numpy.stack((times,indices),axis=-1)
    spike_array = numpy.append(spike_array,numpy.stack((teacher_e_times,numpy.full(teacher_e_times.shape,1,dtype=int)),axis=-1),axis=0)
    spike_array = numpy.append(spike_array,numpy.stack((teacher_i_times,numpy.full(teacher_i_times.shape,0,dtype=int)),axis=-1),axis=0)

    return (spike_array[spike_array[:,0].argsort()],None,start_validation,end_baseline,N_duration*1000*N_reps)



def wave_regression_2s(disable_teacher=False):
    multtime=12
    prerep=2
    postrep=3
    N_duration = 2000
    N_reps = multtime+prerep+postrep

    #Neurons generating a stochastic, repeating input signal - each is connected to the neuron of interest with one synapse
    numpy.random.seed(2)                                                              #seed for pseudo-randomness 

    N_signals = 5120    #total number of input spikes per period
    N_signals_teacher = N_signals/4	 # number for exc and inh teacher		                                            
    N_input_exc = 32	
    N_input_inh = 32	
    N_input = N_input_exc+N_input_inh			                                             #number of input synapses
     			                                                   #period of the signal (in ms)
                                                 #number of repetitions of the signal -1 also defind below


    #Generate random pattern - one timestep is 0.1ms, i.e. 10 elements per ms
    tim = numpy.random.choice(10*N_duration,N_signals,replace = False)	           #Choose <N_signals> random times at which a neuron fires, each time occurs only once to avoid that one neuron fires twice at the same time
    ind = numpy.random.randint(0,N_input, size = N_signals)			           #Choose randomly which neuron fires at each time

    #Repeat the pattern
    indices = ind
    times = tim

    for l in range(N_reps):
    	times = numpy.hstack((times,tim+(1+l)*10*N_duration))
    	indices = numpy.hstack((indices,ind))
    indices += 2 #shift indices by 2 reserve the first two neurons for the teacher

    teacher_e_tim = []
    teach_mem = 0
    for timestep in range(N_duration*10):
        teach_mem += (N_signals_teacher*2/(N_duration*10))*(numpy.sin(numpy.pi*2/(10*N_duration)*timestep)+1)*0.5
        if teach_mem >= 1:
            teach_mem -= 1
            teacher_e_tim.append(timestep)

    teacher_i_tim = numpy.linspace(start=0, stop=N_duration*10, num=len(teacher_e_tim), dtype=int)

    teacher_e_tim = numpy.array(teacher_e_tim)

    teacher_i_times=numpy.array([])
    teacher_e_times=numpy.array([])

    if not disable_teacher:
        for l in range(prerep,N_reps-postrep):
        
            teacher_i_times = numpy.hstack((teacher_i_times,teacher_i_tim+((1+l)*10*N_duration)))
            teacher_e_times = numpy.hstack((teacher_e_times,teacher_e_tim+((1+l)*10*N_duration)))

    start_validation = (N_reps-postrep)*1000*N_duration
    end_baseline = (prerep)*1000*N_duration

    ## convert to us

    times = times*100
    teacher_e_times = teacher_e_times*100
    teacher_i_times = teacher_i_times*100

    spike_array = numpy.stack((times,indices),axis=-1)
    spike_array = numpy.append(spike_array,numpy.stack((teacher_e_times,numpy.full(teacher_e_times.shape,1,dtype=int)),axis=-1),axis=0)
    spike_array = numpy.append(spike_array,numpy.stack((teacher_i_times,numpy.full(teacher_i_times.shape,0,dtype=int)),axis=-1),axis=0)

    return (spike_array[spike_array[:,0].argsort()],None,start_validation,end_baseline,N_duration*1000*N_reps)