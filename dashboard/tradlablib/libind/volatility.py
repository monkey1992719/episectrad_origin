# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from .pyti import *
from .utils import *


#def average_true_range(high, low, close, n=14, fillna=False):
def atr(data, n, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """Average True Range (ATR)

    The indicator provide an indication of the degree of price volatility.
    Strong moves, in either direction, are often accompanied by large ranges,
    or large True Ranges.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_true_range_atr

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
    close = data[close_col]
    high = data[high_col]
    low = data[low_col]
    
    cs = close.shift(1)
    tr = high.combine(cs, max) - low.combine(cs, min)
    tr = ema(tr, n)
    if fillna:
        tr = tr.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(tr, name='atr')

def bb_bw_indicator(data, l, sd, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """
    Bandwidth.

    Formula:
    bw = u_bb - l_bb / m_bb
    """
    close = data[close_col].tolist()
    bb_bw = pd.Series(bollinger_bands.bandwidth(close, l, sd))
    if fillna:
        bb_bw = bb_bw.replace([np.inf, -np.inf], np.nan).fillna(50)
    return pd.Series(bb_bw, name='bb_bw')

def bb_pb_indicator(data, l, sd, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """
    Bandwidth.

    Formula:
    bw = u_bb - l_bb / m_bb
    """
    close = data[close_col].tolist()
    bb_pb = pd.Series(bollinger_bands.percent_b(close, l, sd))
    if fillna:
        bb_pb = bb_pb.replace([np.inf, -np.inf], np.nan).fillna(50)
    return pd.Series(bb_pb, name='bb_pb')

def bollinger_mavg(close, n=20, fillna=False):
    """Bollinger Bands (BB)

    N-period simple moving average (MA).

    https://en.wikipedia.org/wiki/Bollinger_Bands

    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
    mavg = close.rolling(n).mean()
    if fillna:
        mavg = mavg.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(mavg, name='mavg')


def bollinger_hband(close, n=20, ndev=2, fillna=False):
    """Bollinger Bands (BB)

    Upper band at K times an N-period standard deviation above the moving
    average (MA + Kdeviation).

    https://en.wikipedia.org/wiki/Bollinger_Bands

    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation

    Returns:
        pandas.Series: New feature generated.
    """
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    hband = mavg + ndev*mstd
    if fillna:
        hband = hband.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(hband, name='hband')


def bollinger_lband(close, n=20, ndev=2, fillna=False):
    """Bollinger Bands (BB)

    Lower band at K times an N-period standard deviation below the moving
    average (MA − Kdeviation).

    https://en.wikipedia.org/wiki/Bollinger_Bands

    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation

    Returns:
        pandas.Series: New feature generated.
    """
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    lband = mavg - ndev * mstd
    if fillna:
        lband = lband.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(lband, name='lband')


def bollinger_hband_indicator(close, n=20, ndev=2, fillna=False):
    """Bollinger High Band Indicator

    Returns 1, if close is higher than bollinger high band. Else, return 0.

    https://en.wikipedia.org/wiki/Bollinger_Bands

    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation

    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close]).transpose()
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    hband = mavg + ndev * mstd
    df['hband'] = 0.0
    df.loc[close > hband, 'hband'] = 1.0
    hband = df['hband']
    if fillna:
        hband = hband.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(hband, name='bbihband')


def bollinger_lband_indicator(close, n=20, ndev=2, fillna=False):
    """Bollinger Low Band Indicator

    Returns 1, if close is lower than bollinger low band. Else, return 0.

    https://en.wikipedia.org/wiki/Bollinger_Bands

    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation

    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close]).transpose()
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    lband = mavg - ndev * mstd
    df['lband'] = 0.0
    df.loc[close < lband, 'lband'] = 1.0
    lband = df['lband']
    if fillna:
        lband = lband.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(lband, name='bbilband')


def keltner_channel_central(high, low, close, n=10, fillna=False):
    """Keltner channel (KC)

    Showing a simple moving average line (central) of typical price.

    https://en.wikipedia.org/wiki/Keltner_channel

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """ 
    tp = (high + low + close) / 3.0
    tp = tp.rolling(n).mean()
    if fillna:
        tp = tp.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(tp, name='kc_central')


def keltner_channel_hband(high, low, close, n=10, fillna=False):
    """Keltner channel (KC)

    Showing a simple moving average line (high) of typical price.

    https://en.wikipedia.org/wiki/Keltner_channel

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
    tp = ((4 * high) - (2 * low) + close) / 3.0
    tp = tp.rolling(n).mean()
    if fillna:
        tp = tp.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(tp, name='kc_hband')


def keltner_channel_lband(high, low, close, n=10, fillna=False):
    """Keltner channel (KC)

    Showing a simple moving average line (low) of typical price.

    https://en.wikipedia.org/wiki/Keltner_channel

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
    tp = ((-2 * high) + (4 * low) + close) / 3.0
    tp = tp.rolling(n).mean()
    if fillna:
        tp = tp.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(tp, name='kc_lband')


