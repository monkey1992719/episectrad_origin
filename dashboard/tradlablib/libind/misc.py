# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math as m

from .utils import *
from .pyti import *
from .momentum import *
from .trend import *
from .volatility import *
from .volume import *

from finta import TA
from sklearn.linear_model import LinearRegression
import statistics
import talib

def choppiness(data, tp=14, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):
    
    high  = data[high_col]
    low   = data[low_col]

    ATR = atr(data, tp)
    CP = pd.series([])

    for i in range(len(data)):
        if i < tp*2:
            CP.append(0)
        else:
            nmrt = np.log10(np.sum(ATR[i-tp:i])/(max(high[i-tp:i])-min(low[i-tp:i])))
            dnmnt = np.log10(tp)
            CP.append(round(100*nmrt / dnmnt))

    if fillna:
        CP = CP.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(CP, name='cp')


def adr(data, length=14, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):
    
    close = data[close_col]

    adr = []

    for i in range(len(data)):
        h = 0
        l = 0

        sindex = i - length + 1
        if sindex < 0:
            sindex = 0
        for j in range(sindex, i - 1):
            if close[i] > close[j]:
                h = h + (close[i] - close[j])
            if close[i] < close[j]:
                l = l + (close[j] - close[i])

        if l == 0:
            l = 1
        n = h / l

        adr.append(n)
        p = n

    if fillna:
        adr = adr.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(adr, name='adr')


def alma(data, length=100, offset=0.01, sigma=6, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):
    
    close = data[close_col]
    
    '''
    ALMA - Arnaud Legoux Moving Average,
    http://www.financial-hacker.com/trend-delusion-or-reality/
    https://github.com/darwinsys/Trading_Strategies/blob/master/ML/Features.py
    '''

    asize = length - 1
    m = offset * asize
    s = length  / sigma
    dss = 2 * s * s

    alma = np.zeros(close.shape)
    wtd_sum = np.zeros(close.shape)

    for l in range(len(close)):
        if l >= asize:
            for i in range(length):
                im = i - m
                wtd = np.exp( -(im * im) / dss)
                alma[l] += close[l - length + i] * wtd
                wtd_sum[l] += wtd
            alma[l] = alma[l] / wtd_sum[l]

    if fillna:
        alma = alma.replace([np.inf, -np.inf], np.nan).fillna(0)

    return pd.Series(alma, name='alma')


