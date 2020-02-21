from tools import import_distributions, logbin, set_plot_defaults
set_plot_defaults()
import matplotlib.pyplot as plt

dists = import_distributions("task3")

N_sorted_keys = sorted(dists, key = lambda x:x[0])
m_sorted_keys = sorted(dists, key = lambda x:x[1])
q_sorted_keys = sorted(dists, key = lambda x:x[2])

for key in q_sorted_keys:
    N, m, q= key
    vertices, ks = dists[key]
    xs, ys = logbin(ks, scale = 1.2)
    plt.loglog(xs, ys, "x", label = "q = " + str(q))
plt.grid()
plt.legend()
plt.show()