def keltner_channel_hband_indicator(high, low, close, n=10, fillna=False):
    """Keltner Channel High Band Indicator (KC)
    Important: This function has been updated. Original one was not functional.
    
    Returns 1, if close is higher than keltner high band channel. Else,
    return 0.

    https://en.wikipedia.org/wiki/Keltner_channel

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
    hband = keltner_channel_hband(high, low, close, n)
    kc_hband_ind = np.clip(np.sign(close-hband), 0, 1)

    if fillna:
        kc_hband_ind = kc_hband_ind.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(kc_hband_ind, name='kc_hband_ind')

def keltner_channel_lband_indicator(high, low, close, n=10, fillna=False):
    """Keltner Channel Low Band Indicator (KC)
    Important: This function has been updated. Original one was not functional.
    
    Returns 1, if close is lower than keltner low band channel. Else, return 0.

    https://en.wikipedia.org/wiki/Keltner_channel

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
    lband = keltner_channel_lband(high, low, close, n)
    kc_lband_ind = np.clip(np.sign(lband-close), 0, 1)

    if fillna:
        kc_lband_ind = kc_lband_ind.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(kc_lband_ind, name='kc_lband_ind')

def keltner_channel(data, n, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """ Keltner Channel 
    """
    kc = pd.DataFrame()
    high    = data[high_col]
    low     = data[low_col]
    close   = data[close_col]

    kc_central  = keltner_channel_central(high, low, close, n)
    kc_hband    = keltner_channel_hband(high, low, close, n)
    kc_lband    = keltner_channel_lband(high, low, close, n)
    
    kc['kc_central']= kc_central
    kc['kc_hband']  = kc_hband
    kc['kc_lband']  = kc_lband
    
    return kc
    
#def donchian_channel_hband(close, n=20, fillna=False):
def donchian_channel_hband(data, n, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """Donchian channel (DC)

    The upper band marks the highest price of an issue for n periods.

    https://www.investopedia.com/terms/d/donchianchannels.asp

    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
    close = data[close_col]
    
    hband = close.rolling(n).max()
    if fillna:
        hband = hband.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(hband, name='dc_hband')


#def donchian_channel_lband(close, n=20, fillna=False):
def donchian_channel_lband(data, n, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """Donchian channel (DC)

    The lower band marks the lowest price for n periods.

    https://www.investopedia.com/terms/d/donchianchannels.asp

    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
    close = data[close_col]

    lband = close.rolling(n).min()
    if fillna:
        lband = lband.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(lband, name='dc_lband')


def donchian_channel_hband_indicator(close, n=20, fillna=False):
#def donchian_channel_hband_indicator(data, n, high_col='High', low_col='Low', 
#                       close_col='Close', vol_col='Volume', fillna=False):
    """Donchian High Band Indicator

    Returns 1, if close is higher than donchian high band channel. Else,
    return 0.

    https://www.investopedia.com/terms/d/donchianchannels.asp

    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
#    close = data[close_col]

    df = pd.DataFrame([close]).transpose()
    df['hband'] = 0.0
    hband = close.rolling(n).max()
    df.loc[close >= hband, 'hband'] = 1.0
    hband = df['hband']
    if fillna:
        hband = hband.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(hband, name='dc_hband_ind')


def donchian_channel_lband_indicator(close, n=20, fillna=False):
#def donchian_channel_lband_indicator(data, n, high_col='High', low_col='Low', 
#                       close_col='Close', vol_col='Volume', fillna=False):
    """Donchian Low Band Indicator

    Returns 1, if close is lower than donchian low band channel. Else, return 0.

    https://www.investopedia.com/terms/d/donchianchannels.asp

    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
#    close = data[close_col]

    df = pd.DataFrame([close]).transpose()
    df['lband'] = 0.0
    lband = close.rolling(n).min()
    df.loc[close <= lband, 'lband'] = 1.0
    lband = df['lband']
    if fillna:
        lband = lband.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(lband, name='dc_lband_ind')

def donchian_channel_indicator(data, n, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """Donchian channel Indicator


    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.

    Returns:
        pandas.Series: New feature generated.
    """
    dci_ = pd.DataFrame()
    dc_hband = donchian_channel_hband(data, n)
    dc_lband = donchian_channel_lband(data, n)
    dci_['dc_hband'] = dc_hband
    dci_['dc_lband'] = dc_lband
    
    return dci_



