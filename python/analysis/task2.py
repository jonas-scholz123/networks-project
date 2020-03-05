from tools import import_distributions, logbin, set_plot_defaults, make_cdf
set_plot_defaults()
import matplotlib.pyplot as plt
from scipy.special import comb
import numpy as np
dists = import_distributions("task2")

m_sorted_keys = sorted(dists, key = lambda x:x[1])
N_sorted_keys = sorted(dists, key = lambda x:x[0])

def theoretical_pdf(k, N, m):
    return 1/(m+1) * (m/(m+1))**k
    #return 1/m * ((1+m)/m)**(m-1)*(m/(1+m))**k

plot = "pdf"

for key in m_sorted_keys:
    N, m = key
    ks, ns = dists[(N, m)]
    ps = np.array(ns)/N
    #xs, ys = logbin(ks, scale = 1.2)
    #plt.loglog(xs, ys, "x", label = "m = " + str(m))


    if plot == "pdf":
        theoretical_k = np.linspace(0, max(ks), 1000)
        theoretical_p = np.array([theoretical_pdf(k, N, m) for k in theoretical_k])
        print(np.sum(ps))
        plt.semilogy()
        #log_ns = np.log10(ns)
        #log_theoretical_n = np.log10(theoretical_n)
        plt.plot(ks, ps, 'x')
        plt.plot(theoretical_k, theoretical_p, label = str(m))

    elif plot == "cdf":
        plt.xlim((-2, 70))
        dist = {k: ns[k] for k in ks}
        theoretical_dist = {k: theoretical_pdf(k, N, m) for k in ks}
        xs, ys = make_cdf(dist)
        theoretical_xs, theoretical_ys = make_cdf(theoretical_dist)
        plt.plot(xs, ys, "x", markersize = 10)
        plt.plot(theoretical_xs, theoretical_ys, "o")
plt.grid()
plt.xlabel(r"$k_{in}$")
plt.ylabel(r"$n(k_{in})$")
plt.legend()
plt.show()
