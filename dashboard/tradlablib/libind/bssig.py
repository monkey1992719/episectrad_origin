# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys

from .momentum import *
from .trend import *
from .utils import *
from .volatility import *

""" 
    bssact_ic functions
    Buy and Sell active for indicator with short name ic
        1: Active, 0: Not Active
        Return:
        bact: Array of Buy Active
        sact: Array of Sell Active
"""


def get_bssig(bact, sact):
    """ Get Buy/Sell signal instances.
        Signal when 0 to 1    
    Args:
        bact: Buy Active (1:Active, 0:Non Active)
        sact: Sell Active (1:Active, 0:Non Active)
    
    Returns:
        Array of indices for Buy and Sell starting with Buy. 
    """
    baa = np.array(bact)
    saa = np.array(sact)
    
    assert(baa.size == saa.size), 'Unequal lengths for Buy Active and Sell Active.'
    
    bssig = np.array([])
    sel = 1
    for idx in range(baa.size-1): # baa.size = saa.size
        if sel == 1:
            tempa = baa
        elif sel == -1:
            tempa = saa
        
        if tempa[idx] == 0 and tempa[idx+1] == 1:
            bssig = np.append(bssig, idx)
            sel = -1*sel
    
    bssig = bssig.astype(int)
    
    return bssig

def get_bssig2(bact, sact):
    """ Get Buy/Sell signal instances.
        Signal when 1 to 0
    Args:
        bact: Buy Active (1:Active, 0:Non Active)
        sact: Sell Active (1:Active, 0:Non Active)
    
    Returns:
        Array of indices for Buy and Sell starting with Buy.
    """
    baa = np.array(bact)
    saa = np.array(sact)
    
    assert(baa.size == saa.size), 'Unequal lengths for Buy Active and Sell Active.'
    
    bssig = np.array([])
    sel = 1
    for idx in range(baa.size-1): # baa.size = saa.size
        if sel == 1:
            tempa = baa
        elif sel == -1:
            tempa = saa
        
        if tempa[idx] == 1 and tempa[idx+1] == 0:
            bssig = np.append(bssig, idx)
            sel = -1*sel
    
    bssig = bssig.astype(int)
    
    return bssig


def bsact_bb(data, n, ndev):
    # Bollinger Bands
    bact = bollinger_lband_indicator(data['Close'], n, ndev)
    sact = bollinger_hband_indicator(data['Close'], n, ndev)
    
    return bact, sact
    
def bsact_dc(data, n):
    # Donchain Channels
    bact = donchian_channel_hband_indicator(data['Close'], n)
    sact = donchian_channel_lband_indicator(data['Close'], n)
    
    return bact, sact

def bsact_kc(data, n):
    # Keltner Channel/Bands
    bact = keltner_channel_hband_indicator(data['High'], data['Low'], data['Close'], n)
    sact = keltner_channel_lband_indicator(data['High'], data['Low'], data['Close'], n)
    
    return bact, sact

def bsact_cross(in1, in2):
    # Crossovers 
    #       buy - in1 crosses above in2
    #       sell- in1 crosses below in2
    # MA Cross: in1 = mafast, in2 = maslow
    # MACD: in1 = macdt, in2 = macdsig
    # Directioinal Movement Index: in1 = DMI+, in2 = DMI-
    # Vortex: in1 = +VI, in2 = -VI
    diffb = np.array(in1) - np.array(in2)
    diffs = np.array(in2) - np.array(in1)
    
    bact = np.sign(diffb)
    sact = np.sign(diffs)
    bact = np.clip(bact, 0, 1)
    sact = np.clip(sact, 0, 1)

    return bact, sact

def bsact_stoch(stok, stod):
    # Stochastic
    stoknp = np.array(stok)
    stodnp = np.array(stod)

    bact, sact = bsact_cross(stoknp, stodnp)
    for idx in range(bact.size): # bact.size = sact.size
        if stoknp[idx] >= 20 and stodnp[idx] >= 20:
            bact[idx] = 0
        if stoknp[idx] <= 80 and stodnp[idx] <= 80:
            sact[idx] = 0
    
    return bact, sact

def bsact_zcross(ind):
    # Zero Crossing type
    # Awesome Oscillator, Coppock Curve, KST, Momentum, TRIX, Price Oscillator
    bact = np.sign(np.array(ind))
    sact = -1*bact
    bact = np.clip(bact, 0, 1)
    sact = np.clip(sact, 0, 1)

    return bact, sact

def bsact_sovbs(ind, ovb, ovs):
    # Single indicator line with overbought and oversold
    # Commodity Channel Index (CCI): ovb = +100, ovs = -100
    # Relative Strength Index (RSI): ovb = 70, ovs = 30
    # Stochastic RSI: ovb = 80, ovs = 20
    # Williams %R: ovb = 80, ovs = 20
    # True Strength Index (TSI): ovb = 25, ovs = -25
    # *Note*: Use get_bssig2 for all the absbove indicators.
    indnp = np.array(ind)
    indlen = indnp.size
    bact = np.array([1]*indlen)
    sact = np.array([1]*indlen)
    
    for idx in range(indlen):
        if indnp[idx] > ovs:
            bact[idx] = 0
        if indnp[idx] < ovb:
            sact[idx] = 0
    
    return bact, sact

def bsact_atr(close, atr):
    # Average True Range
    closenp = np.array(close)
    atrnp   = np.array(atr)
    
    cplus   = closenp+atrnp
    cminus  = closenp-atrnp
    
    bact = np.array([0]*closenp.size)
    sact = np.array([0]*closenp.size)
    
    for idx in range(closenp.size-1):
        if closenp[idx+1] > cplus[idx]:
            bact[idx+1] = 1
        if closenp[idx+1] < cminus[idx]:
            sact[idx+1] = 1
    
    return bact, sact


