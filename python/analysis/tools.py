''' Contains shared functions that are useful for all tasks'''
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl

def set_plot_defaults():
    x_size = 10

    mpl.rcParams['figure.figsize'] = [x_size, x_size/1.61]
    mpl.rcParams['figure.dpi'] = 80
    mpl.rcParams['savefig.dpi'] = 100

    mpl.rcParams['font.size'] = 14
    mpl.rcParams['legend.fontsize'] = 'medium'
    mpl.rcParams['axes.labelsize'] = 16
    mpl.rcParams['figure.titlesize'] = 'large'
    return

def import_distributions(task = "task3"):
    ''' Imports c++ data from txt for all distributions
        matching the given task

        task = "task1", "task2" or "task3"

        returns: dict[(N,m)] for tasks 1, 2
                 dict[(N, m, q)] for task 3
    '''
    datapath = "../../data"

    distributions = {}
    for filename in os.listdir(datapath):
        if filename.endswith(".txt") and "distribution" in filename:
            if filename.startswith(task):
                dist_path = os.path.join(datapath, filename)
                fname = dist_path.split("/")[-1][0:-4] #todo check
                N = int(re.findall("N[0-9]+", fname)[0][1:])
                m = int(re.findall("m[0-9]+", fname)[0][1:])

                if task == "task3":
                    q = float(re.findall(r"q[01]\.[0-9]+", fname)[0][1:])
                    key = (N, m, q)
                else:
                    key = (N, m)

                f = open(dist_path)

                vertices = []
                ks       = []

                for line in f:
                    vertex, k = line.split(",")
                    vertices.append(int(vertex))
                    ks.append(int(k))

                data = (vertices, ks)
                distributions[key] = data
    return distributions

def logbin(data, scale = 1., zeros = False):
    """
    logbin(data, scale = 1., zeros = False)

    Log-bin frequency of unique integer values in data. Returns probabilities
    for each bin.

    Array, data, is a 1-d array containing full set of event sizes for a
    given process in no particular order. For instance, in the Oslo Model
    the array may contain the avalanche size recorded at each time step. For
    a complex network, the array may contain the degree of each node in the
    network. The logbin function finds the frequency of each unique value in
    the data array. The function then bins these frequencies in logarithmically
    increasing bin sizes controlled by the scale parameter.

    Minimum binsize is always 1. Bin edges are lowered to nearest integer. Bins
    are always unique, i.e. two different float bin edges corresponding to the
    same integer interval will not be included twice. Note, rounding to integer
    values results in noise at small event sizes.

    Parameters
    ----------

    data: array_like, 1 dimensional, non-negative integers
          Input array. (e.g. Raw avalanche size data in Oslo model.)

    scale: float, greater or equal to 1.
          Scale parameter controlling the growth of bin sizes.
          If scale = 1., function will return frequency of each unique integer
          value in data with no binning.

    zeros: boolean
          Set zeros = True if you want binning function to consider events of
          size 0.
          Note that output cannot be plotted on log-log scale if data contains
          zeros. If zeros = False, events of size 0 will be removed from data.

    Returns
    -------

    x: array_like, 1 dimensional
          Array of coordinates for bin centres calculated using geometric mean
          of bin edges. Bins with a count of 0 will not be returned.
    y: array_like, 1 dimensional
          Array of normalised frequency counts within each bin. Bins with a
          count of 0 will not be returned.
    """

    if scale < 1:
        raise ValueError('Function requires scale >= 1.')
    count = np.bincount(data)
    tot = np.sum(count)
    smax = np.max(data)
    if scale > 1:
        jmax = np.ceil(np.log(smax)/np.log(scale))
        if zeros:
            binedges = scale ** np.arange(jmax + 1)
            binedges[0] = 0
        else:
            binedges = scale ** np.arange(1,jmax + 1)
            # count = count[1:]
        binedges = np.unique(binedges.astype('uint64'))
        x = (binedges[:-1] * (binedges[1:]-1)) ** 0.5
        y = np.zeros_like(x)
        count = count.astype('float')
        for i in range(len(y)):
            y[i] = np.sum(count[binedges[i]:binedges[i+1]]/(binedges[i+1] - binedges[i]))
            # print(binedges[i],binedges[i+1])
        # print(smax,jmax,binedges,x)
        # print(x,y)
    else:
        x = np.nonzero(count)[0]
        y = count[count != 0].astype('float')
        if zeros != True and x[0] == 0:
            x = x[1:]
            y = y[1:]
    y /= tot
    x = x[y!=0]
    y = y[y!=0]
    return x,y
