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

commcrg = 0.02 # Default value of trade commission charges


def trade_returns(data, bssig, commcrg=0.20): 
    """ Calculate the return matrix for each buy and sell signal.
    
    Return:
    Trade returns in percentage.
    """
    seedmoney = 100

    sig = []
    money = seedmoney
    value = [0]*bssig.size
    tradeprice = np.array(data)[np.array(bssig)]
    for x in range(bssig.size):
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['AO'] = ao_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
    return apltdt, bsrets

def trade_with_bb(pdf, bb_length, bb_std_dev, retact=False):
    """ Trade with Bollinger Band with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
   
    upr_bb = bollinger_hband(pdf['Close'], bb_length, bb_std_dev, fillna=False)
    mid_bb = bollinger_mavg(pdf['Close'], bb_length, fillna=False)
    lwr_bb = bollinger_lband(pdf['Close'], bb_length, bb_std_dev, fillna=False)

    bact, sact = bsact_bb(pdf, bb_length, bb_std_dev)

    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    if retact == True:
        return bact, sact, sigtype
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['ATR'] = atr_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['CC'] = cc_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
    return apltdt, bsrets    
    
def trade_with_po(pdf, po_short_length, po_long_length, retact=False):
    """ Trade with Price Oscillator with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    po_ = po_indicator(pdf, po_short_length, po_long_length)

    bact, sact = bsact_zcross(po_)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['PO'] = po_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['CCI'] = cci_

    bssig = get_bssig2(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt = pd.concat([apltdt, dc_bands], axis=1)

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['adx_pos'] = adx_pos_
    apltdt['adx_neg'] = adx_neg_

    # # get adx
    # sub = abs(adx_pos_ - adx_neg_)
    # sm = adx_pos_ + adx_neg_
    # sm.replace(0, 1)

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
    return apltdt, bsrets     
    
def trade_with_stchrsi(pdf, stch_length, retact=False):
    """ Trade with Average directional movement index with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    ovb = 80
    ovs = 20
    stchrsi = stchrsi_indicator(pdf, stch_length)
    
    bact, sact = bsact_sovbs(stchrsi, ovb, ovs)
    sigtype = 2 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['STCHRSI'] = stchrsi

    bssig = get_bssig2(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['TSI'] = tsi_

    bssig = get_bssig2(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['WPR'] = wpr_

    bssig = get_bssig2(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt = pd.concat([apltdt, kc_bands], axis=1)

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
    return apltdt, bsrets     
    
def trade_with_macd(pdf, lenfast, lenslow, lensig, retact=False):
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
    macdt   = macd(pdf['Close'], lenfast, lenslow, fillna=False)
    macdsig = macd_signal(pdf['Close'], lenfast, lenslow, lensig, fillna=False)

    bact, sact = bsact_cross(macdt, macdsig)
    sigtype = 1 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['MACD']      = macdt
    apltdt['MACDSig']   = macdsig

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
    return apltdt, bsrets 


def trade_with_ma_cross(pdf, matype, lenfast, lenslow, retact=False):
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['MOM'] = mom_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['EMA'+str(lenfast)] = emafast
    apltdt['EMA'+str(lenslow)] = emaslow

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
    return apltdt, bsrets 
    
def trade_with_rsi(pdf, rsi_length, retact=False):
    """ Trade with Relative Strength Index with its parameters.
    
    Return:
    apltdt: Additional Plot data frame.
    bstret: Buy/Sell and Trade Returns frame.    
    """
    ovb = 70 
    ovs = 30
    rsi_ = rsi(pdf['Close'], rsi_length)

    bact, sact = bsact_sovbs(rsi_, ovb, ovs)
    sigtype = 2 # 1  if get_bssig is used for trade, 2 if get_bssig2 is used for trade.
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['RSI'] = rsi_

    bssig = get_bssig2(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt = pd.DataFrame()
    apltdt['SMA'+str(lenfast)] = smafast
    apltdt['SMA'+str(lenslow)] = smaslow

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['TRIX'] = trix_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['WMA'+str(lenfast)] = wmafast
    apltdt['WMA'+str(lenslow)] = wmaslow

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['STOK'] = stok
    apltdt['STOD'] = stod

    pdf = pd.DataFrame()    # This is unnecessary
    pdf['Date'] = df['Date']
    pdf['Close'] = df['Close']
    
    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()    
    apltdt['voi_pos'] = voi_pos_
    apltdt['voi_neg'] = voi_neg_

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
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
    if retact == True:
        return bact, sact, sigtype
    
    apltdt = pd.DataFrame()
    apltdt['KST'] = kst_

    apltdt['KST_SIG'] = sma(kst_, kst_sig_length)

    bssig = get_bssig(bact, sact)
    bsrets = get_bsrets(pdf, bssig, commcrg)
    
    return apltdt, bsrets     
