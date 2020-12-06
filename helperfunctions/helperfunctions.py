"""
This file contains the functions needed for simulated annealing
"""
import numpy as np
import random
from copy import deepcopy
import csv

def get_length(config):
    L = 0
    for i in range(len(config)-1):
        city_a = config[i][1:]
        city_b = config[i+1][1:]
        L += np.sqrt((city_a[0]-city_b[0])**2+(city_a[1]-city_b[1])**2)

    return L

def generate_seg(n):

    seg_list = []
    for i in range(n):
      for j in range(i+2, n):
        seg_list.append((i,j))

    return seg_list

def mutate(config):
    index_list = [i for i in range(len(config))]
    selection = random.sample(index_list, 2)
    select_a = config[selection[0]]
    select_b = config[selection[1]]
    config[selection[0]] = select_b
    config[selection[1]] = select_a

    return config

def kick(config):
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

    a, b, c, d = config[i-1], config[i], config[j-1], config[j]

    # calculate distances of different permutations
    original = get_length([a,b]) + get_length([c,d])
    perm = get_length([a,c]) + get_length([b,d])

    if original > perm:
      config[i:j] = reversed(config[i:j])

    return config

def log_cool(T_init,t):
    T = T_init/(1+np.log(1+t))
    return T

def geom_cool(T_init,t):
    T_new = T_init*0.99**t
    return T_new

def lin_cool(T_init,t):
    T_new = T_init - t*0.01
    return T_new

def simulated_annealing(cooling_method, coord_list, initial_time, max_time, initial_temperature):
    config_length = [get_length(coord_list)]
    markov_chain = [coord_list]
    delta_L_list = []
    T = initial_temperature
    time = initial_time
    seg_list = generate_seg(len(markov_chain[-1]))
    while config_length[-1] > 2850:
        candidate_coord_list = deepcopy(markov_chain[-1])

        # give a kick to the new candidate to change it from the last config
        # print(get_length(candidate_coord_list))
        kick(candidate_coord_list)
        # print(get_length(candidate_coord_list))
        np.random.shuffle(seg_list)
        for segments in seg_list:
            reverse_if_better(candidate_coord_list, segments[0], segments[1])
        new_length = get_length(candidate_coord_list)
        delta_L = config_length[-1] - new_length

        if delta_L > 0:
            delta_L_list.append((config_length[-1], new_length))
            config_length.append(new_length)
            markov_chain.append(candidate_coord_list)

        else:
            # print(f"time: {time}, chance: {np.e**(delta_L/T)}")
            if np.random.uniform() < np.e**(delta_L/T):

                config_length.append(new_length)
                markov_chain.append(candidate_coord_list)
            else:
                markov_chain.append(markov_chain[-1])
                config_length.append(config_length[-1])

        T = cooling_method(initial_temperature, time)
        time += 1
    return markov_chain, config_length, delta_L_list

def read_inpt(filename):
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
    T_est = 10
    while abs(T_est - p_0) >= error:
        # print(T_n)
        E_max = 0
        E_min = 0
        for i in range(1,len(delta_L)):
            E_max += np.exp(-(delta_L[i][0]/T_n))
            E_min += np.exp(-(delta_L[i][1]/T_n))
        T_est = E_max/E_min
        # print(T_est)
        if abs(T_est - p_0) <= error:
            return T_n
        else:
            # print(np.log(T_est))
            # print(np.log(p_0))
            T_n = T_n*(np.log(T_est)/np.log(p_0))**(1/2)
