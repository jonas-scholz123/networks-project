from tools import import_max_degrees, logbin, set_plot_defaults, make_cdf
set_plot_defaults()
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kstest, anderson_ksamp

max_degrees_dict = import_max_degrees("task1")

m_sorted_keys = sorted(max_degrees_dict, key = lambda x:x[1])
N_sorted_keys = sorted(max_degrees_dict, key = lambda x:x[0])

for key in m_sorted_keys:
    N, m = key
    times, max_degrees = max_degrees_dict[(N, m)]

    print(times)

    plt.loglog(times, max_degrees, label = str(m))

plt.grid()
plt.legend()
plt.show()
