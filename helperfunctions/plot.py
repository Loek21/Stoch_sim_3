import matplotlib.pyplot as plt
import csv

def reader(filename):
    conv_list = []
    with open(filename, "r") as f:
        reader=csv.reader(f)
        for row in reader:
            if len(row) > 0:
                conv_list.append(int(row[0]))
    return conv_list

geom_cool_list = reader("../geom_cool.csv")
lin_cool_list = reader("../lin_cool_04.csv")
log_cool_list = reader("../log_cool.csv")

plt.boxplot([geom_cool_list, lin_cool_list, log_cool_list])
plt.show()
