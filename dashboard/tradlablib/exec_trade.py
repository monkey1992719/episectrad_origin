# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from pandas import DataFrame

from .libind.bssig import *
from .libind.momentum import *
from .libind.trend import *
from .libind.utils import *
from .libind.volatility import *


from .libind.pyti.simple_moving_average import (
    simple_moving_average as sma
    )

from dashboard.tradlablib import model_guilib

import configparser

from dashboard.tradlablib.indicatorparameter import *    
from dashboard.tradlablib import chartpattern as cp
from dashboard.tradlablib import pricebarpattern as pp

config = configparser.ConfigParser()
ini = config.read('dashboard/tradlablib/params.ini')

commcrg = 0.02 # Default value of trade commission charges

def get_periods(acts):
    startpos = 0
    endpos = 0
    periods = []
    for i in range(len(acts)-1):
        if acts[i] == 0 and acts[i+1] == 1:
            startpos = i + 1
        if acts[i] == 1 and acts[i+1] == 0:
            endpos = i
            if endpos >= startpos:
                periods.append([startpos, endpos])

    return periods

def get_periods1(acts):
    periods = []
    for i in range(len(acts)):
        periods.append([acts[i]["start"], acts[i]["end"]])

    return periods

def get_periods2(signals):
    startpos = 0
    endpos = 0
    periods = []

    for i in range(1, len(signals)):

        if signals[i-1] != signals[i]:
            endpos = i - 1
            if endpos >= startpos and startpos != 0 and signals[i-1] != 0:
                periods.append([startpos, endpos, signals[i-1]])
            startpos = i

    return periods

def get_acts(bssig, stopsig, trendsig, sigtype):
    #get active periods
    acts = []

    for i in range(len(bssig)):
        start = bssig[i]
        end = stopsig[i]
        trend = trendsig[i]
        if (i+sigtype) % 2 == 1:
            buysell = 'BUY'
        else:
            buysell = 'SELL'

        acts.append({'start': start, 'end': end, 'trend': trend, 'buysell': buysell})

    return acts

def trade_returns1(close, periods, bssig, commcrg=0.02):
    ''' Get Stats with close and buy/sell signal
        
    '''
    besttarget = 0
    beststoploss = 0
    allprofit = 0.0
    allloss = 0.0

    allprofitmoney = 0.0
    alllossmoney = 0.0

    maxlosingstreak = 0
    maxwinningstreak = 0

    losingcol = 0
    winningcol = 0

    allwinn = 0
    alllossn = 0

    allbuytime = 0
    allselltime = 0
    for period in periods:
        tmp = close[period[0]:period[1]]
        if len(tmp) == 0:
            continue
        enterprice = close[period[0]]

        maxv = max(close[period[0]:period[1]])
        minv = min(close[period[0]:period[1]])
        target = (maxv-enterprice)/enterprice*100
        stoploss = (enterprice-minv)/enterprice*100

        if bssig[period[0]] == -1: # if sell signal invert
            temp = target
            target = stoploss
            stoploss = temp

        besttarget += target
        beststoploss += stoploss

        allbuytime += bssig[period[0]:period[1]].tolist().count(1)
        allselltime += bssig[period[0]:period[1]].tolist().count(-1)

        index = period[0]
        prestate = ''
        profit = 0.0
        loss = 0.0
        profitmoney = 0.0
        lossmoney = 0.0
        winstreak = 0
        lossstreak = 0
        winn = 0
        lossn = 0

        while index <= period[1]:
            state = ''
            if close[index] > enterprice:
                profit += (close[index] - enterprice)/enterprice
                profitmoney += close[index] - enterprice
                winn += 1
                state = 'Win'
                if prestate == '':
                    prestate = state
            elif close[index] < enterprice:
                lossn += 1
                loss += (enterprice - close[index])/enterprice
                lossmoney += enterprice - close[index]
                state = 'Loss'
                if prestate == '':
                    prestate = state

            if state == prestate and state == 'Win':
                winstreak += 1

            if state == prestate and state == 'Loss':
                lossstreak += 1
           
            if prestate != state or index == period[1]:
                if bssig[period[0]] == -1: # if sell signal invert
                    temp = winstreak
                    winstreak = lossstreak
                    lossstreak = temp
                
                if maxwinningstreak < winstreak:
                    maxwinningstreak = winstreak
                
                if maxlosingstreak < lossstreak:
                    maxlosingstreak = lossstreak

            prestate = state
            index += 1

        if bssig[period[0]] == -1: # if sell signal invert
            temp = profit
            profit = loss
            loss = temp

            temp = winn
            winn = lossn
            lossn = temp

            temp = profitmoney
            profitmoney = lossmoney
            lossmoney = temp

        allprofit += profit
        allloss += loss

        allwinn += winn
        alllossn += lossn

        allprofitmoney += profitmoney/(winn if winn>0 else 1)
        alllossmoney += lossmoney/(lossn if lossn>0 else 1)

    periodscnt = len(periods)
    if periodscnt == 0:
        periodscnt = 1
    besttarget /= periodscnt
    beststoploss /= periodscnt
    tmp = allwinn+alllossn
    if tmp == 0:
        tmp = 1
    winlossratio = allwinn/tmp*100

    avbuytime = allbuytime / periodscnt
    avselltime = allselltime / periodscnt

    tmp = allwinn
    if tmp == 0:
        tmp = 1
    avprofit = allprofit / tmp
    tmp = alllossn
    if tmp == 0:
        tmp = 1
    avloss = allloss / tmp

    # allprofitmoney /= periodscnt
    # alllossmoney /= periodscnt
        
    # return {'besttarget':besttarget, 'beststoploss':beststoploss, 'winlossratio':winlossratio, 'winn':allwinn, 'lossn':alllossn, 
    #         'maxlosingstreak':maxlosingstreak, 'maxwinningstreak':maxwinningstreak, 'avbuytime':avbuytime, 'avselltime':avselltime,
    #         'avprofit':avprofit,'avloss':avloss, 'avprofitmoney':allprofitmoney, 'avlossmoney':alllossmoney}

    winlossratio1 = allprofitmoney/alllossmoney
    return {'winlossratio':winlossratio1}  

