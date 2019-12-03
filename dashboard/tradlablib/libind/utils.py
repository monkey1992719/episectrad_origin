# -*- coding: utf-8 -*-
import math
import pandas as pd
import numpy as np
import random

def dropna(df):
    """Drop rows with "Nans" values
    """
    df = df[df < math.exp(709)] # big number
    df = df[df != 0.0]
    df = df.dropna()
    return df

def ema(series, periods):
    sma = series.rolling(window=periods, min_periods=periods).mean()[:periods]
    rest = series[periods:]
    return pd.concat([sma, rest]).ewm(span=periods, adjust=False).mean()

def randlist(start, end, num): 
    """ Generate Random num list of numbers between star & end
    
    Return:
    Returns list of random numbers.
    """
    res = [] 
  
    for j in range(num): 
        res.append(random.randint(start, end)) 
  
    return res 

