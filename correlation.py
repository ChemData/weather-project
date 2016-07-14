import numpy as np
import matplotlib.pyplot as plt
import pandas
import mapping
import dataGetter

def opener():
    return pandas.read_pickle('TMAXdata.pkl')
    
def correlation(v1, v2):
    std1 = np.std(v1, ddof=1)
    std2 = np.std(v2, ddof=1)
    stds = np.array([std1, std2])
    stds = np.outer(stds, stds)
    correlations =  np.cov(v1, v2)*1./stds
    return correlations[0,1]
    
def timeCorrelation(v1, v2, max_difference):
    """Calculates the correlation over time of two time series. The section
        overlapped is changed up to max_difference. Ignores NaNs.
        v1 - 1D array of numbers.
        v2 - 1D array of numbers.
        max_difference - int.
    """
    differences = np.array(range(-1*max_difference, max_difference+1))
    output = []
    for i in differences:
        if i <= 0:
            tv1 = v1[-1*i:]
            tv2 = v2[:len(v2)+i]
        else:
            tv1 = v1[:len(v1)-i]
            tv2 = v2[i:]
        tv1, tv2 = removeNaN(tv1, tv2)
        output += [correlation(tv1, tv2)]
    return output, differences

def removeNaN(v1, v2):
    """Removes NaNs from two vectors and the corresponding values in the other
        vector.
    """
    o1 = []
    o2 = []
    for i in range(len(v1)):
        n1 = v1[i]
        n2 = v2[i]
        if not np.isnan(n1) and not np.isnan(n2):
            o1 += [n1]
            o2 += [n2]
    return o1, o2
    
def maxCorrelation(c, n):
    """Determines which amount of offset had the most correlation.
        c - 1D array of floats. A list of correlations for each offset.
        n - 1D array of ints. A list of offsets.
    """
    max_c = c[0]
    max_n = n[0]
    for i, v in enumerate(c):
        if v > max_c:
            max_c = v
            max_n = n[i]
    return max_c, max_n

