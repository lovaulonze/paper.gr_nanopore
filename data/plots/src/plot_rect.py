from utils import *
import numpy
import matplotlib.pyplot as plt
import os, os.path
from scipy.constants import pi, hbar, e
vf = 1.1e6

# Use C/m^2
def delta_phi_gr(sigma):
    fac = hbar * vf / e * numpy.sqrt(pi * numpy.abs(sigma) / e)
    return fac * numpy.sign(sigma)

pixels = (512, 512)

quantities = ("V", "c_p", "c_n", "zflux_cp", "zflux_cn")
units = ("V", "mol/m$^{3}$", "mol/m$^{3}$", "mol/(m$^{2}$*s)", "mol/(m$^{2}$*s)")

Vg_all = [0.001, 0.025, 0.05, 0.1, 0.15, 0.2] + list(numpy.arange(0.25, 1.35, 0.1))

Vg_true = []

file_template = "{0}.npy"
sigma_file_template = "sigma_{0}.txt"

concentrations = (0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1)

ratio_conc = 10**3

out_path = "../result/concentration/1D/"
plot_path = "../plot/concentration/1D/"

# get the index of column in the new matrix
def get_col_index(Vg, quantity):
    idx_V = Vg_all.index(Vg)
    idx_quant = quantities.index(quantity)
    len_quant = len(quantities)
    return 1 + len_quant * idx_V + idx_quant


avg_tflux = []

quant_flux = ("zflux_cp", "zflux_cn")

plt.style.use("science")
fig = plt.figure(figsize=(4, 4))
for conc in concentrations:
    tflux = []
    file_name = os.path.join(out_path, file_template.format(conc))
    data = numpy.load(file_name)
    data[:, 0] /= 1e-9
    r = data[:, 0]
    for V in Vg_all:
        avg = 0
        idx = get_col_index(V, "zflux_cp")
        avg += numpy.abs(numpy.mean(data[:, idx]))
        idx = get_col_index(V, "zflux_cn")
        avg += numpy.abs(numpy.mean(data[:, idx]))
        tflux.append(avg)
    avg_tflux.append(tflux)
    # correction for Vg
    sigma_file = os.path.join(out_path, sigma_file_template.format(conc))
    sigma_data = numpy.genfromtxt(sigma_file, comments="%")
    V_ = sigma_data[:, 0]; sig_ = -sigma_data[:, 1]
    Vg_true.append(V_ + delta_phi_gr(sig_))

avg_tflux = numpy.array(avg_tflux)

fig = plt.figure(figsize=(4, 4))
plt.style.use("science")

for i, conc in enumerate(concentrations):
    plt.plot(Vg_true[i], avg_tflux[i, :], "-o",
             markersize=5,
             label="{} mol/L$^3$".format(conc))

plt.yscale("log")
plt.xlabel("True $V_{g}$ (V)")
plt.xlim(0, 1.25)
plt.ylabel("Average total flux (mol/(m$^{-2}$*s))")
plt.legend()

plt.savefig(os.path.join(plot_path, "rect_Vg.pdf"))


d_debye = Debye_length(numpy.array(concentrations)) / 1e-9
rect = 1 - avg_tflux[:, 7] / avg_tflux[:, 0]

plt.figure(figsize=(4, 4))
plt.plot(d_debye, rect, "-s", markersize=5)
plt.xlabel("Debye Length (nm)")
plt.ylabel("Rectification ratio")
plt.savefig(os.path.join(plot_path, "rect_debye.pdf"))

    
    
    
    
    