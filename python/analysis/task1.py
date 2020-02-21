from tools import import_distributions, logbin, set_plot_defaults
set_plot_defaults()
import matplotlib.pyplot as plt

dists = import_distributions("task1")

m_sorted_keys = sorted(dists, key = lambda x:x[1])
N_sorted_keys = sorted(dists, key = lambda x:x[0])

for key in m_sorted_keys:
    N, m = key
    vertices, ks = dists[(N, m)]
    xs, ys = logbin(ks, scale = 1.2)
    plt.loglog(xs, ys, "x", label = "m = " + str(m))
plt.grid()
plt.legend()
plt.show()