def bop(data, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', open_col='Open', fillna=False):
    
    high  = data[high_col]
    low   = data[low_col]
    close = data[close_col]
    open_ = data[open_col]
    
    real = talib.BOP(open_, high, low, close)

    if fillna:
        real = real.replace([np.inf, -np.inf], np.nan).fillna(0)

    return pd.Series(real, name='bop')


def cks(data, P=10, Q=9, X=1, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):
    
    high  = data[high_col]
    low   = data[low_col]
    close = data[close_col]
    
    ATR = atr(data, P)
        
    phs_ = []
    pls_ = []
    for l in range(len(close)):
        sindex = l - P + 1
        if sindex < 0:
            sindex = 0

        xatr = X * ATR[l]
        maxv = max(high[sindex:l])
        minv = max(low[sindex:l])
        phs = maxv - xatr
        pls = minv + xatr
        phs_.append(phs)
        pls_.append(pls)

    ss = pd.series([])
    ls = pd.series([])

    for l in range(len(close)):
        sindex = l - Q + 1
        if sindex < 0:
            sindex = 0

        maxv = max(phs_[sindex:l])
        minv = max(pls_[sindex:l])
        ss.append(maxv)
        ls.append(minv)

    if fillna:
        ss = ss.replace([np.inf, -np.inf], np.nan).fillna(0)
        ls = ls.replace([np.inf, -np.inf], np.nan).fillna(0)

    return {ss: pd.Series(ss, name='ss'), ls: pd.Series(ls, name='ls')}


def efi(data, length=13, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):
    
    ForceIndex=pd.Series(data[close_col].diff(length)* data[vol_col],name='efi')

    return ForceIndex


def env(data, length=50, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):
    
    sma = simple_moving_average(data[close_col], length)
    ub = sma + sma * 0.05
    lb = sma - sma * 0.05
    mp = sma

    return {ub: pd.Series(ub, name='ub'), lb: pd.Series(lb, name='lb'), mp: pd.Series(mp, name='mp')}


def fish(data, length=9, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):
    
    fish=TA.FISH(data, length)
    
    return pd.Series(fish, name='fish')


def hv(data, length=9, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):

    close = data[close_col]
    
    r = np.diff(np.log(close), length)
    r_mean = np.mean(r)
    diff_square = [(r[i]-r_mean)**2 for i in range(0,len(r))]
    std = np.sqrt(sum(diff_square)*(1.0/(len(r)-1)))
    vol = std*np.sqrt(252)
    
    return pd.Series(vol, name='hv')


def ko(data, fast=34, slow=55, period=13, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):

    high  = data[high_col]
    low   = data[low_col]
    close = data[close_col]
    volume = data[vol_col]

    hlc3 = (high + low + close)/3
    dm = high - low
    
    cm = np.zeros(close.shape)
    VF = np.zeros(close.shape)

    lasttrend = 1
    for l in range(len(close)):
        trend = 1
        if l>0 and hlc3[l] <= hlc3[l-1]:
            trend = -1
        
        if l>0:
            if lasttrend==trend:
                cm[l] = cm[l-1] + dm[l]
            else:
                cm[l] = dm[l-1] + dm[l]
        
        if cm[l] == 0:
            temp = -2
        else:
            temp = abs(2 * (dm[l]/(cm[l]-1)))
        VF[l] = volume[l] * temp * trend * 100

        lasttrend = trend
        
    koFast = ema(VF, fast)
    koSlow = ema(VF, slow)
    ko = koFast - koSlow
    kos = ema(ko, period)

    return {ko: pd.Series(ko, name='ko'), kos: pd.Series(kos, name='kos')}


def lsma(data, fast=34, slow=55, period=13, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):

    close = data[close_col]

    sumt = 0
    sumx = 0
    sumtx = 0
    lsma = []
    for l in range(len(close)):
        sumx = sumx + close[l]
        sumt = sumt + (l+1)
        sumtx = sumtx + (l+1)*close[l]
        bb = len(close)*sumt-sumt*sumt
        if bb==0:
            bb = 1
        bt = len(close)*sumtx-sumt*sumx

        b = bt/bb
        a = sumx/len(close) - b*sumt/len(close)
        lsma.append(b*(l+1)+a)

    return pd.Series(lsma, name='lsma')


def lrc(data, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):

    close = data[close_col]

    sma = simple_moving_average(data[close_col], 100)

    X = sma.iloc[:, 0].values.reshape(-1, 1)  # values converts it into a numpy array
    Y = sma.iloc[:, 1].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions



    return pd.Series(Y_pred, name='lrc')


def md(data, length=14, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):

    close = data[close_col]

    k=0.6
    md = np.zeros(close.shape)
    md[0] = close[0]/(k*len(close)*close[0])

    for l in range(1, len(close)):
        md[l] = md[l-1] + (close[l]-md[l-1])/(k*len(close)*m.pow(close/md[l-1], 4))

    return pd.Series(md, name='md')    


def psar(data, start=0, iaf=0.02, maxaf=0.2, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):

    length = len(data)
    high  = data[high_col]
    low   = data[low_col]
    close = data[close_col]

    psar = close[start:len(close)]
    psarbull = [None] * length
    psarbear = [None] * length
    bull = True
    af = iaf
    ep = low[0]
    hp = high[0]
    lp = low[0]
    for i in range(2,length):
        if bull:
            psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
        else:
            psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
        reverse = False
        if bull:
            if low[i] < psar[i]:
                bull = False
                reverse = True
                psar[i] = hp
                lp = low[i]
                af = iaf
        else:
            if high[i] > psar[i]:
                bull = True
                reverse = True
                psar[i] = lp
                hp = high[i]
                af = iaf
        if not reverse:
            if bull:
                if high[i] > hp:
                    hp = high[i]
                    af = min(af + iaf, maxaf)
                if low[i - 1] < psar[i]:
                    psar[i] = low[i - 1]
                if low[i - 2] < psar[i]:
                    psar[i] = low[i - 2]
            else:
                if low[i] < lp:
                    lp = low[i]
                    af = min(af + iaf, maxaf)
                if high[i - 1] > psar[i]:
                    psar[i] = high[i - 1]
                if high[i - 2] > psar[i]:
                    psar[i] = high[i - 2]
        if bull:
            psarbull[i] = psar[i]
        else:
            psarbear[i] = psar[i]

    return {psar:pd.Series(psar, name='psar'), psarbull:pd.Series(psarbull, name='psarbull'), psarbear:pd.Series(psarbear, name='psarbear')}



def pvt(data, trend_length=21, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):

    close = data[close_col]
    volume = data[vol_col]
    
    last_val = close[0]
    pvt.append(last_val)
    for l in range(1, len(close)):
        current_val = last_val + (volume[l] * (close[l] - close[l-1]) / close[l-1])
        pvt.append(last_val)
        last_val = current_val

    return pd.Series(pvt, name='pvt')    


def rvgi(data, length=10, offset=4, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', open_col='Open', fillna=False):

    high  = data[high_col]
    low   = data[low_col]
    close = data[close_col]
    volume = data[vol_col]
    open = data[open_col]

    RVGI = (close-open)/(high-low)

    rvig = simple_moving_average(RVI, length)
    rvir = weighted_moving_average(RVI, offset)
    
    return {rvgig: pd.Series(rvgig, name='rvgig'), rvgir: pd.Series(rvgir, name='rvgir')}



def rvi(data, length=10, offset=4, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', open_col='Open', fillna=False):

    close = data[close_col]

    upavg = 0
    dnavg = 0
    rvi = np.zeros(close.shape)
    for l in range(9, len(close)):
        if close[l] > close[l-1]:
            up=statistics.stdev(close[l-9:l])
            dn=0
        else:
            up=0
            dn=statistics.stdev(close[l-9:l])
        upavg=(upavg*(length-1)+up)/length
        dnavg=(dnavg*(length-1)+dn)/length
        rvi[l] = 100*upavg/(upavg+dnavg)

   
    return pd.Series(rvi, name='rvi')


def smi(data, long_period=20, short_period=5, signal_period=5,  high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', open_col='Open', fillna=False):

    close = data[close_col]

    rvi = np.zeros(close.shape)
    change = np.zeros(close.shape)
    absChange = np.zeros(close.shape)

    for l in range(9, len(close)):
        change[l] = close[l] - close[l-1]
        absChange[l] = abs(change)
        

    tempChange = ema(change, long_period)
    tempAbsC = ema(absChange, long_period)
    tempChange = ema(tempChange, short_period)
    tempAbsC = ema(tempAbsC, short_period)
    SMI = tempChange / tempAbsC
    SIGNAL = ema(SMI, signal_period)

    return {smi: pd.Series(SMI, name='smi'), smi_signal: pd.Series(SIGNAL, name='smi_signal')}


def vwma(data, length=14, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', open_col='Open', fillna=False):

    close = data[close_col]

    vwma = data.apply(lambda x: x[close_col] * x[vol_col], axis=1).rolling(length).sum() / data['vol_col'].rolling(length).sum()

    return pd.Series(vwma, name='vwma')


def wali(data, jaw_length=13, teeth_length=8, lips_length=13, jaw_offset=8, teeth_offset=5, lips_offset=3, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', open_col='Open', fillna=False):

    close = data[close_col]
    jaw = smoothed_moving_average(close, jaw_length)
    jaw = np.concatenate((jaw[jaw_offset:],np.zeros(jaw_offset)), axis=0)
    teeth = smoothed_moving_average(close, teeth_length)
    teeth = np.concatenate((teeth[teeth_offset:],np.zeros(teeth_offset)), axis=0)
    lips = smoothed_moving_average(close, lips_length)
    lips = np.concatenate((lips[lips_offset:],np.zeros(lips_offset)), axis=0)

    return {jaw: pd.Series(jaw, name='jaw'), teeth: pd.Series(teeth, name='teeth'), lips: pd.Series(lips, name='lips')}


def wf(data, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', open_col='Open', fillna=False):

    close = data[close_col]

    return {jaw: pd.Series(jaw, name='jaw'), teeth: pd.Series(teeth, name='teeth'), lips: pd.Series(lips, name='lips')}