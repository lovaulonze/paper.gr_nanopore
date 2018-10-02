import numpy
import matplotlib.pyplot as plt

file_templ = "../data/rect_{}_conc.csv"
def read(name):
    file_name = file_templ.format(name)
    err = None
    with open(file_name) as f:
        err = float(f.readline().strip())
    data = numpy.genfromtxt(file_name,
                            skip_header=1,
                            delimiter=",")
    return data, err

import sys
try:
    name = sys.argv[1]
except IndexError:
    name = "KCl"

fig = plt.style.use("science")
plt.figure(figsize=(2.8, 2.1), facecolor="w")
# plt.axvline(x=0, ls="--", color="#00ffee")
data, err = read(name)
plt.errorbar(data[:, 0], data[:, 1], yerr=err / 2, fmt="o")
xx = numpy.logspace(-4.2, -1)
yy = 0.0014 * xx ** -0.587
plt.plot(xx, yy, "--")
plt.xscale("log")
plt.xlabel("KCl concentration (mol/L)")
plt.ylabel("Rectification")
plt.savefig("../img/rect_{}_conc.svg".format(name))
