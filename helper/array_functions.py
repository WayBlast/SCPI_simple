from Generate_pattern_DPSS_2DE import *
from uC_api import *
import numpy

def cycle_through_synapses(uc, neuron=0, start_time=0, step=1000):
    for branch in range(0,2):
        for synapse in range(0,31):
            # set everything to zero
            for nr in range(0,6):
                parameters_config_2[nr]['par'] = 0
            for nr in range(0,12):
                parameters_config_3[nr]['par'] = 0
            for nr in range(0,12):
                parameters_config_4[nr]['par'] = 0
            parameters_config_5[0]['par'] = 0
            # set synapse
            if synapse == 0: parameters_config_2[5]['par'] = 1
            elif synapse == 1: parameters_config_2[4]['par'] = 1
            elif synapse == 2: parameters_config_2[3]['par'] = 1
            elif synapse == 3: parameters_config_2[2]['par'] = 1
            elif synapse == 4: parameters_config_2[1]['par'] = 1
            elif synapse == 5: parameters_config_2[0]['par'] = 1
            elif synapse == 6: parameters_config_3[11]['par'] = 1
            elif synapse == 7: parameters_config_3[10]['par'] = 1
            elif synapse == 8: parameters_config_3[9]['par'] = 1
            elif synapse == 9: parameters_config_3[8]['par'] = 1
            elif synapse == 10: parameters_config_3[7]['par'] = 1
            elif synapse == 11: parameters_config_3[6]['par'] = 1
            elif synapse == 12: parameters_config_3[5]['par'] = 1
            elif synapse == 13: parameters_config_3[4]['par'] = 1
            elif synapse == 14: parameters_config_3[3]['par'] = 1
            elif synapse == 15: parameters_config_3[2]['par'] = 1
            elif synapse == 16: parameters_config_3[1]['par'] = 1
            elif synapse == 17: parameters_config_3[0]['par'] = 1
            elif synapse == 18: parameters_config_4[11]['par'] = 1
            elif synapse == 19: parameters_config_4[10]['par'] = 1
            elif synapse == 20: parameters_config_4[9]['par'] = 1
            elif synapse == 21: parameters_config_4[8]['par'] = 1
            elif synapse == 22: parameters_config_4[7]['par'] = 1
            elif synapse == 23: parameters_config_4[6]['par'] = 1
            elif synapse == 24: parameters_config_4[5]['par'] = 1
            elif synapse == 25: parameters_config_4[4]['par'] = 1
            elif synapse == 26: parameters_config_4[3]['par'] = 1
            elif synapse == 27: parameters_config_4[2]['par'] = 1
            elif synapse == 28: parameters_config_4[1]['par'] = 1
            elif synapse == 29: parameters_config_4[0]['par'] = 1
            elif synapse == 30: parameters_config_5[0]['par'] = 1

            if branch == 0:
                parameters_config_0[10]['par'] = 1
                parameters_config_0[11]['par'] = 0
            else:
                parameters_config_0[10]['par'] = 0
                parameters_config_0[11]['par'] = 1

            if start_time == 0:
                send_fast_config(uc, time=0)
                sleep(.075)
            else:
                send_fast_config(uc, time=start_time+step*synapse+(step*branch*32))
            
            

