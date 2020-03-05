from tools import import_distributions, logbin, set_plot_defaults, make_cdf
set_plot_defaults()
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kstest, anderson_ksamp



def theoretical_pdf(k, m):
    #if k < 0:
        #return 0
    return 2*(m+1)*m * 1/((k+m+2)*(k+m+1)*(k+m))
# logbin approach:

#for key in m_sorted_keys:
#    N, m = key
#    vertices, ks = dists[(N, m)]
#    #xs, ys = logbin(ks, scale = 1.2)
#    plt.loglog(vertices, ks, "x", label = "m = " + str(m))
#    #fit_x = np.linspace(0, 1000, 1000)
#    fit_y = theoretical_pdf(xs, m)
#    plt.loglog(xs, fit_y)


# cdf approach:

def task1_degree_analysis(show_plots = True, show_stats_results = True):

    dists = import_distributions("task1")

    m_sorted_keys = sorted(dists, key = lambda x:x[1])
    #N_sorted_keys = sorted(dists, key = lambda x:x[0])

    ax, (fig1, fig2) = plt.subplots(1, 2)
    colour_counter = 0
    for key in m_sorted_keys:
        N, m = key
        ks, ns = dists[(N, m)]

        dist = {k: ns[k] for k in ks}
        #theoretical_dist = {k: theoretical_pdf(k, m) for k in np.linspace(min(ks), max(ks), 1000)}
        theoretical_dist = {k: theoretical_pdf(k, m) for k in ks}

        xs, ys = make_cdf(dist)
        fit_xs, fit_ys = make_cdf(theoretical_dist)

        if show_plots:
            colour = "C"+str(colour_counter)
            fig2.loglog(xs, ys, colour + "x", label = "m = " + str(m), markersize = 6)
            fig2.loglog(fit_xs, fit_ys, colour + "o", markersize=3, label = "theoretical m = " + str(m))
            fig1.set_xlim((-2, 50))
            fig1.plot(xs, ys, colour + "x", label = "m = " + str(m), markersize = 6)
            fig1.plot(fit_xs, fit_ys, colour + "o", markersize = 3, label = "theoretical m = " + str(m))
            colour_counter += 1

        if show_stats_results:
            results = anderson_ksamp([ys, fit_ys])
            print(results)
    if show_plots:
        for fig in [fig1, fig2]:
            fig.set_xlabel(r"$k$")
            fig.set_ylabel(r"$p_{<}(k)$")
            fig.grid()
        fig2.legend()
        ax.suptitle("Degree CDF lin/lin and log/log Axes", fontsize = 22)
        plt.show()

if __name__ == "__main__":
    task1_degree_analysis()
