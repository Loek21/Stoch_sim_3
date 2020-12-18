from helperfunctions.helperfunctions import *
import sys
import matplotlib.pyplot as plt
import numpy as np
import random
import csv
from datetime import datetime


if __name__ == "__main__":
    coord_list = read_inpt('a280.tsp')

    # The length of the MC is j
    # for j in [1,2,5,10,100,1000,5000,10000,20000,50000]:
    h = 1
    for method in [lin_cool, geom_cool, log_cool]:
        # Each MC length is performed 100 times
        for i in range(100):
            random.shuffle(coord_list)

            markov, length, delta_L_list = simulated_annealing(cooling_method=method, coord_list=coord_list, initial_time=1, \
                max_time=100, initial_temperature=200)

            with open(f"{h}.csv", "a") as f:
                writer=csv.writer(f, delimiter=';')
                writer.writerow([np.min(length), length[-1]])
        h += 1
        # Used once to calculate the initial temperature
        # initial_T = T_init(delta_L_list, 200, 0.8, 0.01)



    # Used to plot the route
    # for i in range(len(markov[-1])-1):
    #     x1, y1 = markov[-1][i][1], markov[-1][i][2]
    #     x2, y2 = markov[-1][i+1][1], markov[-1][i+1][2]
    #     plt.plot(x1, y1, 'bo')
    #     plt.plot(x2, y2, 'bo')
    #     plt.plot([x1, x2], [y1,y2], 'r-')
    # plt.show()
