# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from pandas import DataFrame

from .exec_trade import *

from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib.indicatorparameter import *


   
def train_with_one(pret, dft, p1_a, tr_f):
    """ Training function for TI with 2 params.
    
    Args:
    pret: Empty frame with columns for parameters and return values.
    dft : Data frame on which trading can be done using technical indicator.
    p1_a: Array of first parameter values.
    p2_a: Array of second parameter values.
    tr_f: Trading function.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    ipret = 0
    for ip1 in range(p1_a.size):
        apltd, bsrets = tr_f(dft, p1_a[ip1])
        if bsrets.empty:
            traderet = 0
        else:
            traderet = bsrets['Returns%'].iloc[-1] # Last index for final return
        pret.loc[ipret] = [p1_a[ip1], traderet, '']
        ipret+=1
    
    retcol = pret['Returns%']
    imax = np.array(retcol).argmax()
    pret.at[imax, 'MaxR'] = 'MR'
    psetb = pret.loc[imax]

    return psetb, pret

def train_with_two(pret, dft, p1_a, p2_a, tr_f):
    """ Training function for TI with 2 params.
    
    Args:
    pret: Empty frame with columns for parameters and return values.
    dft : Data frame on which trading can be done using technical indicator.
    p1_a: Array of first parameter values.
    p2_a: Array of second parameter values.
    tr_f: Trading function.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    ipret = 0
    for ip1 in range(p1_a.size):
        for ip2 in range(p2_a.size):
            apltd, bsrets = tr_f(dft, p1_a[ip1], p2_a[ip2])
            if bsrets.empty:
                traderet = 0
            else:
                traderet = bsrets['Returns%'].iloc[-1] # Last index for final return
            pret.loc[ipret] = [p1_a[ip1], p2_a[ip2], traderet, '']
            ipret+=1
    
    retcol = pret['Returns%']
    imax = np.array(retcol).argmax()
    pret.at[imax, 'MaxR'] = 'MR'
    psetb = pret.loc[imax]

    return psetb, pret

   
def train_with_three(pret, dft, p1_a, p2_a, p3_a, tr_f):
    """ Training function for TI with 2 params.
    
    Args:
    pret: Empty frame with columns for parameters and return values.
    dft : Data frame on which trading can be done using technical indicator.
    p1_a: Array of first parameter values.
    p2_a: Array of second parameter values.
    p2_a: Array of second parameter values.
    tr_f: Trading function.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    ipret = 0
    for ip1 in range(p1_a.size):
        for ip2 in range(p2_a.size):
            for ip3 in range(p3_a.size):
                #print(np.array([ip1, ip2, ip3]))
                apltd, bsrets = tr_f(dft, p1_a[ip1], p2_a[ip2], p3_a[ip3])
                if bsrets.empty:
                    traderet = 0
                else:
                    traderet = bsrets['Returns%'].iloc[-1] # Last index for final return
                pret.loc[ipret] = [p1_a[ip1], p2_a[ip2], p3_a[ip3], traderet, '']
                ipret+=1
    
    retcol = pret['Returns%']
    imax = np.array(retcol).argmax()
    pret.at[imax, 'MaxR'] = 'MR'
    psetb = pret.loc[imax]

    return psetb, pret
    
def train_with_eighth(pret, dft, p1_a, p2_a, p3_a, p4_a, p5_a, p6_a, p7_a, p8_a, tr_f):
    """ Training function for TI with 8 params.
    
    Args:
    pret: Empty frame with columns for parameters and return values.
    dft : Data frame on which trading can be done using technical indicator.
    p1_a: Array of first parameter values.
    p2_a: Array of second parameter values.
    p3_a: Array of three parameter values.
    p4_a: Array of fourth parameter values.
    p5_a: Array of fifth parameter values.
    p6_a: Array of sixth parameter values.
    p7_a: Array of seventh parameter values.
    p8_a: Array of eigth parameter values.
    tr_f: Trading function.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    ipret = 0
    for ip1 in range(p1_a.size):
        for ip2 in range(p2_a.size):
            for ip3 in range(p3_a.size):
                for ip4 in range(p4_a.size):
                    for ip5 in range(p5_a.size):
                        for ip6 in range(p6_a.size):
                            for ip7 in range(p7_a.size):
                                for ip8 in range(p8_a.size):
                                    apltd, bsrets = tr_f(dft, p1_a[ip1], p2_a[ip2], p3_a[ip3], p4_a[ip4], p5_a[ip5], p6_a[ip6], p7_a[ip7], p8_a[ip8])
                                    if bsrets.empty:
                                        traderet = 0
                                    else:
                                        traderet = bsrets['Returns%'].iloc[-1] # Last index for final return
                                    pret.loc[ipret] = [p1_a[ip1], p2_a[ip2], p3_a[ip3], p4_a[ip4], p5_a[ip5], p6_a[ip6], p7_a[ip7], p8_a[ip8], traderet, '']
                                    ipret+=1
    
    retcol = pret['Returns%']
    imax = np.array(retcol).argmax()
    pret.at[imax, 'MaxR'] = 'MR'
    psetb = pret.loc[imax]

    return psetb, pret
    
