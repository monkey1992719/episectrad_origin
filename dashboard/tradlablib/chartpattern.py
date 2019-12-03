import pandas as pd
import talib
import numpy as np
import plotly
import plotly.graph_objs as go
from numpy import array, zeros, argmin, inf, ndim
from scipy.spatial.distance import cdist
from scipy import signal
from scipy.signal import savgol_filter
# from sklearn.linear_model import LinearRegression
import math
# from statsmodels.nonparametric.smoothers_lowess import lowess


patternnames = ['Ascending Triangle', 'Descending Triangle', 'Bullish Symmetric Triangle', 'Bearish Symmetric Triangle', 'Cup And Handle', 'Inverse Cup And Handle', 'Channel up', 'Channel down', 'Double Bottom', 'Double Top', 'Rising Wedge', 'Falling Wedge', 'Inverse Head And Shoulders', 'Head And Shoulders', 'Triple bottom', 'Triple top', 'Bull Flag Continuation', 'Bear Flag Continuation', 'Bull Pennant', 'Bear Pennant', 'Rounding Bottom', 'Rounding Top']
bullishpatternnames = ['Ascending Triangle', 'Bullish Symmetric Triangle', 'Cup And Handle', 'Channel up', 'Double Bottom', 'Rising Wedge', 'Inverse Head And Shoulders', 'Triple bottom', 'Bull Flag Continuation', 'Bull Pennant', 'Rounding Bottom']
bearishpatternnames = ['Descending Triangle','Bearish Symmetric Triangle', 'Inverse Cup And Handle', 'Channel down', 'Double Top', 'Falling Wedge', 'Head And Shoulders', 'Triple top', 'Bear Flag Continuation', 'Bear Pennant', 'Rounding Top']

patterns = []
#Ascending Triangle pattern reverse
patterns.append(np.array([0,8,2,8,4,8,6]))
#Descending Triangle pattern reverse
patterns.append(np.array([8,0,6,0,4,0,2]))
#Bullish Symmetric Triangle
patterns.append(np.array([7,1,6,2,5,3,4]))
#Bearish Symmetric Triangle
patterns.append(np.array([1,7,2,6,3,5,4]))
#Cup And Handle
patterns.append(np.array([8,3,4,1,2,0,2,1,4,3,8,6,4]))
#Inverse Cup And Handle
patterns.append(np.array([0,5,4,7,6,8,6,7,4,5,0,2,4]))
#Channel up
patterns.append(np.array([0,2,1,4,3,6,5,8]))
#Channel down
patterns.append(np.array([8,6,7,4,5,2,3,0]))
#Double Bottom
patterns.append(np.array([6,4,6,4,6]))
#Double Top
patterns.append(np.array([4,6,4,6,4]))
#Rising Wedge
patterns.append(np.array([0,6,1,7,2,8,3]))
#Falling Wedge
patterns.append(np.array([8,2,7,1,6,0,5]))
#Head and shoulder pattern reverse
patterns.append(np.array([6,4,6,2,6,4,6]))
#Head and shoulder pattern
patterns.append(np.array([4,6,4,8,4,6,4]))
#Triple bottom
patterns.append(np.array([4,2,4,2,4,2,4]))
#Triple top
patterns.append(np.array([4,6,4,6,4,6,4]))
#Bull Flag Continuation
patterns.append(np.array([6,4,6,2,6,4,6]))
#Bear Flag Continuation
patterns.append(np.array([6,4,6,2,6,4,6]))
#Bull Pennant
patterns.append(np.array([6,4,6,2,6,4,6]))
#Bear Pennant
patterns.append(np.array([6,4,6,2,6,4,6]))
#Rounding Bottom
patterns.append(np.array([6,4,6,2,6,4,6]))
#Rounding Top
patterns.append(np.array([6,4,6,2,6,4,6]))

