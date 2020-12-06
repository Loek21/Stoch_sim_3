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
    markov_chain = [get_length(coord_list)]
    T = initial_temperature
    time = initial_time
    while time < max_time:
        new_coord_list = mutate(deepcopy(coord_list))
        new_length = get_length(new_coord_list)
        delta_L = markov_chain[-1] - new_length

        if delta_L > 0:
            coord_list = new_coord_list
            markov_chain.append(new_length)

        else:
            if np.random.uniform() < np.e**(delta_L/T):
                coord_list = new_coord_list
                markov_chain.append(new_length)
            else:
                markov_chain.append(markov_chain[-1])

        T = cooling_method(initial_temperature, time)
        time += 1

    return markov_chain

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