def init_dpss_weights(uc, neuron=0, start_time=0, times=1000, step=5000, force_1=False, force_0=False):
    numpy.random.seed(2)
    if force_1:
        branch1=[*range(0,31)]
        branch2=[*range(0,31)]
    elif force_0:
        branch1=[]
        branch2=[]
    else:
        branch1=numpy.random.choice(30,size=15,replace=False)
        branch2=numpy.random.choice(30,size=15,replace=False)
    print("branch1: " + str(branch1))
    print("branch2: " + str(branch2))
    branch1_inv = []
    branch2_inv = []
    for synapse in range(0,31):
        if synapse not in branch1:
            branch1_inv.append(synapse)
        if synapse not in branch2:
            branch2_inv.append(synapse)
    # potentiate 
    for time in range(1+start_time,times*step+start_time,step):
        uc.async_to_chip[0].send(word=packet_address(synapse=0,neuron=neuron,synapse_type="exc_static"), time = time)
        for synapse in branch1:
            uc.async_to_chip[0].send(word=packet_address(synapse=synapse,neuron=neuron,synapse_type="exc_dynamic"), time = time)
        for synapse in branch2:
            uc.async_to_chip[0].send(word=packet_address(synapse=synapse,neuron=neuron,synapse_type="inh_dynamic"), time = time)
        for nb in range(0,30):
            uc.async_to_chip[0].send(word=packet_address(synapse=0,neuron=neuron,synapse_type="exc_static"), time = int(time+nb*step/30))
    # depress
    for time in range(times*step+start_time,times*step*2+start_time,step):
        uc.async_to_chip[0].send(word=packet_address(synapse=0,neuron=neuron,synapse_type="inh_static"), time = time)
        for synapse in branch1_inv:
            uc.async_to_chip[0].send(word=packet_address(synapse=synapse,neuron=neuron,synapse_type="exc_dynamic"), time = time)
        for synapse in branch2_inv:
            uc.async_to_chip[0].send(word=packet_address(synapse=synapse,neuron=neuron,synapse_type="inh_dynamic"), time = time)
        for nb in range(0,30):
            uc.async_to_chip[0].send(word=packet_address(synapse=0,neuron=neuron,synapse_type="inh_static"), time = int(time+nb*step/30))

    return times*step*2+start_time



def reset_async(uc,time=0):
    if time != 0:
        uc.pin[19].send(value=0, time=time)
        uc.pin[20].send(value=0, time=time+100)
        uc.pin[20].send(value=1, time=time+200)
        uc.pin[19].send(value=1, time=time+300)
    else:
        uc.pin[19].send(value=0)     
        uc.pin[20].send(value=0)
        sleep(0.1)
        uc.pin[20].send(value=1)
        uc.pin[19].send(value=1)
    logging.info("reset async at time " + str(time))

def send_dac_config(uc,sweep=0,time=0):
    if time != 0:
        uc.pin[0].send(value=1, time=time)
        for word in create_SPI0_input(sweep):
            uc.spi[1].send(word, time=time+100)
        uc.pin[0].send(value=0, time=time+300)
    else:
        uc.pin[0].send(value=1)
        sleep(0.1)
        number_of_bytes_send = 0
        for word in create_SPI0_input(sweep):
            number_of_bytes_send += 1
            uc.spi[1].send(word)
        sleep(0.1)
        uc.pin[0].send(value=0)
        logging.info("number of bytes send on dac fifo: " + str(number_of_bytes_send))

def send_fast_config(uc,sweep=0,time=0):
    if time != 0:
        uc.pin[10].send(value=1, time=time)
        for word in create_SPI1_input():
            uc.spi[0].send(word, time=time+100)
        uc.pin[10].send(value=0, time=time+300)
    else:
        uc.pin[10].send(value=1)
        sleep(0.1)
        number_of_bytes_send = 0
        for word in create_SPI1_input():
            number_of_bytes_send += 1
            uc.spi[0].send(word)
        sleep(0.1)
        uc.pin[10].send(value=0)
        logging.info("number of bytes send on fast fifo: " + str(number_of_bytes_send))