def dtw(x, y, warp=1):
    """
    Computes Dynamic Time Warping (DTW) of two sequences in a faster way.
    Instead of iterating through each element and calculating each distance,
    this uses the cdist function from scipy (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html)
    :param array x: N1*M array
    :param array y: N2*M array
    :param string or func dist: distance parameter for cdist. When string is given, cdist uses optimized functions for the distance metrics.
    If a string is passed, the distance function can be 'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean', 'hamming', 'jaccard', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'wminkowski', 'yule'.
    :param int warp: how many shifts are computed.
    Returns the minimum distance, the cost matrix, the accumulated cost matrix, and the wrap path.
    """
    assert len(x)
    assert len(y)
    if ndim(x) == 1:
        x = x.reshape(-1, 1)

    if ndim(y) == 1:
        y = y.reshape(-1, 1)

    r, c = len(x), len(y)
    D0 = zeros((r + 1, c + 1))
    D0[0, 1:] = inf
    D0[1:, 0] = inf
    D1 = D0[1:, 1:]

    D0[1:, 1:] = cdist(x, y, 'euclidean')
    
    C = D1.copy()
    for i in range(r):
        for j in range(c):
            min_list = [D0[i, j]]
            for k in range(1, warp + 1):
                min_list += [D0[min(i + k, r - 1), j],
                             D0[i, min(j + k, c - 1)]]
            D1[i, j] += min(min_list)
    if len(x) == 1:
        path = zeros(len(y)), range(len(y))
    elif len(y) == 1:
        path = range(len(x)), zeros(len(x))
    else:
        path = _traceback(D0)
    return D1[-1, -1] / sum(D1.shape), C, D1, path


def _traceback(D):
    i, j = array(D.shape) - 2
    p, q = [i], [j]
    while (i > 0) or (j > 0):
        tb = argmin((D[i, j], D[i, j+1], D[i+1, j]))
        if tb == 0:
            i -= 1
            j -= 1
        elif tb == 1:
            i -= 1
        else:  # (tb == 2):
            j -= 1
        p.insert(0, i)
        q.insert(0, j)
    return array(p), array(q)


def normalize(s, pattern):
    a = min(pattern)
    b = max(pattern)
    xmin = min(s)
    xmax = max(s)
    sdot = []

    for x in s:
        xdot = a + (x - xmin) * (b - a) / (xmax - xmin)
        sdot.append(xdot)

    return sdot


def recogpattern(sample_points, patternname):
    samplecnt = len(sample_points)
    patternno = patternnames.index(patternname)

    patternlen = len(patterns[patternno])
    if patternlen > samplecnt:
        pass

    maxdist = 10000
    searchedindex = 0

    for i in range(samplecnt-patternlen):
        testpattern = []
        for j in range(patternlen):
            testpattern.append(sample_points[i+j])
        testpattern = normalize(testpattern, patterns[patternno])
        testpattern = np.array(testpattern)
        dist, cost, acc, path = dtw(patterns[patternno], testpattern)

        if dist < maxdist:
            maxdist = dist
            searchedindex = i

    return searchedindex, maxdist, patternlen


def sampling(sample_points):
    presign = 2
    delta = 8
    ind = 1
    sample_points = np.array(sample_points, 'f')
    indexes = np.arange(len(sample_points))
    newsample = [sample_points[0]]
    newsampleind = [0]

    while ind < len(sample_points):
        offset = sample_points[ind] - sample_points[ind - 1]
        if(offset > 0):
            sign = 1
        elif(offset < 0):
            sign = -1 
        else:
            ind = ind + 1
            continue

        if(abs(offset) > delta):
            newsample.append(sample_points[ind])
            newsampleind.append(ind)

        presign = sign
        ind = ind + 1

    return newsample, newsampleind


def recogchartpattern(df, patternname):
    dates = df['Date']
    sample_points = df['Close']

    # resample_points, resampleind = sampling(sample_points)
    resample_count = int(len(sample_points) / 5)
    if len(sample_points) <= 20:
        resample_count = len(sample_points)

    indexes = np.array(np.linspace(0, len(sample_points)-1, len(sample_points)), 'i')
    resample_points, resampleind = signal.resample(sample_points, resample_count, indexes)
    resampleind = resampleind.astype(int)
    searchedindex, maxdist, patternlen = recogpattern(resample_points, patternname)
    fromdate = dates[resampleind[searchedindex]]
    todate = dates[resampleind[searchedindex+patternlen]]
    
    highs = df['High'][resampleind[searchedindex]:resampleind[searchedindex+patternlen]]
    lows = df['Low'][resampleind[searchedindex]:resampleind[searchedindex+patternlen]]
    
    maxval = max(highs)
    minval = min(lows)

    fromindex = resampleind[searchedindex]
    toindex = resampleind[searchedindex+patternlen]

    # return fromdate, todate, maxval, minval, fromindex, toindex
    return {'fromdate': fromdate, 'todate': todate, 'maxval': maxval, 'minval': minval, 'fromindex' : str(fromindex), 'toindex' : str(toindex)}


