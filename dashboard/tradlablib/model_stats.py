# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from pandas import DataFrame

from .libind.bssig import *
from .model_train import *

commcrg = 0.02 # Default value of trade commission charges (same in exec_trade.py)


def print_stats(ti_name, psetb, wlsts):
    ''' Print Statistics for a technical indicator
    '''
    name_str = 'TI_Stats_'+ti_name
    name_str+='.txt'
    f= open('../data/results/'+name_str,"w+")
    psetb_str = ' '.join(str(pset) for pset in psetb)
    f.write("Best Parameters & Returns \r\n %s\r\n" % psetb_str)
    f.write("Win/Loss Stats %s\r\n" % wlsts)
    f.close()
    print('')
    print('Technical Indicator(s): '+ti_name)
    print('Best Parameters & Returns%')
    print(psetb)
    print('')
    print('Win/Loss Stats')
    print(wlsts)

def get_wl_stats(close, bssig, commcrg=0.02):
    ''' Get Stats with close and buy/sell signal
        
    '''
    sig, trp = trade_returns(close, bssig, commcrg)

    ttrs = int(len(trp)/2)   # Total Trade Sessions. Buy + Sell is one sessions
    inval = 0
    wininst = 0
    loseinst = 0
    for idx in range(ttrs):
        if trp[2*idx+1] > inval:
            wininst += 1
        elif trp[2*idx+1] < inval:
            loseinst += 1
        inval = trp[2*idx+1]
    
    allinst = wininst+loseinst
    if allinst == 0:
        allinst = 1
    winp = 100*wininst/allinst
    losp = 100-winp
    wlsts = pd.DataFrame(columns=['win', 'loss', 'win%', 'loss%'])
    wlsts.loc[0] = [wininst, loseinst, winp, losp]
    
    return wlsts, sig, trp

def get_stats(close, periods, bssig, commcrg=0.02):
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

        allbuytime += bssig[period[0]:period[1]].count(1)
        allselltime += bssig[period[0]:period[1]].count(-1)

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

    tmp = alllossmoney
    if tmp == 0:
        tmp = 1
    
    allprofitmoney /= periodscnt
    alllossmoney /= periodscnt

    return {'besttarget':besttarget, 'beststoploss':beststoploss, 'winlossratio':winlossratio, 'winn':allwinn, 'lossn':alllossn, 
            'maxlosingstreak':maxlosingstreak, 'maxwinningstreak':maxwinningstreak, 'avbuytime':avbuytime, 'avselltime':avselltime,
            'avprofit':avprofit,'avloss':avloss, 'avprofitmoney':allprofitmoney, 'avlossmoney':alllossmoney}


def get_stats_singleti(dt, *arglist):
    ''' Gives Statistics for single technical indicator.
    
        Input
        dt: data with required columns
        arglist: List of arguments
            1. training function
            2. base parameter argument. e.g. bsprms = (param1, param2, param3)
        
        Returns
        psetb: best parameter set with % buy/sell returns
        wlsts: win and lose stats
    '''
    trn_fn  = arglist[0]
    bsprms  = arglist[1]

    psetb, pret, sigtype, stopsig, trendsig, bssig = trn_fn(dt, *bsprms, True)
    # psetb has the best parameters
    
    # if sigtype == 1:
    #     bssig = get_bssig(bact, sact)
    # elif sigtype == 2:
    #     bssig = get_bssig2(bact, sact)

    wlsts, sig, trp = get_wl_stats(dt['Close'], bssig, commcrg)

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
    
    return psetb, wlsts, acts


def get_stats_singletradei(dt, *arglist):
    ''' Gives Statistics for single technical indicator.
    
        Input
        dt: data with required columns
        arglist: List of arguments
            1. training function
            2. base parameter argument. e.g. bsprms = (param1, param2, param3)
        
        Returns
        psetb: best parameter set with % buy/sell returns
        wlsts: win and lose stats
    '''
    trade_fn  = arglist[0]
    bsprms  = arglist[1]

    try:
        sigtype, stopsig, trendsig, bssig = trade_fn(dt, *bsprms, True)
    except ValueError:
        bsrets, sigtype, stopsig, trendsig, bssig = trade_fn(dt, *bsprms, True)

    wlsts, sig, trp = get_wl_stats(dt['Close'], bssig, commcrg)

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
    
    return psetb, wlsts, acts