def packet_address(synapse_type="exc_static", synapse=0, neuron=0):
    synapse= int(synapse)
    neuron= int(neuron)

    if neuron > 15:
        Warning("invalid neuron id - 0 is used")
        neuron = 0  

    # c2f neurons do not have input and are skipt in the input encoding
    if neuron >= 12:
        neuron = neuron - 4

    if synapse_type == "exc_static" or synapse_type == "inh_static":
        if synapse != 0:
            Warning("invalid synapse id - 0 is used")
            synapse = 0

    elif synapse_type == "exc_dynamic" or synapse_type == "inh_dynamic":
        if synapse > 30 and neuron < 8:
            Warning("invalid synapse id - 0 is used")
            synapse = 0  
        elif synapse > 14 and neuron >= 8:
            Warning("invalid synapse id - 0 is used")
            synapse = 0  
    
        # on BCall on every second syn is connected
        if neuron >= 8:
            synapse = synapse*2
        # shift static synapse away
        synapse = synapse + 1
    else:
        Warning("wrong synapse type")
    # each neuron has 2 syn rows
    neuron = neuron*2

    if synapse_type == "exc_dynamic" or synapse_type == "exc_static":
        neuron = neuron + 1
    
    #print("synapse address " + str((neuron<<5) + synapse) + " n " + str(neuron) + " s " + str(synapse))
    return int((neuron<<5) + synapse)

def setup(uc):
    # reset
    #uc.pin[31].activate("OUTPUT")  -> Old setup
    #uc.pin[32].activate("OUTPUT")  -> Old setup
    uc.pin[19].activate("OUTPUT")
    uc.pin[20].activate("OUTPUT")
    uc.pin[21].activate("OUTPUT")
    uc.pin[22].activate("OUTPUT")
    uc.pin[23].activate("OUTPUT")
    uc.pin[21].send(0)      # MUX config
    uc.pin[22].send(1)      # MUX config
    uc.pin[23].send(1)      # MUX config (0 1 1 = 6, binary but reversed order)

    #fifo dac
    uc.spi[1].activate(mode="SPI_MODE0", speed_class=2, order="LSBFIRST", number_of_bytes=1)
    uc.pin[0].activate("OUTPUT")

    #fifo fast
    uc.spi[0].activate(mode="SPI_MODE0", speed_class=2, order="LSBFIRST", number_of_bytes=1)
    uc.pin[10].activate("OUTPUT")

    # aer
    uc.async_to_chip[0].activate(req_pin=41, ack_pin=2, data_width=10, data_pins=[28, 30, 31, 34, 35, 36, 37, 38, 39, 40], mode="4Phase_Chigh_Dhigh", req_delay = 0)
    uc.async_from_chip[0].activate(req_pin=5, ack_pin=18, data_width=4, data_pins=[6, 7, 8, 9], mode="4Phase_Chigh_Dhigh", req_delay = 0)

    #async reset
    sleep(1)
    reset_async(uc)


def create_AER_input_from_dataset(uc, dataset, validation_t, end_baseline_t, end_t, label_array=None, mode_pin=30, label_pin=29, target_neuron=0):
    id_max = dataset[:,1].max(axis=0)
    logging.info("max id: " + str(id_max))
    uc.pin[mode_pin].send(value=1, time=1)
    label_number = 0
    tmp_baseline = False
    tmp_validation = False
    for i in range(dataset.shape[0]):
        if dataset[i][0] >= end_baseline_t and not tmp_baseline:
            tmp_baseline = True
            uc.pin[mode_pin].send(value=0, time=end_baseline_t)
        elif dataset[i][0] >= validation_t and not tmp_validation:
            tmp_validation = True
            uc.pin[mode_pin].send(value=1, time=validation_t)

        if label_array is not None and dataset[i][0] >= label_array[label_number][0]:
            uc.pin[label_pin].send(value=int(label_array[label_number][1]), time=int(label_array[label_number][0]))

        if dataset[i][1] == 0:
            # Send spike
            uc.async_to_chip[0].send(word=packet_address(synapse=0,neuron=target_neuron,synapse_type="inh_static"), time = int(dataset[i][0])) # Time stamps must be ordered - Specifies microsends from experiment start to send spike
        elif dataset[i][1] == 1:
            uc.async_to_chip[0].send(word=packet_address(synapse=0,neuron=target_neuron,synapse_type="exc_static"), time = int(dataset[i][0])) # THESE TWO NEED TO BE IMPLEMENTED IN NEW FUNCTION
        elif id_max <= 33:
            uc.async_to_chip[0].send(word=packet_address(synapse=dataset[i][1]-2,neuron=target_neuron,synapse_type="exc_dynamic"), time = int(dataset[i][0]))
            uc.async_to_chip[0].send(word=packet_address(synapse=dataset[i][1]-2,neuron=target_neuron,synapse_type="inh_dynamic"), time = int(dataset[i][0]))
        elif dataset[i][1] <= 33:
            uc.async_to_chip[0].send(word=packet_address(synapse=dataset[i][1]-2,neuron=target_neuron,synapse_type="inh_dynamic"), time = int(dataset[i][0]))
        elif dataset[i][1] <= 66:
            uc.async_to_chip[0].send(word=packet_address(synapse=dataset[i][1]-34,neuron=target_neuron,synapse_type="exc_dynamic"), time = int(dataset[i][0]))
    uc.pin[mode_pin].send(value=0, time=end_t)