##### test ##########


# df = pd.read_csv('../../media/labdata/NSEI.csv', sep=',')
# df = pd.DataFrame(df)
# df = df.dropna()
# dates = df['Date']
# sample_points = df['Close']

# resample_count = int(len(sample_points) / 5)
# if len(sample_points) <= 20:
#     resample_count = len(sample_points)

# indexes = np.array(np.linspace(0, len(sample_points)-1, len(sample_points)), 'i')
# resample_points, resampleind = signal.resample(sample_points, resample_count, indexes)
# resampleind = resampleind.astype(int)
# print(resampleind)
# trace1 = go.Scatter(
#     x = dates,
#     y = sample_points
# )
# trace2 = go.Scatter(
#     x = dates[resampleind],
#     #y = filtered[:,1]
#     y = resample_points
# )
# data = [trace1, trace2]
# plotly.offline.plot(data)


# resample_points, resampleind = sampling(sample_points)
# recogchartpattern(resample_points, 'Inverse Head And Shoulders')

# trace = go.Ohlc(x=df['Date'],
#                 open=df['Open'],
#                 high=df['High'],
#                 low=df['Low'],
#                 close=df['Close'])
#indexes = np.array(np.linspace(0, len(sample_points)-1, len(sample_points)), 'i')
# trace1 = go.Scatter(
#     x = dates,
#     y = sample_points
# )
# filtered = lowess(sample_points,range(len(sample_points)), frac=0.1, is_sorted=True, it=0)
# sampled, indexes = signal.resample(sample_points, len(sample_points), indexes)
#maxima = argrelextrema(filtered[:,1], np.greater)
#if len(maxima[0]) == 3:
# newsample, newsampleind = sampling(samplel_points)
# trace2 = go.Scatter(
#     x = dates[resampleind],
#     #y = filtered[:,1]
#     y = resample_points
# )
# data = [trace1, trace2]
# plotly.offline.plot(data)


def sampling(points):
    sample_count = int(len(points) / 5)
    if len(points) <= 50:
        return points, np.arange(len(points))

    indexes = np.array(np.linspace(0, len(points)-1, len(points)), 'i')
    sample_points, sampleind = signal.resample(points, sample_count, indexes)
    sampleind = sampleind.astype(int)

    return sample_points, sampleind


def searchextremum(points):

    points_ = np.array(points)
    
    if len(points_)<8:
        return len(points) - 1

    filtersize = int(len(points_)/2)
    if filtersize % 2 == 0:
        filtersize += 1
    sample_points = savgol_filter(points_, filtersize, 2)

    extind = 0
    deltax = 2
    for i in range(len(sample_points)-2):
        p1 = sample_points[i]
        p2 = sample_points[i+1]
        p3 = sample_points[i+2]

        angle1 = math.atan((p2-p1)/deltax)/math.pi*180
        angle2 = math.atan((p3-p2)/deltax)/math.pi*180

        if (angle1 > 0 and angle2 < 0) or (angle1 < 0 and angle2 > 0):
            extind = i + 1
            break

    if extind == 0:
        return len(points) - 1
    
    # return sampleind[extind]
    return extind


def getdirection(points):
    # First, search the extremum point.
    # Second, get the direction until the extremum point.   1: uptrending -1: downtrending

    extind = searchextremum(points)
    trend=0
    if np.array(points)[0] > np.array(points)[extind]:
        trend = -1
    elif np.array(points)[0] < np.array(points)[extind]:
        trend = 1

    return trend, extind
    
