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

def improvement_abs(baseline, value):
    return (1-value/baseline)

def improvement_abss(baseline, value, cur_l):
    return (1-value/baseline)/(cur_l)

mean_1, std_1 = reader("../1_new.csv")
mean_2, std_2 = reader("../2_new.csv")
mean_5, std_5 = reader("../5_new.csv")
mean_10, std_10 = reader("../10_new.csv")
mean_100, std_100 = reader("../100_new.csv")
mean_1000, std_1000 = reader("../1000_new.csv")
mean_5000, std_5000 = reader("../5000_new.csv")
mean_10000, std_10000 = reader("../10000_new.csv")
mean_20000, std_20000 = reader("../20000_new.csv")
mean_50000, std_50000 = reader("../50000_new.csv")
mean_list = np.array([mean_1, mean_2, mean_5, mean_10, mean_100, mean_1000, mean_5000, mean_10000, mean_20000, mean_50000])
std_list = np.array([std_1, std_2, std_5, std_10, std_100, std_1000, std_5000, std_10000, std_20000, std_50000])
x_list = [1,2,5,10,100,1000,5000,10000,20000,50000]

abs_improv = []
abs_improvs = []
for i in range(1,len(mean_list)):
    abs_improv.append(improvement_abs(mean_list[0], mean_list[i]))
    abs_improvs.append(improvement_abss(mean_list[0], mean_list[i], x_list[i]))

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.semilogx(x_list, mean_list)
ax1.fill_between(x_list, mean_list-std_list, mean_list+std_list, alpha=0.5)
ax1.set_xlabel("Markov Chain length")
ax1.set_ylabel("Mean shortest traveling distance")
ax1.grid()
plt.show()

fig = plt.figure()
ax2 = fig.add_subplot(1,1,1)
# ax2.semilogx(x_list[1:], abs_improv)
ax2.semilogx(x_list[1:], abs_improvs)
ax2.semilogx(x_list, log_list)
ax2.set_xlabel("Markov Chain length")
ax2.set_ylabel("Mean shortest traveling distance")
ax2.grid()
plt.show()