def create_AER_input_simple(uc, dataset, validation_t, end_baseline_t, end_t, label_array=None, mode_pin=30, label_pin=29, target_neuron=0, expression = "exc"):
    id_max = dataset[:,1].max(axis=0)
    logging.info("max id: " + str(id_max))
    uc.pin[mode_pin].send(value=1, time=1)
    label_number = 0
    tmp_baseline = False
    tmp_validation = False

    if expression == "inh":     
        for i in range(dataset.shape[0]):
            if dataset[i][0] >= end_baseline_t and not tmp_baseline:
                tmp_baseline = True
                uc.pin[mode_pin].send(value=0, time=end_baseline_t)
            elif dataset[i][0] >= validation_t and not tmp_validation:
                tmp_validation = True
                uc.pin[mode_pin].send(value=1, time=validation_t)

            if label_array is not None and dataset[i][0] >= label_array[label_number][0]:
                    uc.pin[label_pin].send(value=int(label_array[label_number][1]), time=int(label_array[label_number][0]))

            uc.async_to_chip[0].send(word=packet_address(synapse=0,neuron=target_neuron,synapse_type="inh_static"), time = int(dataset[i][0]))
    elif expression == "exc":
        for i in range(dataset.shape[0]):
            if dataset[i][0] >= end_baseline_t and not tmp_baseline:
                tmp_baseline = True
                uc.pin[mode_pin].send(value=0, time=end_baseline_t)
            elif dataset[i][0] >= validation_t and not tmp_validation:
                tmp_validation = True
                uc.pin[mode_pin].send(value=1, time=validation_t)

            if label_array is not None and dataset[i][0] >= label_array[label_number][0]:
                    uc.pin[label_pin].send(value=int(label_array[label_number][1]), time=int(label_array[label_number][0]))
            uc.async_to_chip[0].send(word=packet_address(synapse=0,neuron=target_neuron,synapse_type="exc_static"), time = int(dataset[i][0]))
    else:
        raise Exception("Expression type not defined - must be inhibitory or excitatory")


def generate_spikes(uc, freq, duration, target_neuron, regular=True, type="exc"):
    if type == "exc" or type == "inh":
        uc.pin[30].send(value=1, time=1)   # at start

        numpy.random.seed(2) 

        if regular:
            times_t = numpy.unique(numpy.linspace(start=1, stop=duration * 10, num=int(freq*(duration/1000)), dtype=int))
        else:
            times_t = numpy.unique(numpy.random.randint(low=1, high=duration * 10, size=int(freq*(duration/1000))))
        
        times_t = times_t*100
        
        for t in times_t:
            uc.async_to_chip[0].send(word=packet_address(synapse=0,neuron=6,synapse_type=f"{type}_static"), time = int(t))

        uc.pin[30].send(value=0, time=duration)
    else:
        raise Exception("Expression type not defined - must be inhibitory or excitatory")
    
    

    