def trade_returns(data, bssig, commcrg=0.20): 
    """ Calculate the return matrix for each buy and sell signal.
    
    Return:
    Trade returns in percentage.
    """
    seedmoney = 100

    sig = []
    money = seedmoney
    value = [0]*len(bssig)
    tradeprice = np.array(data)[np.array(bssig)]

    if len(bssig) == 1:
        return ['BUY'], [money*(1-commcrg/100)]

    for x in range(len(bssig)):
        if x%2 == 0: # Buy case
            sig.append('BUY')
            value[x]= money*(1-commcrg/100)
            #numunit = value[x]/np.array(data)[bssig[x]]
            numunit = value[x]/tradeprice[x]
        else: # Sell case
            sig.append('SELL')
            #money = np.array(data)[bssig[x]]*numunit*(1-commcrg/100)
            money = tradeprice[x]*numunit*(1-commcrg/100)
            value[x] = money
    
    trp = np.array(value) - seedmoney

    return sig, trp


def get_bsrets(pdf, bssig, commcrg=0.02):
    """ Make the retruns frame for the trading
    
    Return:
    bsrets: Buy/Sell and Return frame.
    """
    sig, tra = trade_returns(pdf['Close'], bssig, commcrg)
            
    bsrets = pd.DataFrame()
    bsrets['Date'] = np.array(pdf['Date'])[np.array(bssig)]
    bsrets['Price'] = np.array(pdf['Close'])[np.array(bssig)]
    bsrets['Signal'] = sig
    bsrets['Returns%'] = tra
    
    return bsrets


def get_stopsig(pts, bssig):
    stopact = []
    trendact = []
    for i in range(len(bssig)):
        if i == len(bssig)-1:
            spts = pts[bssig[i]:]
        else:
            spts = pts[bssig[i]:bssig[i+1]]

        trend, stopind = cp.getdirection(spts)
        stopind = stopind + bssig[i]
        stopact.append(stopind)
        trendact.append(trend)

    return stopact, trendact

