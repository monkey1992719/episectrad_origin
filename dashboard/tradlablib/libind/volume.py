# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from .utils import *
from .pyti import *

   
    
def acc_dist_index(data, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """Accumulation/Distribution Index (ADI)

    Acting as leading indicator of price movements.

    https://en.wikipedia.org/wiki/Accumulation/distribution_index

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    high    = data[high_col]
    low     = data[low_col]
    close   = data[close_col]
    volume  = data[vol_col]
    
    clv = ((close - low) - (high - close)) / (high - low)
    clv = clv.fillna(0.0) # float division by zero
    ad = clv * volume
    ad = ad + ad.shift(1)
    if fillna:
        ad = ad.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(ad, name='acc')

def chaikin_money_flow(data, n, high_col='High', low_col='Low', 
                       close_col='Close', vol_col='Volume', fillna=False):
    """Chaikin Money Flow (CMF)

    It measures the amount of Money Flow Volume over a specific period.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_money_flow_cmf

    Args:
        data        : pandas DataFrame
        high_col    : High column name in data
        low_col     : Low column name in data
        close_col   : Close column name in data
        vol_col     : Volume column name in data
        
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
    
    mfv = ((close - low) - (high - close)) / (high - low)
    mfv = mfv.fillna(0.0) # float division by zero
    mfv *= volume
    cmf = mfv.rolling(n).sum() / volume.rolling(n).sum()
    if fillna:
        cmf = cmf.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(cmf, name='cmf')


def chaikin_oscillator(data, periods_short=3, periods_long=10, high_col='High',
                       low_col='Low', close_col='Close', vol_col='Volume', fillna=False):
    """
    Chaikin Oscillator
    Source: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_oscillator
    Params: 
        data: pandas DataFrame
        periods_short: period for the shorter EMA (3 days recommended)
        periods_long: period for the longer EMA (10 days recommended)
        high_col: the name of the HIGH values column
        low_col: the name of the LOW values column
        close_col: the name of the CLOSE values column
        vol_col: the name of the VOL values column
        
    Returns:
        copy of 'data' DataFrame with 'ch_osc' column added
    """
    ac = pd.Series([])
    ac1 = pd.Series([])
    val_last = 0
	
    for index, row in data.iterrows():
        if row[high_col] != row[low_col]:
            val = val_last + ((row[close_col] - row[low_col]) - (row[high_col] - row[close_col])) / \
                             (row[high_col] - row[low_col]) * row[vol_col]
        else:
            val = val_last
        #ac.set_value(index, val) # Removed for set_value Future Depricated warning
        ac.at[index] = val
    val_last = val

    ema_long = ac.ewm(ignore_na=False, min_periods=0, com=periods_long, adjust=True).mean()
    ema_short = ac.ewm(ignore_na=False, min_periods=0, com=periods_short, adjust=True).mean()
    ch_osc = ema_short - ema_long
    if fillna:
        ch_osc = ch_osc.replace([np.inf, -np.inf], np.nan).fillna(0)

    return pd.Series(ch_osc, name='ch_osc')


def ease_of_movement(data, n, high_col='High', low_col='Low', close_col='Close', vol_col='Volume', fillna=False):
    """Ease of movement (EoM, EMV)

    It relate an asset's price change to its volume and is particularly useful
    for assessing the strength of a trend.

    https://en.wikipedia.org/wiki/Ease_of_movement

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

    emv = (high.diff(1) + low.diff(1)) * (high - low) / (2 * volume)
    emv = emv.rolling(n).mean()
    if fillna:
        emv = emv.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(emv, name='eom_' + str(n))

def on_balance_volume(close, volume, fillna=False):
    """On-balance volume (OBV)

    It relates price and volume in the stock market. OBV is based on a
    cumulative total volume.

    https://en.wikipedia.org/wiki/On-balance_volume

    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close, volume]).transpose()
    df['OBV'] = 0
    c1 = close < close.shift(1)
    c2 = close > close.shift(1)
    if c1.any():
        df.loc[c1, 'OBV'] = - volume
    if c2.any():
        df.loc[c2, 'OBV'] = volume
    obv = df['OBV']
    if fillna:
        obv = obv.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(obv, name='obv')


def on_balance_volume_mean(close, volume, n=10, fillna=False):
    """On-balance volume mean (OBV mean)

    It's based on a cumulative total volume.

    https://en.wikipedia.org/wiki/On-balance_volume

    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close, volume]).transpose()
    df['OBV'] = 0
    c1 = close < close.shift(1)
    c2 = close > close.shift(1)
    if c1.any():
        df.loc[c1, 'OBV'] = - volume
    if c2.any():
        df.loc[c2, 'OBV'] = volume
    obv = df['OBV'].rolling(n).mean()
    if fillna:
        obv = obv.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(obv, name='obv')


def force_index(close, volume, n=2, fillna=False):
    """Force Index (FI)

    It illustrates how strong the actual buying or selling pressure is. High
    positive values mean there is a strong rising trend, and low values signify
    a strong downward trend.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:force_index

    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    fi = close.diff(n) * volume.diff(n)
    if fillna:
        fi = fi.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(fi, name='fi_'+str(n))

