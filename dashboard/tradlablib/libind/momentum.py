# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math as m

from .utils import *
from .pyti import *

from .pyti.simple_moving_average import (
    simple_moving_average as sma
    )

#from libind.pyti.stochastic import *


def copp(df, n, fillna=False):
    """Coppock Curve
    
    """
    M = df['Close'].diff(int(n * 11 / 10) - 1)  
    N = df['Close'].shift(int(n * 11 / 10) - 1)  
    ROC1 = M / N  
    M = df['Close'].diff(int(n * 14 / 10) - 1)  
    N = df['Close'].shift(int(n * 14 / 10) - 1)  
    ROC2 = M / N  
    Copp = pd.Series((ROC1 + ROC2).ewm(span=n, min_periods=n).mean())

    if fillna:
        Copp = Copp.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(Copp, name='copp')
 
def cmo(data, n, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """
    Chande Momentum Oscillator.
    Formula:
    cmo = 100 * ((sum_up - sum_down) / (sum_up + sum_down))
    """
    close = data[close_col].tolist()
    cmo__ = pd.Series(chande_momentum_oscillator.chande_momentum_oscillator(close, n))
    if fillna:
        cmo__ = cmo__.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(cmo__, name='cmo')
    
def po_indicator(data, short_length, long_length, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """
    Price Oscillator.

    Formula:
    (short EMA - long EMA / long EMA) * 100
    """
    close = data[close_col].tolist()
    po_ = pd.Series(price_oscillator.price_oscillator(close,short_length, long_length ))
    if fillna:
        po_ = po_.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(po_, name='po')
    
def stochastic(df, s_k=14, s_d=3, s_smooth=3):
    """ Stochastic indicator with smoothing.
        Equivalent to Stochastic Slow that is considered superior.
        
        http://www.onlinetradingconcepts.com/TechnicalAnalysis/Stochastics.html
        
     Args:
        close(pandas.Series): dataset 'Close' column.
        s_k, s_d and s_smooth

    Returns:
        Slow %K, Slow %D
    """
    high = df['High']
    low  = df['Low']
    close= df['Close']
    #stoc = ((close - pd.rolling_min(low, s_k)) / (pd.rolling_max(high, s_k) - pd.rolling_min(low, s_k))) * 100
    #stok = pd.rolling_mean(stoc, s_d)
    #stod = pd.rolling_mean(stok, s_smooth)
    
    stoc = ((close - low.rolling(s_k).min()) / (high.rolling(s_k).max() - low.rolling(s_k).min())) * 100
    stok = stoc.rolling(s_d).mean()
    stod = stok.rolling(s_smooth).mean()

    return pd.Series(stok, name='STOK'), pd.Series(stod, name='STOD')

'''
def stochastic(close, s_k=14, s_d=3, s_smooth=3):
    """ Stochastic indicator with smoothing.
        Equivalent to Stochastic Slow that is considered superior.
        
        http://www.onlinetradingconcepts.com/TechnicalAnalysis/Stochastics.html
        
     Args:
        close(pandas.Series): dataset 'Close' column.
        s_k, s_d and s_smooth

    Returns:
        Slow %K, Slow %D
    """
    stoc = percent_k(close, s_k)
    stok = smooth_sma(stoc, s_d)
    stod = smooth_sma(stok, s_smooth)

    return stok, stod
'''

def rsi(close, n=14, fillna=False):
    """Relative Strength Index (RSI)

    Compares the magnitude of recent gains and losses over a specified time
    period to measure speed and change of price movements of a security. It is
    primarily used to attempt to identify overbought or oversold conditions in
    the trading of an asset.

    https://www.investopedia.com/terms/r/rsi.asp

    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    diff = close.diff()
    which_dn = diff < 0

    up, dn = diff, diff*0
    up[which_dn], dn[which_dn] = 0, -up[which_dn]

    emaup = ema(up, n)
    emadn = ema(dn, n)

    rsi = 100 * emaup / (emaup + emadn)
    if fillna:
        rsi = rsi.replace([np.inf, -np.inf], np.nan).fillna(50)
    return pd.Series(rsi, name='rsi')

def mom_indicator(data, n, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """
    Momentum.

    Formula:
    DATA[i] - DATA[i - period]
    """
    close = data[close_col].tolist()
    mom = pd.Series(momentum.momentum(close, n))
    if fillna:
        mom = mom.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(mom, name='mom')

    
def money_flow_index_sma(data, sma_length=5):

    mfi_sma = sma(data, sma_length)

    return pd.Series(mfi_sma, name='mfi_sma')


#def money_flow_index(high, low, close, volume, n=14, fillna=False):
def money_flow_index(data, n=14, avg_len=5, high_col='High', low_col='Low', 
                     close_col='Close', vol_col='Volume', fillna=False):
    """Money Flow Index (MFI)

    Uses both price and volume to measure buying and selling pressure. It is
    positive when the typical price rises (buying pressure) and negative when
    the typical price declines (selling pressure). A ratio of positive and
    negative money flow is then plugged into an RSI formula to create an
    oscillator that moves between zero and one hundred.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:money_flow_index_mfi

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.

    """
    high    = data[high_col]
    low     = data[low_col]
    close   = data[close_col]
    volume  = data[vol_col]

    # 0 Prepare dataframe to work
    df = pd.DataFrame([high, low, close, volume]).T
    df.columns = ['High', 'Low', 'Close', 'Volume']
    df['Up_or_Down'] = 0
    df.loc[(df['Close'] > df['Close'].shift(1)), 'Up_or_Down'] = 1
    df.loc[(df['Close'] < df['Close'].shift(1)), 'Up_or_Down'] = 2

    # 1 typical price
    tp = (df['High'] + df['Low'] + df['Close']) / 3.0

    # 2 money flow
    mf = tp * df['Volume']

    # 3 positive and negative money flow with n periods
    df['1p_Positive_Money_Flow'] = 0.0
    df.loc[df['Up_or_Down'] == 1, '1p_Positive_Money_Flow'] = mf
    n_positive_mf = df['1p_Positive_Money_Flow'].rolling(n).sum()

    df['1p_Negative_Money_Flow'] = 0.0
    df.loc[df['Up_or_Down'] == 2, '1p_Negative_Money_Flow'] = mf
    n_negative_mf = df['1p_Negative_Money_Flow'].rolling(n).sum()

    # 4 money flow index
    mr = n_positive_mf / n_negative_mf
    mr = (100 - (100 / (1 + mr)))
    if fillna:
        mr = mr.replace([np.inf, -np.inf], np.nan).fillna(50)

    return pd.Series(mr, name='mfi_')


#def tsi(close, r=25, s=13, fillna=False):
def tsi(data, r=25, s=13, high_col='High', low_col='Low', 
        close_col='Close', vol_col='Volume', fillna=False):
    """True strength index (TSI)

    Shows both trend direction and overbought/oversold conditions.

    https://en.wikipedia.org/wiki/True_strength_index

    Args:
        close(pandas.Series): dataset 'Close' column.
        r(int): high period.
        s(int): low period.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    close = data[close_col]
    m = close - close.shift(1)
    m1 = m.ewm(r).mean().ewm(s).mean()
    m2 = abs(m).ewm(r).mean().ewm(s).mean()
    tsi = m1 / m2
    tsi *= 100
    
    if fillna:
        tsi = tsi.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(tsi, name='tsi')

#def uo(high, low, close, s=7, m=14, l=28, ws=4.0, wm=2.0, wl=1.0, fillna=False):
def uo(data, s=7, m=14, l=28, ws=4.0, wm=2.0, wl=1.0, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):
    """Ultimate Oscillator

    Larry Williams' (1976) signal, a momentum oscillator designed to capture momentum
    across three different timeframes.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ultimate_oscillator

    BP = Close - Minimum(Low or Prior Close).
    TR = Maximum(High or Prior Close)  -  Minimum(Low or Prior Close)
    Average7 = (7-period BP Sum) / (7-period TR Sum)
    Average14 = (14-period BP Sum) / (14-period TR Sum)
    Average28 = (28-period BP Sum) / (28-period TR Sum)

    UO = 100 x [(4 x Average7)+(2 x Average14)+Average28]/(4+2+1)

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        s(int): short period
        m(int): medium period
        l(int): long period
        ws(float): weight of short BP average for UO
        wm(float): weight of medium BP average for UO
        wl(float): weight of long BP average for UO
        fillna(bool): if True, fill nan values with 50.

    Returns:
        pandas.Series: New feature generated.

    """
    high  = data[high_col]
    low   = data[low_col]
    close = data[close_col]

    min_l_or_pc = close.shift(1).combine(low, min)
    max_h_or_pc = close.shift(1).combine(high, max)

    bp = close - min_l_or_pc
    tr = max_h_or_pc - min_l_or_pc

    avg_s = bp.rolling(s).sum() / tr.rolling(s).sum()
    avg_m = bp.rolling(m).sum() / tr.rolling(m).sum()
    avg_l = bp.rolling(l).sum() / tr.rolling(l).sum()

    uo = 100.0 * ((ws * avg_s) + (wm * avg_m) + (wl * avg_l)) / (ws + wm + wl)
    if fillna:
        uo = uo.replace([np.inf, -np.inf], np.nan).fillna(50)
    return pd.Series(uo, name='uo')
    
def stchrsi_indicator(data, n, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """
    StochRSI.

    Formula:
    SRSI = ((RSIt - RSI LOW) / (RSI HIGH - LOW RSI)) * 100
    """
    close = data[close_col].tolist()
    
    stch_rsi = pd.Series(stochrsi.stochrsi(close, n))
    if fillna:
        stch_rsi = stch_rsi.replace([np.inf, -np.inf], np.nan).fillna(50)
    return pd.Series(stch_rsi, name='stch_rsi')
    
def stoch(high, low, close, n=14, fillna=False):
    """Stochastic Oscillator

    Developed in the late 1950s by George Lane. The stochastic
    oscillator presents the location of the closing price of a
    stock in relation to the high and low range of the price
    of a stock over a period of time, typically a 14-day period.

    https://www.investopedia.com/terms/s/stochasticoscillator.asp

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    smin = low.rolling(n).min()
    smax = high.rolling(n).max()
    stoch_k = 100 * (close - smin) / (smax - smin)

    if fillna:
        stoch_k = stoch_k.replace([np.inf, -np.inf], np.nan).fillna(50)
    return pd.Series(stoch_k, name='stoch_k')

def stoch_signal(high, low, close, n=14, d_n=3, fillna=False):
    """Stochastic Oscillator Signal

    Shows SMA of Stochastic Oscillator. Typically a 3 day SMA.

    https://www.investopedia.com/terms/s/stochasticoscillator.asp

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        d_n(int): sma period over stoch_k
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    stoch_k = stoch(high, low, close, n, fillna=fillna)
    stoch_d = stoch_k.rolling(d_n).mean()

    if fillna:
        stoch_d = stoch_d.replace([np.inf, -np.inf], np.nan).fillna(50)
    return pd.Series(stoch_d, name='stoch_d')


#def wr(high, low, close, lbp=14, fillna=False):
def wr(data, lbp=14, high_col='High', low_col='Low', 
       close_col='Close', vol_col='Volume', fillna=False):
    """Williams %R

    From: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:williams_r

    Developed by Larry Williams, Williams %R is a momentum indicator that is the inverse of the
    Fast Stochastic Oscillator. Also referred to as %R, Williams %R reflects the level of the close
    relative to the highest high for the look-back period. In contrast, the Stochastic Oscillator
    reflects the level of the close relative to the lowest low. %R corrects for the inversion by
    multiplying the raw value by -100. As a result, the Fast Stochastic Oscillator and Williams %R
    produce the exact same lines, only the scaling is different. Williams %R oscillates from 0 to -100.

    Readings from 0 to -20 are considered overbought. Readings from -80 to -100 are considered oversold.

    Unsurprisingly, signals derived from the Stochastic Oscillator are also applicable to Williams %R.


    %R = (Highest High - Close)/(Highest High - Lowest Low) * -100

    Lowest Low = lowest low for the look-back period
    Highest High = highest high for the look-back period
    %R is multiplied by -100 correct the inversion and move the decimal.

    From: https://www.investopedia.com/terms/w/williamsr.asp
    The Williams %R oscillates from 0 to -100. When the indicator produces readings from 0 to -20, this indicates
    overbought market conditions. When readings are -80 to -100, it indicates oversold market conditions.


    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        lbp(int): lookback period
        fillna(bool): if True, fill nan values with -50.

    Returns:
        pandas.Series: New feature generated.
    """
    high  = data[high_col]
    low   = data[low_col]
    close = data[close_col]

    hh = high.rolling(lbp).max() #highest high over lookback period lbp
    ll = low.rolling(lbp).min()  #lowest low over lookback period lbp
    
    # Williams %R is same as Stochastic Fast. Earlier implementation, commented below, was buggy. 
    #wr = -100 * (hh - close) / (hh - ll)
    wr = 100*((close - ll) / (hh - ll)) # Correct one

    if fillna:
        wr = wr.replace([np.inf, -np.inf], np.nan).fillna(-50)
    return pd.Series(wr, name='wr')


def ao(high, low, s=5, l=34, fillna=False):
#def ao(data, s=5, l=34, high_col='High', low_col='Low', 
#       close_col='Close', vol_col='Volume', fillna=False):
    """Awesome Oscillator

    From: https://www.tradingview.com/wiki/Awesome_Oscillator_(AO)

    The Awesome Oscillator is an indicator used to measure market momentum. AO calculates the difference of a
    34 Period and 5 Period Simple Moving Averages. The Simple Moving Averages that are used are not calculated
    using closing price but rather each bar's midpoints. AO is generally used to affirm trends or to anticipate
    possible reversals.

    From: https://www.ifcm.co.uk/ntx-indicators/awesome-oscillator

    Awesome Oscillator is a 34-period simple moving average, plotted through the central points of the bars (H+L)/2,
    and subtracted from the 5-period simple moving average, graphed across the central points of the bars (H+L)/2.
    MEDIAN PRICE = (HIGH+LOW)/2
    AO = SMA(MEDIAN PRICE, 5)-SMA(MEDIAN PRICE, 34)

    where

    SMA — Simple Moving Average.

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        s(int): short period
        l(int): long period
        fillna(bool): if True, fill nan values with -50.

    Returns:
        pandas.Series: New feature generated.
    """
#    high = data[high_col]
#    low = data[low_col]

    mp = 0.5 * (high + low)
    ao = mp.rolling(int(s)).mean() - mp.rolling(int(l)).mean()

    if fillna:
        ao = ao.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(ao, name='ao')