def train_for_ao(pdf, ao_short_length, ao_long_length, retwithact=False):
    """ Train for Awesome Oscillator in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(ao_short_length-2, ao_short_length+4, 1, dtype=int)
    sd_a  = np.arange(ao_long_length-7, ao_long_length+7, 3, dtype=int)
    
    pret = pd.DataFrame(columns=['ao_short_length', 'ao_long_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_two(pret, pdf, len_a, sd_a, trade_with_ao)

    if retwithact == True:
        bao_short_length = psetb[0]
        bao_long_length  = psetb[1]
        args = (bao_short_length, bao_long_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_ao(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_atr(pdf, atr_length, retwithact=False):
    """ Train for Average True Range in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(atr_length-7, atr_length+7, 1, dtype=int)
    pret = pd.DataFrame(columns=['atr_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, len_a, trade_with_atr)

    if retwithact == True:
        batr_length = psetb[0]
        args = (batr_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_atr(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_bb(pdf, bb_length, bb_std_dev, retwithact=False):
    """ Train for Bollinger Band in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(bb_length-4, bb_length+4, 2, dtype=int)
    sd_a  = np.arange(bb_std_dev-1, bb_std_dev+1, 0.5, dtype=float)
    
    pret = pd.DataFrame(columns=['bb_length', 'bb_std_dev', 'Returns%', 'MaxR'])
    psetb, pret = train_with_two(pret, pdf, len_a, sd_a, trade_with_bb)
    
    if retwithact == True:
        bb_length = psetb[0]
        bb_std_dev  = psetb[1]
        args = (bb_length, bb_std_dev, True)
        sigtype, stopsig, trendsig, bssig = trade_with_bb(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_po(pdf, po_short_length, po_long_length, retwithact=False):
    """ Train for Price Oscillator in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(po_short_length-4, po_short_length+4, 2, dtype=int)
    sd_a  = np.arange(po_long_length-5, po_long_length+5, 2, dtype=int)
    
    pret = pd.DataFrame(columns=['po_short_length', 'po_long_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_two(pret, pdf, len_a, sd_a, trade_with_po)

    if retwithact == True:
        bpo_short_length = psetb[0]
        bpo_long_length  = psetb[1]
        args = (bpo_short_length, bpo_long_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_po(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_cc(pdf, cc_length, retwithact=False):
    """ Train for Coppock Curve in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(cc_length-5, cc_length+5, 2, dtype=int)
    pret = pd.DataFrame(columns=['cc_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, len_a, trade_with_cc)
    
    if retwithact == True:
        bcc_length = psetb[0]
        args = (bcc_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_cc(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret 
    
def train_for_cci(pdf, cci_length, cci_mul, retwithact=False):
    """ Train for Commodity Channel Index in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    lenf_a = np.arange(cci_length-5, cci_length+5, 2, dtype=int)
    lens_a = np.arange(cci_mul-0.005, cci_mul+0.005, 0.001, dtype=float)
    
    pret = pd.DataFrame(columns=['cci_length', 'cci_mul', 'Returns%', 'MaxR'])
    psetb, pret = train_with_two(pret, pdf, lenf_a, lens_a, trade_with_cci)

    if retwithact == True:
        bcci_length = psetb[0]
        bcci_mul  = psetb[1]
        args = (bcci_length, bcci_mul, True)
        sigtype, stopsig, trendsig, bssig = trade_with_cci(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_tsi(pdf, tsi_long_length, tsi_short_length, retwithact=False):
    """ Train for True Strength Index in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    lenf_a = np.arange(tsi_long_length-6, tsi_long_length+6, 2, dtype=int)
    lens_a = np.arange(tsi_short_length-4, tsi_short_length+4, 1, dtype=int)
    
    pret = pd.DataFrame(columns=['tsi_long_length', 'tsi_short_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_two(pret, pdf, lenf_a, lens_a, trade_with_tsi)

    if retwithact == True:
        btsi_long_length = psetb[0]
        btsi_short_length  = psetb[1]
        args = (btsi_long_length, btsi_short_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_tsi(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret 
    
def train_for_stchrsi(pdf, stch_length, retwithact=False):
    """ Train for Commodity Channel Index in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    lenf_a = np.arange(stch_length-5, stch_length+5, 2, dtype=int)
    
    pret = pd.DataFrame(columns=['stchrsi_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, lenf_a, trade_with_stchrsi)

    if retwithact == True:
        bstch_length = psetb[0]
        args = (bstch_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_stchrsi(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret 
    
def train_for_wpr(pdf, wpr_length, retwithact=False):
    """ Train for William %R in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    lenf_a = np.arange(wpr_length-10, wpr_length+10, 1, dtype=int)
    
    pret = pd.DataFrame(columns=['wpr_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, lenf_a, trade_with_wpr)
    if retwithact == True:
        bwpr_length = psetb[0]
        args = (bwpr_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_wpr(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_dc(pdf, dc_length, retwithact=False):
    """ Train for Donchain Channels in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(dc_length-5, dc_length+5, 1, dtype=int)
    pret = pd.DataFrame(columns=['dc_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, len_a, trade_with_dc)
    
    if retwithact == True:
        bdc_length = psetb[0]
        args = (bdc_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_dc(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_adx(pdf, dmi_length, retwithact=False):
    """ Train for Average Directional Movement Index  in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(dmi_length-5, dmi_length+5, 1, dtype=int)
    pret = pd.DataFrame(columns=['dmi_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, len_a, trade_with_adx)
    
    if retwithact == True:
        bdmi_length = psetb[0]
        args = (bdmi_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_adx(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_kc(pdf, kc_length, retwithact=False):
    """ Train for Keltner Channels in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(kc_length-9, kc_length+9, 1, dtype=int)
    pret = pd.DataFrame(columns=['kc_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, len_a, trade_with_kc)
    if retwithact == True:
        bkc_length = psetb[0]
        args = (bkc_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_kc(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret  
    
def train_for_macd(pdf, macd_short_period, macd_long_period, macd_signal_smoothing, retwithact=False):
    """ Train for MACD in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    shortp_a = np.arange(macd_short_period-2, macd_short_period+2, 1, dtype=int)
    longp_a = np.arange(macd_long_period-4, macd_long_period+4, 2, dtype=int)
    sigsm_a = np.arange(macd_signal_smoothing-2, macd_signal_smoothing+2, 1, dtype=int)
    
    pret = pd.DataFrame(columns=['macd_short_period', 'macd_long_period', \
                                 'macd_signal_smoothing', 'Returns%', 'MaxR'])
    psetb, pret = train_with_three(pret, pdf, shortp_a, longp_a, sigsm_a, trade_with_macd)
    
    if retwithact == True:
        bmacd_short_period      = psetb[0]
        bmacd_long_period       = psetb[1]
        bmacd_signal_smoothing  = psetb[2]
        args = (bmacd_short_period, bmacd_long_period, bmacd_signal_smoothing, True)
        sigtype, stopsig, trendsig, bssig = trade_with_macd(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret

def train_for_ema(pdf, ema_length_fast, ema_length_slow, retwithact=False):
    """ Train for EMA in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    lenf_a = np.arange(ema_length_fast-2, ema_length_fast+2, 1, dtype=int)
    lens_a = np.arange(ema_length_slow-4, ema_length_slow+4, 2, dtype=int)
    
    pret = pd.DataFrame(columns=['ema_length_fast', 'ema_length_slow', 'Returns%', 'MaxR'])
    psetb, pret = train_with_two(pret, pdf, lenf_a, lens_a, trade_with_ema)

    if retwithact == True:
        bema_length_fast = psetb[0]
        bema_length_slow  = psetb[1]
        args = (bema_length_fast, bema_length_slow, True)
        sigtype, stopsig, trendsig, bssig = trade_with_ema(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret

def train_for_macross(pdf, matype, ma_length_fast, ma_length_slow, retwithact=False):
    """ Train for MA Cross in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    lenf_a = np.arange(ma_length_fast-2, ma_length_fast+2, 1, dtype=int)
    lens_a = np.arange(ma_length_slow-4, ma_length_slow+4, 2, dtype=int)
    
    pret = pd.DataFrame(columns=['length_fast', 'length_slow', 'Returns%', 'MaxR'])
    #psetb, pret = train_with_three(pret, pdf, ['EMA', 'SMA', 'WMA'], lenf_a, lens_a, trade_with_ma_cross)
    if matype == 'EMA':
        psetb, pret = train_with_two(pret, pdf, lenf_a, lens_a, trade_with_ema_cross)
    elif matype == 'SMA':
        psetb, pret = train_with_two(pret, pdf, lenf_a, lens_a, trade_with_sma_cross)
    elif matype == 'WMA':
        psetb, pret = train_with_two(pret, pdf, lenf_a, lens_a, trade_with_wma_cross)
    else:
        psetb, pret = train_with_two(pret, pdf, lenf_a, lens_a, trade_with_sma_cross) 
        
    if retwithact == True:
        if type == 'EMA':
            ma_length_fast = psetb[0]
            ma_length_slow = psetb[1]
            args = (ma_length_fast, ma_length_slow, True)
            sigtype, stopsig, trendsig, bssig = trade_with_ema_cross(pdf, *args)
            return psetb, pret, sigtype, stopsig, trendsig, bssig
        elif type == 'SMA':
            ma_length_fast = psetb[0]
            ma_length_slow = psetb[1]
            args = (ma_length_fast, ma_length_slow, True)            
            sigtype, stopsig, trendsig, bssig = trade_with_sma_cross(pdf, *args)
            return psetb, pret, sigtype, stopsig, trendsig, bssig
        elif type == 'WMA':
            ma_length_fast = psetb[0]
            ma_length_slow = psetb[1]
            args = (ma_length_fast, ma_length_slow, True)            
            sigtype, stopsig, trendsig, bssig = trade_with_wma_cross(pdf, *args)
            return psetb, pret, sigtype, stopsig, trendsig, bssig        
        else:
            ma_length_fast = psetb[0]
            ma_length_slow = psetb[1]
            args = (ma_length_fast, ma_length_slow, True)            
            sigtype, stopsig, trendsig, bssig = trade_with_sma_cross(pdf, *args)
            return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_mom(pdf, mom_length, retwithact=False):
    """ Train for Momentum in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(mom_length-5, mom_length+5, 2, dtype=int)
    pret = pd.DataFrame(columns=['mom_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, len_a, trade_with_mom)

    if retwithact == True:
        bmom_length = psetb[0]
        args = (bmom_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_mom(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret 
    
def train_for_rsi(pdf, rsi_length, retwithact=False):
    """ Train for Relative Strength Index in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(rsi_length-10, rsi_length+10, 1, dtype=int)
    pret = pd.DataFrame(columns=['rsi_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, len_a, trade_with_rsi)

    if retwithact == True:
        brsi_length = psetb[0]
        args = (brsi_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_rsi(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret 
    
def train_for_sma(pdf, sma_length_fast, sma_length_slow, retwithact=False):
    """ Train for SMA in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    lenf_a = np.arange(sma_length_fast-2, sma_length_fast+2, 1, dtype=int)
    lens_a = np.arange(sma_length_slow-4, sma_length_slow+4, 2, dtype=int)
    
    pret = pd.DataFrame(columns=['sma_length_fast', 'sma_length_slow', 'Returns%', 'MaxR'])
    psetb, pret = train_with_two(pret, pdf, lenf_a, lens_a, trade_with_sma)

    if retwithact == True:
        bsma_length_fast = psetb[0]
        bsma_length_slow  = psetb[1]
        args = (bsma_length_fast, bsma_length_slow, True)
        sigtype, stopsig, trendsig, bssig = trade_with_sma(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_trix(pdf, trix_length, retwithact=False):
    """ Train for Trix in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(trix_length-5, trix_length+5, 2, dtype=int)
    pret = pd.DataFrame(columns=['trix_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, len_a, trade_with_trix)
    
    if retwithact == True:
        btrix_length = psetb[0]
        args = (btrix_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_trix(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret

def train_for_wma(pdf, wma_length_fast, wma_length_slow, retwithact=False):
    """ Train for WMA in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    lenf_a = np.arange(wma_length_fast-2, wma_length_fast+2, 1, dtype=int)
    lens_a = np.arange(wma_length_slow-4, wma_length_slow+4, 2, dtype=int)
    
    pret = pd.DataFrame(columns=['wma_length_fast', 'wma_length_slow', 'Returns%', 'MaxR'])
    psetb, pret = train_with_two(pret, pdf, lenf_a, lens_a, trade_with_wma)
    if retwithact == True:
        bwma_length_fast = psetb[0]
        bwma_length_slow  = psetb[1]
        args = (bwma_length_fast, bwma_length_slow, True)
        sigtype, stopsig, trendsig, bssig = trade_with_wma(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret

def train_for_stoch(pdf, s_k, s_d, s_smooth, retwithact=False):
    """ Train for MACD in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    sk_a = np.arange(s_k-1, s_k+1, 1, dtype=int)
    sd_a = np.arange(s_d-2, s_d+2, 2, dtype=int)
    ss_a = np.arange(s_smooth-1, s_smooth+1, 1, dtype=int)
    
    pret = pd.DataFrame(columns=['s_k', 's_d', 's_smooth', 'Returns%', 'MaxR'])
    psetb, pret = train_with_three(pret, pdf, sk_a, sd_a, ss_a, trade_with_stoch)

    if retwithact == True:
        bs_k        = psetb[0]
        bs_d        = psetb[1]
        bs_smooth   = psetb[2]
        args = (bs_k, bs_d, bs_smooth, True)
        sigtype, stopsig, trendsig, bssig = trade_with_stoch(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret 

def train_for_voi(pdf, voi_length, retwithact=False):
    """ Train for Vortex Indicator  in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    len_a = np.arange(voi_length-5, voi_length+5, 1, dtype=int)
    pret = pd.DataFrame(columns=['voi_length', 'Returns%', 'MaxR'])
    psetb, pret = train_with_one(pret, pdf, len_a, trade_with_voi)
    if retwithact == True:
        bvoi_length = psetb[0]
        args = (bvoi_length, True)
        sigtype, stopsig, trendsig, bssig = trade_with_voi(pdf, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret
    
def train_for_kst(pltdt, kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, kst_sma_length_1, 
            kst_sma_length_2, kst_sma_length_3, kst_sma_length_4, retwithact=False):
    """ Train for KST Oscillator  in the neighbourhood of given params.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """
    sk_a = np.arange(kst_roc_length_1-2, kst_roc_length_1+2, 2, dtype=int)
    sd_a = np.arange(kst_roc_length_2-3, kst_roc_length_2+3, 2, dtype=int)
    sk1_a = np.arange(kst_roc_length_3-4, kst_roc_length_3+4, 2, dtype=int)
    sd2_a = np.arange(kst_roc_length_4-5, kst_roc_length_4+5, 2, dtype=int)
    ss_a = np.arange(kst_sma_length_1-2, kst_sma_length_1+2, 2, dtype=int)
    ss2_a = np.arange(kst_sma_length_2-2, kst_sma_length_2+2, 2, dtype=int)
    ss3_a = np.arange(kst_sma_length_3-2, kst_sma_length_3+2, 2, dtype=int)
    ss4_a = np.arange(kst_sma_length_4-3, kst_sma_length_4+3, 2, dtype=int)
    
    pret = pd.DataFrame(columns=['roc_l1', 'roc_l2', 'roc_l3', 'roc_l4', 'sma_l1', 'sma_l2', 'sma_l3', 'sma_l4', 'Returns%', 'MaxR'])
    psetb, pret = train_with_eighth(pret, pltdt, sk_a, sd_a, sk1_a, sd2_a, ss_a, ss2_a, ss3_a, ss4_a, trade_with_kst)
    
    if retwithact == True:
        bkst_roc_length_1 = psetb[0]
        bkst_roc_length_2 = psetb[1]
        bkst_roc_length_3 = psetb[2]
        bkst_roc_length_4 = psetb[3]
        bkst_sma_length_1 = psetb[4]
        bkst_sma_length_2 = psetb[5]
        bkst_sma_length_3 = psetb[6]
        bkst_sma_length_4 = psetb[7]
        args = (bkst_roc_length_1, bkst_roc_length_2, bkst_roc_length_3, bkst_roc_length_4, bkst_sma_length_1, 
                bkst_sma_length_2, bkst_sma_length_3, bkst_sma_length_4, True)
        sigtype, stopsig, trendsig, bssig = trade_with_kst(pltdt, *args)
        return psetb, pret, sigtype, stopsig, trendsig, bssig
    else:
        return psetb, pret


def prepare_params_for_cmf(cmf_length):
    cmf_lengtha = np.arange(cmf_length-7, cmf_length+7, 1, dtype=int)
    return [cmf_lengtha]

def prepare_params_for_vo(vo_short_length, vo_long_length):
    vo_short_lengtha = np.arange(3, vo_short_length+2, 1, dtype=int)
    vo_long_lengtha = np.arange(vo_long_length-2, vo_long_length+3, 1, dtype=int)
    return [vo_short_lengtha, vo_long_lengtha]

def prepare_params_for_eom(eom_length):
    eom_lengtha = np.arange(eom_length-4, eom_length+6, 1, dtype=int)
    return [eom_lengtha]

def prepare_params_for_co(co_short_length, co_long_length):
    co_short_lengtha = np.arange(3, co_short_length+2, 1, dtype=int)
    co_long_lengtha = np.arange(co_long_length-2, co_long_length+3, 1, dtype=int)
    return [co_short_lengtha, co_long_lengtha]

def prepare_params_for_bb_pb(bb_pb_length, bb_pb_std_dev):
    bb_pb_lengtha = np.arange(bb_pb_length-7, bb_pb_length+7, 1, dtype=int)
    bb_pb_std_deva = np.array([bb_pb_std_dev])
    return [bb_pb_lengtha, bb_pb_std_deva]

def prepare_params_for_bb_bw(bb_length, bb_std_dev):
    bb_lengtha = np.arange(bb_length-7, bb_length+7, 1, dtype=int)
    bb_std_deva = np.array([bb_pb_std_dev])
    return [bb_lengtha, bb_std_deva]

def prepare_params_for_bb_dc(dc_length):
    dc_lengtha = np.arange(dc_length-2, dc_length+3, 1, dtype=int)
    return [dc_lengtha]

def prepare_params_for_uo(uo_period_1, uo_period_2, uo_period_3, uo_ws, uo_wm, uo_wl):
    uo_period_1a = np.arange(uo_period_1-2, uo_period_1+3, 1, dtype=int)
    uo_period_2a = np.arange(uo_period_2-2, uo_period_2+3, 1, dtype=int)
    uo_period_3a = np.arange(uo_period_3-2, uo_period_3+3, 1, dtype=int)
    uo_wsa = np.array([uo_ws])
    uo_wma = np.array([uo_wm])
    uo_wla = np.array([uo_wl])
    return [uo_period_1a, uo_period_2a, uo_period_3a, uo_wsa, uo_wma, uo_wla]

def prepare_params_for_aroon(aroon_length):
    aroon_lengtha = np.arange(aroon_length-2, aroon_length+3, 1, dtype=int)
    return [aroon_lengtha]

def prepare_params_for_adi(adi_length, di_length):
    adi_lengtha = np.arange(adi_length-2, adi_length+3, 1, dtype=int)
    di_lengtha = np.arange(di_length-2, di_length+3, 1, dtype=int)
    return [adi_lengtha, di_lengtha]    

def prepare_params_for_hma(hma_period, close_col):
    hma_perioda = np.arange(hma_period-2, hma_period+3, 1, dtype=int)
    close_cola = [close_col]
    return [hma_perioda, close_cola]    

def prepare_params_for_ic(ic_conversion_line_period, ic_baseline_period, ic_lagging_spen_period, ic_displacement):
    ic_conversion_line_perioda = np.arange(ic_conversion_line_period-2, ic_conversion_line_period+3, 1, dtype=int)
    ic_baseline_perioda = np.arange(ic_baseline_period-2, ic_baseline_period+3, 1, dtype=int)
    ic_lagging_spen_perioda = np.arange(ic_lagging_spen_period-2, ic_lagging_spen_period+3, 1, dtype=int)
    ic_displacementa = [ic_displacement]
    return [ic_conversion_line_perioda, ic_baseline_perioda, ic_lagging_spen_perioda, ic_displacementa]

def prepare_params_for_dema(dema_length):
    dema_lengtha = np.arange(dema_length-2, dema_length+3, 1, dtype=int)
    return [dema_lengtha]

def prepare_params_for_mi(mi_high_period, mi_low_period):
    mi_high_perioda = np.arange(mi_high_period-2, mi_high_period+3, 1, dtype=int)
    mi_low_perioda = np.arange(mi_low_period-2, mi_low_period+3, 1, dtype=int)
    return [mi_high_perioda, mi_low_perioda]

def prepare_params_for_ema(ema_length):
    ema_lengtha = np.arange(ema_length-2, ema_length+3, 1, dtype=int)
    return [ema_lengtha, ema_lengtha]

def prepare_params_for_sma(sma_length, close_col):
    sma_lengtha = np.arange(sma_length-2, sma_length+3, 1, dtype=int)
    close_cola = [close_col]
    return [sma_lengtha, close_cola]

def prepare_params_for_wma(wma_length, close_col):
    wma_lengtha = np.arange(wma_length-2, wma_length+3, 1, dtype=int)
    close_cola = [close_col]
    return [wma_lengtha, close_cola]

def prepare_params_for_smma(smma_length, close_col):
    smma_lengtha = np.arange(smma_length-2, smma_length+3, 1, dtype=int)
    close_cola = [close_col]
    return [smma_lengtha, close_cola]

def prepare_params_for_cmo(cmo_length):
    cmo_lengtha = np.arange(cmo_length-2, cmo_length+3, 1, dtype=int)
    return [cmo_lengtha]




def train_for_cross2(df, tii1, tii2, plt1, plt2, recact=False):
    """ Train for plot vs plot in.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """

    cols = []
    params1 = []
    for ii in tii1.indicator.indicatorinputs.all():
        params1.append(get_input_value(tii1, ii.parameter))
        cols.append(ii.parameter)

    params2 = []
    for ii in tii2.indicator.indicatorinputs.all():
        params2.append(get_input_value(tii2, ii.parameter))
        cols.append(ii.parameter)

    if len(params1) > 0:
        params1 = globals()['prepare_params_for_'+tii1.indicator.id_letter](*params1)
    
    if len(params2) > 0:    
        params2 = globals()['prepare_params_for_'+tii2.indicator.id_letter](*params2)

    cols.extend(['Returns%', 'MaxR'])
    pret = pd.DataFrame(columns=cols)

    arglist = [[]]      # make all possible parameter combinations
    for p in params1:
        newarglist = []
        for pp in p:    
            for argset in arglist:
                newargset = argset.copy()
                newargset.append(pp)
                newarglist.append(newargset)

        arglist = newarglist
    
    arglist1 = arglist

    arglist = [[]]      # make all possible parameter combinations
    for p in params2:
        newarglist = []
        for pp in p:    
            for argset in arglist:
                newargset = argset.copy()
                newargset.append(pp)
                newarglist.append(newargset)

        arglist = newarglist
    
    arglist2 = arglist

    sargs = [trade_with_cross2]

    bssigmap = dict()
    stopsigmap = dict()
    trendsigmap = dict()
    sigtypemap = dict()

    ipret = 0
    for argset1 in arglist1:
        graphdata1 = tind.display_indicator(df, tii1.indicator.name, tii1, True, *argset1)
        dfnew = df.copy()
        for pltdt in graphdata1:
            dfnew[pltdt['name']] = pltdt['y']
            if pltdt['name'] == plt1:
                pltdt1=pltdt['y']
        
        for argset2 in arglist2:
            graphdata2 = tind.display_indicator(dfnew, tii2.indicator.name, tii2, True, *argset2)
            for pltdt in graphdata2:
                if pltdt['name'] == plt2:
                    pltdt2=pltdt['y']
                    break
            bsrets, sigtype, stopsig, trendsig, bssig = trade_with_cross2(df, pltdt1, pltdt2, True)
            if bsrets.empty:
                traderet = 0
            else:
                traderet = bsrets['Returns%'].iloc[-1] # Last index for final return
            
            parama = argset1.copy()
            parama.extend(argset2)
            parama.extend([traderet, ''])
            bssigmap[ipret] = bssig
            stopsigmap[ipret] = stopsig
            trendsigmap[ipret] = trendsig
            sigtypemap[ipret] =  sigtype
            pret.loc[ipret] = parama
            ipret+=1
    
    retcol = pret['Returns%']
    imax = np.array(retcol).argmax()
    pret.at[imax, 'MaxR'] = 'MR'
    psetb = pret.loc[imax]
    
    return psetb, pret, sigtypemap[imax], stopsigmap[imax], trendsigmap[imax], bssigmap[imax]


def train_for_crossv(df, tii, plt, recact=False):
    """ Train for plot vs plot in.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """

    cols = []
    params = []
    for ii in tii.indicator.indicatorinputs.all():
        params.append(get_input_value(tii, ii.parameter))
        cols.append(ii.parameter)

    if len(params) > 0:
        params = globals()['prepare_params_for_'+tii.indicator.id_letter](*params)

    cols.extend(['Returns%', 'MaxR'])
    pret = pd.DataFrame(columns=cols)

    arglist = [[]]      # make all possible parameter combinations
    for p in params:
        newarglist = []
        for pp in p:    
            for argset in arglist:
                newargset = argset.copy()
                newargset.append(pp)
                newarglist.append(newargset)

        arglist = newarglist
    
    sargs = [trade_with_crossv]

    bssigmap = dict()
    stopsigmap = dict()
    trendsigmap = dict()
    sigtypemap = dict()

    ipret = 0
    for argset in arglist:
        graphdata = tind.display_indicator(df, tii.indicator.name, tii, True, *argset)
        for pltdt in graphdata:
            if pltdt['name'] == plt:
                pltdt1=pltdt['y']
                break
        bsrets, sigtype, stopsig, trendsig, bssig = trade_with_crossv(df, pltdt1, True)
        if bsrets.empty:
            traderet = 0
        else:
            traderet = bsrets['Returns%'].iloc[-1] # Last index for final return
        
        parama = argset.copy()
        parama.extend([traderet, ''])
        pret.loc[ipret] = parama
        bssigmap[ipret] = bssig
        stopsigmap[ipret] = stopsig
        trendsigmap[ipret] = trendsig
        sigtypemap[ipret] =  sigtype
        ipret+=1
    
    retcol = pret['Returns%']
    imax = np.array(retcol).argmax()
    pret.at[imax, 'MaxR'] = 'MR'
    psetb = pret.loc[imax]
    
    return psetb, pret, sigtypemap[imax], stopsigmap[imax], trendsigmap[imax], bssigmap[imax]


def train_for_threshold(df, tii, plt, recact=False):
    """ Train for plot vs plot in.
    
    Return:
    psetb: Parameter set with highest trade returns.
    pret: Frame with parameters and returns values.
    """

    cols = []
    params1 = []
    for ii in tii.indicator.indicatorinputs.all():
        params1.append(get_input_value(tii, ii.parameter))
        cols.append(ii.parameter)

    if len(params1) > 0:
        params1 = globals()['prepare_params_for_'+tii.indicator.id_letter](*params1)

    cols.extend(['ovb', 'ovs', 'Returns%', 'MaxR'])
    pret = pd.DataFrame(columns=cols)

    arglist = [[]]      # make all possible parameter combinations
    for p in params1:
        newarglist = []
        for pp in p:
            for argset in arglist:
                newargset = argset.copy()
                newargset.append(pp)
                newarglist.append(newargset)

        arglist = newarglist
    
    sargs = [trade_with_threshold]

    bssigmap = dict()
    stopsigmap = dict()
    trendsigmap = dict()
    sigtypemap = dict()

    ipret = 0
    for argset in arglist:
        graphdata = tind.display_indicator(df, tii.indicator.name, tii, True, *argset)
        for pltdt in graphdata:
            if pltdt['name'] == plt:
                pltdt1=pltdt['y']
                break
        maxv = max(pltdt1)
        minv = min(pltdt1)
        ovba = np.arange((maxv+minv)/2, maxv, maxv/10, dtype=int)
        ovsa = np.arange((maxv+minv)/2, minv, minv/10, dtype=int)

        for ovb in ovba:
            for ovs in ovsa:
                bsrets, sigtype, stopsig, trendsig, bssig = trade_with_threshold(df, pltdt1, ovb, ovs, True)
                if bsrets.empty:
                    traderet = 0
                else:
                    traderet = bsrets['Returns%'].iloc[-1] # Last index for final return

                parama = argset.copy()
                parama.extend([ovb, ovs, traderet, ''])
                pret.loc[ipret] = parama
                bssigmap[ipret] = bssig
                stopsigmap[ipret] = stopsig
                trendsigmap[ipret] = trendsig
                sigtypemap[ipret] =  sigtype
                ipret+=1
    
    retcol = pret['Returns%']
    imax = np.array(retcol).argmax()
    pret.at[imax, 'MaxR'] = 'MR'
    psetb = pret.loc[imax]
    return psetb, pret, sigtypemap[imax], stopsigmap[imax], trendsigmap[imax], bssigmap[imax]


def prepare_params_for_adr(adr_length):
    adr_lengtha = np.arange(adr_length-7, adr_length+7, 1, dtype=int)
    return [adr_lengtha]