"""
This file contains the functions needed for simulated annealing
"""
import numpy as np
import random
from copy import deepcopy
import csv

def get_length(config, entire):
    """Calculates the euclidean distance of a section or the entire chain (if entire is True), Returns the length of desired specs"""
    L = 0
    for i in range(len(config)-1):
        city_a = config[i][1:]
        city_b = config[i+1][1:]
        L += np.sqrt((city_a[0]-city_b[0])**2+(city_a[1]-city_b[1])**2)
    if entire == True:
        L += np.sqrt((config[0][1]-config[-1][1])**2+(config[0][2]-config[-1][2])**2)

    return L

def generate_seg(n):
    """Generates a list of segments over which the 2-opt operation is carried out, returns list of segments."""
    seg_list = []
    for i in range(n):
      for j in range(i+2, n):
        seg_list.append((i,j))

    return seg_list

def kick(config):
    """Kicks the current configuration of TSP by swapping 4 random nodes, returns disturbed configuration"""
    index_list = [i for i in range(len(config))]
    selection = random.sample(index_list, 4)
    select_a = config[selection[0]]
    select_b = config[selection[1]]
    select_c = config[selection[2]]
    select_d = config[selection[3]]
    config[selection[0]] = select_d
    config[selection[1]] = select_c
    config[selection[2]] = select_b
    config[selection[3]] = select_a

    return config

def reverse_if_better(config, i, j):
    """Performs the 2-opt operator of segments of the TSP configuration, makes changes if new distance is shorter"""
    a, b, c, d = config[i-1], config[i], config[j-1], config[j]

    # calculate distances of different permutations
    original = get_length([a,b], False) + get_length([c,d], False)
    perm = get_length([a,c], False) + get_length([b,d], False)

    # Applies changes if new distance is shorter than the old.
    if original > perm:
      config[i:j] = reversed(config[i:j])

    return config

def log_cool(T_init,t):
    """Logarithmic cooling scheme"""
    T = T_init/(1+np.log(1+t))
    return T

def geom_cool(T_init,t):
    """Geometric cooling scheme"""
    T_new = T_init*0.97**t
    return T_new

def lin_cool(T_init,t):
    """Linear cooling scheme"""
    T_new = T_init - t*1.9
    return T_new

def exp_cool(T_init,t, max_time):
    """Exponential cooling scheme"""
    T_new = T_init*np.e**(-t*np.log(2)/(0.25*max_time))
    return T_new

def simulated_annealing(cooling_method, coord_list, initial_time, max_time, initial_temperature):
    config_length = [get_length(coord_list, True)]
    markov_chain = [coord_list]
    delta_L_list = []
    T = initial_temperature

    # Takes the TSP configuration from the last entry in the MC
    seg_list = generate_seg(len(markov_chain[-1]))
    for i in range(max_time):
        candidate_coord_list = deepcopy(markov_chain[-1])

        # give a kick to the new candidate to change it from the last config and shuffles the segment list
        kick(candidate_coord_list)
        np.random.shuffle(seg_list)
        for segments in seg_list:

            # Performs 2-opt operator and saves the changes if it results in a lower total distance
            reverse_if_better(candidate_coord_list, segments[0], segments[1])

        # Calculates new lengths
        new_length = get_length(candidate_coord_list, True)

        # Calculates difference in length between current and previous entry
        delta_L = config_length[-1] - new_length

        # If new TSP configuration is better it is accepted 100% of the time
        if delta_L > 0:
            delta_L_list.append((config_length[-1], new_length))
            config_length.append(new_length)
            markov_chain.append(candidate_coord_list)

        else:
            # If the new one is longer it is accepted with a certain probability
            if np.random.uniform() < np.e**(delta_L/T):

                config_length.append(new_length)
                markov_chain.append(candidate_coord_list)
            else:
                markov_chain.append(markov_chain[-1])
                config_length.append(config_length[-1])

        # Cools the algorithm depending on the selected scheme
        T = cooling_method(initial_temperature, i)

    return markov_chain, config_length, delta_L_list

def read_inpt(filename):
    """Reads text files containing the TSP configurations and returns a list where each element looks as follows: (node nr, x, y)"""
    config = []
    f = open(f"configs/"+f"{filename}.txt", "r")
    skip_lines = f.readlines()[6:]
    for i in range(len(skip_lines)-1):
        line = skip_lines[i]
        nnl = line.replace("\n","")
        splitter = nnl.split(" ")
        for j in np.arange(len(splitter)-1,-1,-1):
            if len(splitter[j]) == 0:
                splitter.remove(splitter[j])
            else:
                splitter[j] = splitter[j].replace("'", "")
                splitter[j] = int(splitter[j])
        coord = (splitter[0],splitter[1], splitter[2])
        config.append(coord)

    return config

def T_init(delta_L, T_n, p_0, error):
    """Used to determine the initial temperature for the SA"""
    T_est = 10
    while abs(T_est - p_0) >= error:
        E_max = 0
        E_min = 0
        for i in range(1,len(delta_L)):
            E_max += np.exp(-(delta_L[i][0]/T_n))
            E_min += np.exp(-(delta_L[i][1]/T_n))
        T_est = E_max/E_min

        if abs(T_est - p_0) <= error:
            return T_n
        else:
            T_n = T_n*(np.log(T_est)/np.log(p_0))**(1/2)