def vi_indicator(close, volume, type='PVI', fillna=False):
    """Volume Index Positive (PVI) or Negative (NVI)
    Default is positive volume index (PVI).

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    if type == 'PVI':
        vi_indx = pd.Series(volume_index.positive_volume_index(close, volume))
    elif type == 'NVI':
        vi_indx = pd.Series(volume_index.negative_volume_index(close, volume))

    if fillna:
        vi_indx = vi_indx.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(vi_indx, name=type)
 
def volume_index_indicator(data, high_col='High', low_col='Low', 
                 close_col='Close', vol_col='Volume', fillna=False):
    """Volume Index Positive (PVI) or Negative (NVI)
    Default is positive volume index (PVI).

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    close = data[close_col].tolist()
    volume = data[vol_col].tolist()
    
    vo_index = pd.DataFrame()
    pvi = vi_indicator(close, volume, 'PVI')
    nvi = vi_indicator(close, volume, 'NVI')
    vo_index['PVI'] = pvi
    vo_index['NVI'] = nvi    

    return vo_index
    
def vo_indicator(data, short_length, long_length, high_col='High', low_col='Low', 
                 close_col='Close', vol_col='Volume', fillna=False):
    """Volume Oscillator (VO)

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    volume = data[vol_col].tolist()
    vo = pd.Series(volume_oscillator.volume_oscillator(volume, short_length, long_length))
    if fillna:
        vo = vo.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(vo, name='vo')
 

def volume_price_trend(close, volume, fillna=False):
    """Volume-price trend (VPT)

    Is based on a running cumulative volume that adds or substracts a multiple
    of the percentage change in share price trend and current volume, depending
    upon the investment's upward or downward movements.

    https://en.wikipedia.org/wiki/Volume%E2%80%93price_trend

    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    vpt = volume * ((close - close.shift(1)) / close.shift(1))
    vpt = vpt.shift(1) + vpt
    if fillna:
        vpt = vpt.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(vpt, name='vpt')


def negative_volume_index(close, volume, fillna=False):
    """Negative Volume Index (NVI)

    From: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:negative_volume_inde

    The Negative Volume Index (NVI) is a cumulative indicator that uses the change in volume to decide when the
    smart money is active. Paul Dysart first developed this indicator in the 1930s. [...] Dysart's Negative Volume
    Index works under the assumption that the smart money is active on days when volume decreases and the not-so-smart
    money is active on days when volume increases.

    The cumulative NVI line was unchanged when volume increased from one period to the other. In other words,
    nothing was done. Norman Fosback, of Stock Market Logic, adjusted the indicator by substituting the percentage
    price change for Net Advances.

    This implementation is the Fosback version.

    If today's volume is less than yesterday's volume then:
        nvi(t) = nvi(t-1) * ( 1 + (close(t) - close(t-1)) / close(t-1) )
    Else
        nvi(t) = nvi(t-1)

    Please note: the "stockcharts.com" example calculation just adds the percentange change of price to previous
    NVI when volumes decline; other sources indicate that the same percentage of the previous NVI value should
    be added, which is what is implemented here.

    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        fillna(bool): if True, fill nan values with 1000.

    Returns:
        pandas.Series: New feature generated.

    See also:
    https://en.wikipedia.org/wiki/Negative_volume_index
    """
    price_change = close.pct_change()
    vol_decrease = (volume.shift(1) > volume)

    nvi = pd.Series(data=np.nan, index=close.index, dtype='float64', name='nvi')

    nvi.iloc[0] = 1000
    for i in range(1,len(nvi)):
        if vol_decrease.iloc[i]:
            nvi.iloc[i] = nvi.iloc[i - 1] * (1.0 + price_change.iloc[i])
        else:
            nvi.iloc[i] = nvi.iloc[i - 1]

    if fillna:
        nvi = nvi.replace([np.inf, -np.inf], np.nan).fillna(1000) # IDEA: There shouldn't be any na; might be better to throw exception

    return pd.Series(nvi, name='nvi')

# TODO

def put_call_ratio():
    # will need options volumes for this put/call ratio

    """Put/Call ratio (PCR)
    https://en.wikipedia.org/wiki/Put/call_ratio
    """
    # TODO
    return
