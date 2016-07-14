import dataLoader as dl
import correlation as cl
import dateFunctions as df
import mapping
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


d = dl.loadFile()
d = dl.separateStations(d)
v1 = d['93737'].values
cs = []
ds = []
for s in d.columns[1:]:
    c, diff = cl.timeCorrelation(v1, d[s].values,40)
    m_c, m_d = cl.maxCorrelation(c, diff)
    cs += [m_c]
    ds += [m_d]
plt.scatter(ds, cs)
    




"""
data1 = cl.opener()
data = data1.values
ds = []
for d in range(data.shape[1]):
    ds += [data[:,d]]

subd = ds[:10]
corr_arr = np.zeros((len(subd), len(subd)))
off_arr = np.zeros((len(subd), len(subd)))
for i, d1 in enumerate(subd):
    for j, d2 in enumerate(subd):
        c, n = timeCorrelation(d1, d2, 5)
        max_c, max_n = maxCorrelation(c, n)
        corr_arr[i,j] = max_c
        off_arr[i,j] = max_n

coors = cl.dataGetter.getLatLong(data1.columns)
mapping.plotCoors(coors.values())
"""