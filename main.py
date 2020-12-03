from helperfunctions.helperfunctions import *
import sys
import matplotlib.pyplot as plt
import numpy as np
import random


if __name__ == "__main__":
    coord_list = read_inpt('a280.tsp')
    random.shuffle(coord_list)
    
    markov = simulated_annealing(cooling_method=log_cool, coord_list=coord_list, initial_time=1, \
        max_time=5000, initial_temperature=200)
    print(markov)

    plt.plot(np.linspace(0,5000,5000), markov)
    plt.show()


