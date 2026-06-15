import numpy
import logging


logging.basicConfig(level=logging.INFO)

def wdbc():

    N_sets = 5
    N_epochs = 2
    T_wait_between_epochs = 0
    N_validation_blocks = 1 # not implemented
    N_duration = 500 # in ms
    #N_signals = 512    #total number of input spikes per period
    N_signals_syn = 30 # max spikes per synapse in duration
    N_signals_teacher = 120	 # max spikes for exc teacher in duration


    N_duration_us = N_duration*1000

    numpy.random.seed(2) 

    wdbc = numpy.genfromtxt('dataset/wdbc.data', delimiter=',')

    wdbc_normed = (wdbc - wdbc.min(axis=0)) / (wdbc - wdbc.min(axis=0)).max(axis=0)

    numpy.random.shuffle(wdbc_normed)

    split_points = numpy.linspace(start=0,stop=wdbc_normed.shape[0], num=N_sets+1,dtype=int)

    sets = []
    for i in range(N_sets):
        sets.append(wdbc_normed[split_points[i]:split_points[i+1]-1])
    print(len(sets))
    print(sets[0].shape)

    def set_shuffle_to_sorted_spiketrain(input_set, start_time_us,validation=False):
        numpy.random.shuffle(input_set)
        spike_array = numpy.zeros((0,2),dtype=int)
        label_array = numpy.zeros((0,2),dtype=int)
        for i in range(input_set.shape[0]):
            tmp_label = numpy.empty((1,2),dtype=int)
            tmp_label[0][0] = start_time_us
            tmp_label[0][1] = input_set[i][1]
            label_array = numpy.append(label_array,tmp_label,axis=0)
            if not validation:
                # inhbitory teacher set to the middle op on and off
                tmp_times = (numpy.linspace(start=start_time_us,stop=start_time_us+N_duration_us,num=int(N_signals_teacher/2)+1,endpoint=False,dtype=int))[1::]
                tmp_ids = numpy.full(tmp_times.shape,0,dtype=int)
                tmp_array = numpy.stack((tmp_times,tmp_ids),axis=-1)
                spike_array = numpy.append(spike_array,tmp_array,axis=0)
                # exitatory teacher
                tmp_times = (numpy.linspace(start=start_time_us,stop=start_time_us+N_duration_us,num=int(N_signals_syn*input_set[i][1])+1,endpoint=False,dtype=int))[1::]
                tmp_ids = numpy.full(tmp_times.shape,1,dtype=int)
                spike_array = numpy.append(spike_array,numpy.stack((tmp_times,tmp_ids),axis=-1),axis=0)
            for j in range(2,input_set.shape[1]):
                tmp_times = (numpy.linspace(start=start_time_us,stop=start_time_us+N_duration_us,num=int(N_signals_syn*input_set[i][j])+1,endpoint=False,dtype=int))[1::]
                tmp_ids = numpy.full(tmp_times.shape,j,dtype=int)
                spike_array = numpy.append(spike_array,numpy.stack((tmp_times,tmp_ids),axis=-1),axis=0)
            start_time_us += N_duration_us
        return (spike_array[spike_array[:,0].argsort()],start_time_us+N_duration_us,label_array)
    
    spiketrain_set = []
    for i in range(N_sets):
        logging.info("started set "+str(i))
        validation_set = sets[i]
        test_set = numpy.zeros((0,sets[i].shape[1]),dtype=int)
        for j in range(N_sets):
            if i != j:
                tmp_cutsets = sets[j]
                test_set = numpy.append(test_set,tmp_cutsets,axis=0)

        current_time = 0
        spike_array, current_time, label_array = set_shuffle_to_sorted_spiketrain(validation_set, current_time,validation=True)
        end_baseline = current_time
        for j in range(N_epochs):
            logging.info("started epoch "+str(j)+" of set "+str(i))
            current_time += T_wait_between_epochs
            tmp_spike_array, current_time, tmp_label_array = set_shuffle_to_sorted_spiketrain(test_set, current_time)
            spike_array = numpy.append(spike_array, tmp_spike_array, axis=0)
            label_array = numpy.append(label_array, tmp_label_array, axis=0)
        current_time += T_wait_between_epochs
        start_validation = current_time
        tmp_spike_array, current_time,tmp_label_array = set_shuffle_to_sorted_spiketrain(validation_set, current_time,validation=True)
        spike_array = numpy.append(spike_array, tmp_spike_array, axis=0)
        label_array = numpy.append(label_array, tmp_label_array, axis=0)
        spiketrain_set.append((spike_array,label_array,start_validation,end_baseline,current_time))

    logging.info("Dataset: WDBC \n number of sets:" +str(N_sets)+
                "\n sample exposure time [sec]: "+str(N_duration_us/1000000)+
                "\n set start training [msec]: "+str(spiketrain_set[0][3]/1000)+
                "\n set start validation [msec]: "+str(spiketrain_set[0][2]/1000)+
                "\n total runtime per set [sec]: "+str(spiketrain_set[0][4]/1000000)
                )      
    return spiketrain_set














