from helperfunctions.helperfunctions import *
import sys
import matplotlib.pyplot as plt
import numpy as np
import random
import csv


if __name__ == "__main__":
    coord_list = read_inpt('a280.tsp')

    for j in [10000]:
        for i in range(7):
            random.shuffle(coord_list)
            markov, length, delta_L_list = simulated_annealing(cooling_method=exp_cool, coord_list=coord_list, initial_time=1, \
                max_time=j, initial_temperature=200)
            with open(f"{j}_new2.csv", "a") as f:
                writer=csv.writer(f, delimiter=';')
                writer.writerow([np.min(length), length[-1]])
        # initial_T = T_init(delta_L_list, 200, 0.8, 0.01)
        # print(initial_T)

    # plt.plot(np.linspace(1,200,199), length[1:])
    # plt.show()
    #
    # for i in range(len(markov[-1])-1):
    #     x1, y1 = markov[-1][i][1], markov[-1][i][2]
    #     x2, y2 = markov[-1][i+1][1], markov[-1][i+1][2]
    #     plt.plot(x1, y1, 'bo')
    #     plt.plot(x2, y2, 'bo')
    #     plt.plot([x1, x2], [y1,y2], 'r-')
    # plt.show()