def trade_with_ao(pdf, ao_short_length, ao_long_length, retact=False):
    """ Trade with Awesome oscillator with its parameters.
    
    Return:
        For default, retact=False
        apltdt: Additional Plot data frame.
        bstret: Buy/Sell and Trade Returns frame.  
        
        When retact=True
        bact:   Active signal for Buy
        sact:   Active signal for Sell
    """
    ao_ = ao(pdf['High'], pdf['Low'], ao_short_length, ao_long_length, fillna=False)
    
    bact, sact = bsact_zcross(ao_)
    
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['AO'] = ao_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(ao_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']

    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets

def trade_with_bb(pdf, bb_length, bb_std_dev, close_col, retact=False):
    """ Trade with Bollinger Band with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
   
    upr_bb = bollinger_hband(pdf[close_col], bb_length, bb_std_dev, fillna=False)
    mid_bb = bollinger_mavg(pdf[close_col], bb_length, fillna=False)
    lwr_bb = bollinger_lband(pdf[close_col], bb_length, bb_std_dev, fillna=False)

    bact, sact = bsact_bb(pdf, bb_length, bb_std_dev)

    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['UPRBB'] = upr_bb
    apltdt['MIDBB'] = mid_bb
    apltdt['LWRBB'] = lwr_bb

    dtbss = pd.DataFrame()
    dtbss['ub'] = upr_bb
    dtbss['lb'] = lwr_bb
    dtbss.fillna(0, inplace=True)
    
    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(mid_bb, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets    
    
def trade_with_atr(pdf, atr_length, retact=False):
    """ Trade with Average True Range with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """

    atr_ = atr(pdf, atr_length)
    
    bact, sact = bsact_atr(pdf['Close'], atr_)
    
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['ATR'] = atr_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(atr_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']

    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets
    
def trade_with_cc(pdf, cc_length, retact=False):
    """ Trade with Coppock Curve with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    cc_ = copp(pdf, cc_length)

    bact, sact = bsact_zcross(cc_)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['CC'] = cc_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(cc_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']

    if retact == True:
        return sigtype, stopsig, trendsig, bssig
    
    return apltdt, bsrets    
    
def trade_with_po(pdf, po_short_length, po_long_length, close_col, retact=False):
    """ Trade with Price Oscillator with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    po_ = po_indicator(data=pdf, short_length=po_short_length, long_length=po_long_length, close_col=close_col)

    bact, sact = bsact_zcross(po_)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['PO'] = po_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(po_, bssig)

    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     
    
def trade_with_cci(pdf, cci_length, cci_mul, retact=False):
    """ Trade with Commodity Channel Index with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    ovb = 100 
    ovs = -100
    cci_ = cci(pdf, cci_length, cci_mul, fillna=False)
    
    bact, sact = bsact_sovbs(cci_, ovb, ovs)
    sigtype = 2 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['CCI'] = cci_

    bssig = get_bssig2(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(cci_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']

    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     
    
def trade_with_dc(pdf, len, retact=False):
    """ Trade with Donchain Channels with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    dc_bands = donchian_channel_indicator(pdf, len)

    bact, sact = bsact_dc(pdf, len)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt = pd.concat([apltdt, dc_bands], axis=1)

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(dc_bands['dc_hband'], bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']

    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     
    
def trade_with_adx(pdf, dmi_length, retact=False):
    """ Trade with Average directional movement index with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    adx_pos_ =  adx_pos(pdf['High'], pdf['Low'], pdf['Close'], dmi_length)
    adx_neg_ =  adx_neg(pdf['High'], pdf['Low'], pdf['Close'], dmi_length)
        
    bact, sact = bsact_cross(adx_pos_, adx_neg_)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['adx_pos'] = adx_pos_
    apltdt['adx_neg'] = adx_neg_

    # # get adx
    # sub = abs(adx_pos_ - adx_neg_)
    # sm = adx_pos_ + adx_neg_
    # sm.replace(0, 1)

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)

    stopsig, trendsig = get_stopsig(adx_pos_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']

    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     
    
def trade_with_stchrsi(pdf, stch_length, close_col, retact=False):
    """ Trade with Average directional movement index with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    ovb = 80
    ovs = 20
    stchrsi = stchrsi_indicator(data=pdf, n=stch_length, close_col=close_col)
    
    bact, sact = bsact_sovbs(stchrsi, ovb, ovs)
    sigtype = 2 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['STCHRSI'] = stchrsi

    bssig = get_bssig2(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(stchrsi, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']

    if retact == True:
        return sigtype, stopsig, trendsig, bssig
    
    return apltdt, bsrets     
    
def trade_with_tsi(pdf, tsi_long_length, tsi_short_length, retact=False):
    """ Trade with True Strength Index with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    ovb = 25
    ovs = -25
    tsi_ = tsi(pdf, tsi_long_length, tsi_short_length)
    
    bact, sact = bsact_sovbs(tsi_, ovb, ovs)
    sigtype = 2 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['TSI'] = tsi_

    bssig = get_bssig2(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(tsi_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     
      
def trade_with_wpr(pdf, wpr_length, retact=False):
    """ Trade with William %R with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    wpr_ = wr(pdf, wpr_length)
    
    ovb = 80
    ovs = 20
    bact, sact = bsact_sovbs(wpr_, ovb, ovs)
    sigtype = 2 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['WPR'] = wpr_

    bssig = get_bssig2(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(wpr_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     
    
def trade_with_kc(pdf, kc_length, retact=False):
    """ Trade with Keltner Channels with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    kc_bands = keltner_channel(pdf, kc_length)
    
    bact, sact = bsact_kc(pdf, kc_length)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt = pd.concat([apltdt, kc_bands], axis=1)

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(kc_bands['kc_central'], bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     
    
def trade_with_macd(pdf, lenfast, lenslow, lensig, close_col, retact=False):
    """ Trade with MACD with fast, slow and signal parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bsrets: Buy/Sell and Returns frame.
    """
    #This is alternate method. Lib funciton available so it is disabled.
    #emafast = ema_indicator(pdf['Close'], lenfast, fillna=True)
    #emaslow = ema_indicator(pdf['Close'], lenslow, fillna=True)
    #macdt = emafast - emaslow
    #macdsig = ema_indicator(macd, lensig, fillna=True)
    macdt   = macd(pdf[close_col], lenfast, lenslow, fillna=False)
    macdsig = macd_signal(pdf[close_col], lenfast, lenslow, lensig, fillna=False)

    bact, sact = bsact_cross(macdt, macdsig)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['MACD']      = macdt
    apltdt['MACDSig']   = macdsig

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(macdsig, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets 


def trade_with_macross(pdf, matype, lenfast, lenslow, retact=False):
    """ Trade with MA Cross wih fast and slow parameters.
        
    Return:
    apltdt: Additional Plot data frame.
    """
    if matype == 'SMA':
        return trade_with_sma_cross(pdf, lenfast, lenslow, retact)
    elif matype == 'EMA':
        return trade_with_ema_cross(pdf, lenfast, lenslow, retact)
    elif matype == 'WMA':
        return trade_with_wma_cross(pdf, lenfast, lenslow, retact)
    else:
        return trade_with_sma_cross(pdf, lenfast, lenslow, retact)
        
def trade_with_mom(pdf, mom_length, retact=False):
    """ Trade with Momentum with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    mom_ = mom_indicator(pdf, mom_length)

    bact, sact = bsact_zcross(mom_)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['MOM'] = mom_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(mom_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     

def trade_with_ema_cross(pdf, lenfast, lenslow, retact=False):
    """ Trade with EMA with fast and slow parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bsrets: Buy/Sell and Returns frame.
    """
    emafast = ema_indicator(pdf['Close'], lenfast, fillna=True)
    emaslow = ema_indicator(pdf['Close'], lenslow, fillna=True)
    
    bact, sact = bsact_cross(emafast, emaslow)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['EMA'+str(lenfast)] = emafast
    apltdt['EMA'+str(lenslow)] = emaslow

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(emafast, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets 
    
def trade_with_rsi(pdf, rsi_length, close_col, retact=False):
    """ Trade with Relative Strength Index with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    ovb = 70 
    ovs = 30
    rsi_ = rsi(pdf[close_col], rsi_length)

    bact, sact = bsact_sovbs(rsi_, ovb, ovs)
    sigtype = 2 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['RSI'] = rsi_

    bssig = get_bssig2(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(rsi_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     

def trade_with_sma_cross(pdf, lenfast, lenslow, retact=False):
    """ Trade with SMA with fast and slow parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bsrets: Buy/Sell and Returns frame.
    """
    smafast = sma_indicator(pdf['Close'], lenfast, fillna=True)
    smaslow = sma_indicator(pdf['Close'], lenslow, fillna=True)
 
    bact, sact = bsact_cross(smafast, smaslow)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt = pd.DataFrame()
    apltdt['SMA'+str(lenfast)] = smafast
    apltdt['SMA'+str(lenslow)] = smaslow

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(smafast, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets 
    
def trade_with_trix(pdf, trix_length, retact=False):
    """ Trade with TRIX with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    trix_ = trix(pdf, trix_length)

    bact, sact = bsact_zcross(trix_)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['TRIX'] = trix_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(trix_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     

def trade_with_wma_cross(pdf, lenfast, lenslow, retact=False):
    """ Trade with SMA with fast and slow parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bsrets: Buy/Sell and Returns frame.
    """
    wmafast = wma_indicator(pdf['Close'], lenfast, fillna=True)
    wmaslow = wma_indicator(pdf['Close'], lenslow, fillna=True)
    
    bact, sact = bsact_cross(wmafast, wmaslow)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['WMA'+str(lenfast)] = wmafast
    apltdt['WMA'+str(lenslow)] = wmaslow

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(wmafast, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets

def trade_with_stoch(df, s_k, s_d, s_smooth, retact=False):
    """ Trade with Stochastic indicator.
    

    Return:
    apltdt: Additional Plot data frame.
    bsrets: Buy/Sell and Returns frame.
    """
    stok, stod = stochastic(df, s_k, s_d, s_smooth)
    
    bact, sact = bsact_stoch(stok, stod)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['STOK'] = stok
    apltdt['STOD'] = stod

    pdf = pd.DataFrame()    # This is unnecessary
    pdf['Date'] = df['Date']
    pdf['Close'] = df['Close']
    
    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(stok, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets 

def trade_with_voi(pdf, voi_length, retact=False):
    """ Trade with Vortex Indicator with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    voi_pos_ =  vortex_indicator_pos(pdf['High'], pdf['Low'], pdf['Close'], voi_length)
    voi_neg_ =  vortex_indicator_neg(pdf['High'], pdf['Low'], pdf['Close'], voi_length)
    
    bact, sact = bsact_cross(voi_pos_, voi_neg_)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()    
    apltdt['voi_pos'] = voi_pos_
    apltdt['voi_neg'] = voi_neg_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(voi_pos_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    if retact == True:
        return sigtype, stopsig, trendsig, bssig

    return apltdt, bsrets     

def trade_with_kst(pdf, kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, 
                   kst_sma_length_1, kst_sma_length_2, kst_sma_length_3, kst_sma_length_4, kst_sig_length, retact=False):
    """ Trade with KST Oscillator with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.
    """
    kst_ =  kst(pdf['Close'],  kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, kst_sma_length_1, 
            kst_sma_length_2, kst_sma_length_3, kst_sma_length_4)
    
    bact, sact = bsact_zcross(kst_)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
        
    apltdt = pd.DataFrame()
    apltdt['KST'] = kst_

    apltdt['KST_SIG'] = sma(kst_, kst_sig_length)

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(kst_, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']

    if retact == True:
        return sigtype, stopsig, trendsig, bssig
    
    return apltdt, bsrets     


def trade_with_cross2(pdf, first_plt, second_plt, retact=False):
    """ Trade with an Indicator vs another Indicator with its parameters.
    
    Return:
        For default, retact=False
        apltdt: Additional Plot data frame.
        bstret: Buy/Sell and Trade Returns frame.  
        
        When retact=True
        bact:   Active signal for Buy
        sact:   Active signal for Sell
    """
    bact, sact = bsact_cross(first_plt, second_plt)
    
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    # if retact == True:
    #     return sigtype, stopsig, trendsig, bssig
    
    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(first_plt, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']

    return bsrets, sigtype, stopsig, trendsig, bssig


def trade_with_threshold(pdf, plt, ovb, ovs, retact=False):
    """ Trade with an Indicator vs another Indicator with its parameters.
    
    Return:
        For default, retact=False
        apltdt: Additional Plot data frame.
        bstret: Buy/Sell and Trade Returns frame.  
        
        When retact=True
        bact:   Active signal for Buy
        sact:   Active signal for Sell
    """
    bact, sact = bsact_sovbs(plt, ovb, ovs)
    
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    
    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(plt, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    return bsrets, sigtype, stopsig, trendsig, bssig

def trade_with_crossv(pdf, plt, retact=False):
    """ Trade with an Indicator vs another Indicator with its parameters.
    
    Return:
        For default, retact=False
        apltdt: Additional Plot data frame.
        bstret: Buy/Sell and Trade Returns frame.  
        
        When retact=True
        bact:   Active signal for Buy
        sact:   Active signal for Sell
    """
    maxval = max(plt)
    minval = min(plt)
    plt2 = maxval - np.array(plt) + minval
    bact, sact = bsact_cross(plt, plt2)
    
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    
    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(plt, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    return bsrets, sigtype, stopsig, trendsig, bssig


def trade_with_pricebarpattern(pdf, pattern, retact=False):
    """ Trade with a pricebar pattern

    Return:
        For default, retact=False
        apltdt: Additional Plot data frame.
        bstret: Buy/Sell and Trade Returns frame.  
        
        When retact=True
        bact:   Active signal for Buy
        sact:   Active signal for Sell
    """
    data = pp.patternrecog(pdf, pattern)

    # bact, sact = bsact_cross(plt, plt2)
    
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    
    # bssig = get_bssig(bact, sact)
    bssig = np.array(data['indexes'])
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(pdf['Close'], bssig)

    # acts = get_acts(bssig, stopsig, trendsig, sigtype)
    # periods = get_periods1(acts)

    # bsact = bact.copy()
    # bsact = np.where(bsact==0, -1, bsact)
    
    # result = trade_returns1(pdf['Close'], periods, bsact)
    # bsrets['Returns%'] = result['winlossratio']
    
    return bsrets, sigtype, stopsig, trendsig, bssig


def trade_with_chartpattern(pdf, pattern, retact=False):
    """ Trade with a chart pattern

    Return:
        For default, retact=False
        apltdt: Additional Plot data frame.
        bstret: Buy/Sell and Trade Returns frame.  
        
        When retact=True
        bact:   Active signal for Buy
        sact:   Active signal for Sell
    """
    data = cp.recogchartpattern(pdf, pattern)
    fromindex = int(data['fromindex'])
    toindex = int(data['toindex'])
    
    
    # bact, sact = bsact_cross(plt, plt2)
    
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    
    # bssig = get_bssig(bact, sact)
    if pattern in cp.bullishpatternnames:
        bssig = [fromindex]
        stopsig = [toindex]
        trendsig = [1]
    else:
        bssig = [fromindex]
        stopsig = [toindex]
        trendsig = [-1]

    bsrets = get_bsrets(pdf, bssig, commcrg)
    # stopsig, trendsig = get_stopsig(df['Close'], bssig)

    # acts = get_acts(bssig, stopsig, trendsig, sigtype)
    # periods = get_periods1(acts)

    # bsact = bact.copy()
    # bsact = np.where(bsact==0, -1, bsact)
    
    # result = trade_returns1(pdf['Close'], periods, bsact)
    # bsrets['Returns%'] = result['winlossratio']
    
    return bsrets, sigtype, stopsig, trendsig, bssig


def trade_with_threshold(pdf, plt, ovb, ovs, retact=False):
    """ Trade with an Indicator vs another Indicator with its parameters.
    
    Return:
        For default, retact=False
        apltdt: Additional Plot data frame.
        bstret: Buy/Sell and Trade Returns frame.  
        
        When retact=True
        bact:   Active signal for Buy
        sact:   Active signal for Sell
    """
    bact, sact = bsact_sovbs(plt, ovb, ovs)
    
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    
    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    stopsig, trendsig = get_stopsig(plt, bssig)

    acts = get_acts(bssig, stopsig, trendsig, sigtype)
    periods = get_periods1(acts)

    bsact = bact.copy()
    bsact = np.where(bsact==0, -1, bsact)
    
    result = trade_returns1(pdf['Close'], periods, bsact)
    bsrets['Returns%'] = result['winlossratio']
    
    return bsrets, sigtype, stopsig, trendsig, bssig


def trade_returns2(close, periods, commcrg=0.02):
    ''' Get Stats with close and buy/sell signal
        
    '''
    besttarget = 0
    beststoploss = 0
    allprofit = 0.0
    allloss = 0.0

    allprofitmoney = 0.0
    alllossmoney = 0.0

    maxlosingstreak = 0
    maxwinningstreak = 0

    losingcol = 0
    winningcol = 0

    allwinn = 0
    alllossn = 0

    allbuytime = 0
    allselltime = 0
    for period in periods:
        tmp = close[period[0]:period[1]]
        if len(tmp) == 0:
            continue
        enterprice = close[period[0]]

        maxv = max(close[period[0]:period[1]])
        minv = min(close[period[0]:period[1]])
        target = (maxv-enterprice)/enterprice*100
        stoploss = (enterprice-minv)/enterprice*100

        if period[2] == 2: # if sell signal invert
            temp = target
            target = stoploss
            stoploss = temp

        besttarget += target
        beststoploss += stoploss

        if period[2] == 1:
            allbuytime += period[1] - period[0] + 1
        else:
            allselltime += period[1] - period[0] + 1

        index = period[0]
        prestate = ''
        profit = 0.0
        loss = 0.0
        profitmoney = 0.0
        lossmoney = 0.0
        winstreak = 0
        lossstreak = 0
        winn = 0
        lossn = 0

        while index <= period[1]:
            state = ''
            if close[index] > enterprice:
                profit += (close[index] - enterprice)/enterprice
                profitmoney += close[index] - enterprice
                winn += 1
                state = 'Win'
                if prestate == '':
                    prestate = state
            elif close[index] < enterprice:
                lossn += 1
                loss += (enterprice - close[index])/enterprice
                lossmoney += enterprice - close[index]
                state = 'Loss'
                if prestate == '':
                    prestate = state

            if state == prestate and state == 'Win':
                winstreak += 1

            if state == prestate and state == 'Loss':
                lossstreak += 1
           
            if prestate != state or index == period[1]:
                if period[2] == -1: # if sell signal invert
                    temp = winstreak
                    winstreak = lossstreak
                    lossstreak = temp
                
                if maxwinningstreak < winstreak:
                    maxwinningstreak = winstreak
                
                if maxlosingstreak < lossstreak:
                    maxlosingstreak = lossstreak

            prestate = state
            index += 1

        if period[2] == 2: # if sell signal invert
            temp = profit
            profit = loss
            loss = temp

            temp = winn
            winn = lossn
            lossn = temp

            temp = profitmoney
            profitmoney = lossmoney
            lossmoney = temp

        allprofit += profit
        allloss += loss

        allwinn += winn
        alllossn += lossn

        allprofitmoney += profitmoney/(winn if winn>0 else 1)
        alllossmoney += lossmoney/(lossn if lossn>0 else 1)

    periodscnt = len(periods)
    if periodscnt == 0:
        periodscnt = 1
    besttarget /= periodscnt
    beststoploss /= periodscnt
    tmp = allwinn+alllossn
    if tmp == 0:
        tmp = 1
    winlossratio = allwinn/tmp*100

    avbuytime = allbuytime / periodscnt
    avselltime = allselltime / periodscnt

    tmp = allwinn
    if tmp == 0:
        tmp = 1
    avprofit = allprofit / tmp
    tmp = alllossn
    if tmp == 0:
        tmp = 1
    avloss = allloss / tmp

    # allprofitmoney /= periodscnt
    # alllossmoney /= periodscnt
        
    # return {'besttarget':besttarget, 'beststoploss':beststoploss, 'winlossratio':winlossratio, 'winn':allwinn, 'lossn':alllossn, 
    #         'maxlosingstreak':maxlosingstreak, 'maxwinningstreak':maxwinningstreak, 'avbuytime':avbuytime, 'avselltime':avselltime,
    #         'avprofit':avprofit,'avloss':avloss, 'avprofitmoney':allprofitmoney, 'avlossmoney':alllossmoney}

    if alllossmoney == 0:
        alllossmoney = 1
    winlossratio1 = allprofitmoney/alllossmoney
    return {'winlossratio':winlossratio1}  


def trade_with_signals(pdf, signals):
    periods = get_periods2(signals)
    
    result = trade_returns2(pdf['Close'], periods)
    
    return result