import matplotlib.pyplot as plt
import csv
import numpy as np

def reader(filename):
    conv_list = []
    with open(filename, "r") as f:
        reader=csv.reader(f, delimiter=";")
        for row in reader:
            if len(row) > 0:
                conv_list.append(float(row[0]))
    return np.mean(conv_list), np.std(conv_list)

mean_10, std_10 = reader("../10_new.csv")
mean_100, std_100 = reader("../100_new.csv")
mean_1000, std_1000 = reader("../1000_new.csv")
mean_5000, std_5000 = reader("../5000_new.csv")
mean_10000, std_10000 = reader("../10000_new.csv")
mean_20000, std_20000 = reader("../20000_new.csv")
mean_list = np.array([mean_10, mean_100, mean_1000, mean_5000, mean_10000, mean_20000])
std_list = np.array([std_10, std_100, std_1000, std_5000, std_10000, std_20000])
x_list = [10,100,1000,5000,10000,20000]

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.semilogx(x_list, mean_list)
ax1.fill_between(x_list, mean_list-std_list, mean_list+std_list, alpha=0.5)
ax1.set_xlabel("Markov Chain length")
ax1.set_ylabel("Mean shortest traveling distance")
plt.show()
