# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import configparser

from .exec_trade import *
from .model_train import *
from .libind.momentum import *
from .libind.trend import *
from .libind.volatility import *
from .libind.volume import *
from .libind.misc import *

from dashboard import models
from dashboard.tradlablib.indicatorparameter import *

# Read the params.ini file
config = configparser.ConfigParser()
ini = config.read('dashboard/tradlablib/params.ini')



# Plot Settings Functions
def getPlotSetting(name, user):
    strmodel = models.ChartString.objects.get(name=name)
    defplotmodel = models.ChartPlotDefaultSetting.objects.get(string=strmodel)

    if defplotmodel.setting_manual:
        # get default plot settings
        settingval = { 'name' : strmodel.name, 'color' : defplotmodel.color, 'width' : defplotmodel.width }

        if request.user.is_authenticated:
            userplotmodel = models.ChartPlotSetting.objects.get(user=request.user, string=strmodel)
            if userplotmodel:
                # update for user plot settings
                settingval = { 'name' : strmodel.name, 'color' : userplotmodel.color, 'width' : userplotmodel.width }
    else:
        return None


# Functions description
''' Get GUI meta data for Accumulation/Distribution indicator

Args
    astdt: asset trade data.
    gpldt: existing gui plot data.

Returns
    gpldt: final gui plot data after adding new plot
    sargs: arguments for stats model. 
           some indicators do not have stats, hence empty sargs.
           Ref: test_suite.py, 
           direct indicator call, no actual trading => sargs is empty
           call with trade function, actual trading => sargs has defined value.
           #0 - plot data in src window, #1 - plot data in new window
'''

def get_mdt_acc(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #1 # Accumulation Distribution Index
    acc_ = acc_dist_index(astdt)
    
    pclm = acc_
    clname = acc_.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_adr(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #1 # Advance/Decline

    adr_length = get_input_value(tii, 'adr_length')

    if withparams:
        adr_length = arglist[0]

    adr_ = adr(astdt, adr_length)
    
    pclm = adr_
    clname = adr_.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_adi(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #1 # Average Directional Index
    # adi_length = int(config['Average_Directional_Index']['adi_length'])
    adi_length = get_input_value(tii, 'adi_length')

    if withparams:
        adi_length = arglist[0]

    adi_ = adi_indicator(astdt, adi_length)
    
    pclm = adi_
    clname = adi_.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt
    
def get_mdt_aroon(astdt, gpldt, stmdt, tii, withparams = False, *arglist):         #1 # Aroon
    # aroon_length = int(config['Aroon']['aroon_length'])
    aroon_length = get_input_value(tii, 'aroon_length')
    if withparams:
        aroon_length = arglist[0]
    
    aroon = aroon_indicator(astdt, aroon_length)
    
    clnames = list(aroon.head(0))
    for idx in range(len(aroon.columns)):
        pclm = aroon.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    return gpldt

def get_mdt_atr(astdt, gpldt, stmdt, tii, withparams = False, *arglist):       #T  #1 # Average True Range
    # atr_length = int(config['Average_True_Range']['atr_length'])
    atr_length = get_input_value(tii, 'atr_length')
    if withparams:
        atr_length = arglist[0]
    
    apltdt, bsrets = trade_with_atr(astdt, atr_length)
    
    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_atr, [atr_length]]
    stmdt['Average True Range'] = sargs
  
    return gpldt
    
def get_mdt_ao(astdt, gpldt, stmdt, tii, withparams = False, *arglist):        #T  #1 # Awesome Oscillator
    # ao_short_length = int(config['Awesome_Oscillator']['ao_short_length'])
    # ao_long_length  = int(config['Awesome_Oscillator']['ao_long_length'])

    ao_short_length = get_input_value(tii, 'ao_short_length')
    ao_long_length = get_input_value(tii, 'ao_long_length')
    if withparams:
        ao_short_length = arglist[0]
        ao_long_length = arglist[1]

    apltdt, bsrets = trade_with_ao(astdt, ao_short_length, ao_long_length)
    
    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'histogram', 'name': clnames[idx]})
    
    sargs = [train_for_ao, [ao_short_length, ao_long_length]]
    stmdt['Awesome Oscillator'] = sargs
  
    return gpldt

def get_mdt_bb(astdt, gpldt, stmdt, tii, withparams = False, *arglist):        #T  #0 # Bollinger Bands
    # bb_length   = int(config['Bollinger_Bands']['bb_length'])
    # bb_std_dev  = int(config['Bollinger_Bands']['bb_std_dev'])
    bb_length = get_input_value(tii, 'bb_length')
    bb_std_dev = get_input_value(tii, 'bb_std_dev')
    close_col = get_input_value(tii, 'close_col')

    if withparams:
        bb_length = arglist[0]
        bb_std_dev = arglist[1]
        close_col = arglist[2]

    apltdt, bsrets = trade_with_bb(astdt, bb_length, bb_std_dev, close_col)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_bb, [bb_length, bb_std_dev, close_col]]
    stmdt['Bollinger Bands'] = sargs

    return gpldt

def get_mdt_bb_pb(astdt, gpldt, stmdt, tii, withparams = False, *arglist):         #1 # Bollinger Bands % B
    # bb_pb_length = int(config['Bollinger_Bands_PB']['bb_pb_length'])
    # bb_pb_std_dev = int(config['Bollinger_Bands_PB']['bb_pb_std_dev'])

    bb_pb_length = get_input_value(tii, 'bb_pb_length')
    bb_pb_std_dev = get_input_value(tii, 'bb_pb_std_dev')

    if withparams:
        bb_pb_length = arglist[0]
        bb_pb_std_dev = arglist[1]

    bw_pb = bb_pb_indicator(astdt, bb_pb_length, bb_pb_std_dev)
    
    pclm = bw_pb
    clname = bw_pb.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_bb_bw(astdt, gpldt, stmdt, tii, withparams = False, *arglist):         #1 # Bollinger Bands Width
    # bb_length  = int(config['Bollinger_Bandwidth']['bb_length'])
    # bb_std_dev = int(config['Bollinger_Bandwidth']['bb_std_dev'])

    bb_length = get_input_value(tii, 'bb_length')
    bb_std_dev = get_input_value(tii, 'bb_std_dev')

    if withparams:
        bb_length = arglist[0]
        bb_std_dev = arglist[1]

    bw_bw = bb_bw_indicator(astdt, bb_length, bb_std_dev)
    
    pclm = bw_bw
    clname = bw_bw.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_cmf(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #1 # Chaikin Money Flow
    # cmf_length = int(config['Chaikin_Money_Flow']['cmf_length'])

    cmf_length = get_input_value(tii, 'cmf_length')

    if withparams:
        cmf_length = arglist[0]

    cmf = chaikin_money_flow(astdt, cmf_length)
    
    pclm = cmf
    clname = cmf.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_co(astdt, gpldt, stmdt, tii, withparams = False, *arglist):            #1 # Chaikin Oscillator
    # co_short_length = int(config['Chaikin_Oscillator']['co_short_length'])
    # co_long_length  = int(config['Chaikin_Oscillator']['co_long_length'])

    co_short_length = get_input_value(tii, 'co_short_length')
    co_long_length = get_input_value(tii, 'co_long_length')

    if withparams:
        co_short_length = arglist[0]    
        co_long_length = arglist[1]    

    ch_osc = chaikin_oscillator(astdt, co_short_length, co_long_length)
    
    pclm = ch_osc
    clname = ch_osc.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_cmo(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #1 # Chande Momentum Oscillator
    # cmo_length = int(config['Chande_Momentum_Oscillator']['cmo_length'])

    cmo_length = get_input_value(tii, 'cmo_length')

    if withparams:
        cmo_length = arglist[0] 

    cmo_ = cmo(astdt, cmo_length)
    
    pclm = cmo_
    clname = cmo_.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_cci(astdt, gpldt, stmdt, tii, withparams = False, *arglist):       #T  #1 # Commodity Channel Index
    # cci_length  = int(config['Commodity_Channel_Index']['cci_length'])
    # cci_mul     = float(config['Commodity_Channel_Index']['cci_mul'])
    cci_length = get_input_value(tii, 'cci_length')
    cci_mul = get_input_value(tii, 'cci_mul')

    if withparams:
        cci_length = arglist[0] 
        cci_mul = arglist[1] 
    
    apltdt, bsrets = trade_with_cci(astdt, cci_length, cci_mul)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_cci, [cci_length, cci_mul]]
    stmdt['Commodity Channel Index'] = sargs

    return gpldt

def get_mdt_cc(astdt, gpldt, stmdt, tii, withparams = False, *arglist):        #T  #1 # Coppock Curve
    # cc_length = int(config['Coppock_Curve']['cc_length'])
    cc_length = get_input_value(tii, 'cc_length')
    
    if withparams:
        cc_length = arglist[0]

    apltdt, bsrets = trade_with_cc(astdt, cc_length)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_cc, [cc_length]]
    stmdt['Coppock Curve'] = sargs

    return gpldt

def get_mdt_dmi(astdt, gpldt, stmdt, tii, withparams = False, *arglist):       #T  #1 # Directional Movement Index
    # dmi_length = int(config['Directional_Movement_Index']['dmi_length'])
    dmi_length = get_input_value(tii, 'dmi_length')

    if withparams:
        dmi_length = arglist[0]
    
    apltdt, bsrets = trade_with_adx(astdt, dmi_length)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_adx, [dmi_length]]
    stmdt['Directional Movement Index'] = sargs

    return gpldt

def get_mdt_dc(astdt, gpldt, stmdt, tii, withparams = False, *arglist):        #T  #0 # Donchian Channels
    # dc_length = int(config['Donchian_Channel']['dc_length'])
    dc_length = get_input_value(tii, 'dc_length')

    if withparams:
        dc_length = arglist[0]

    apltdt, bsrets = trade_with_dc(astdt, dc_length)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_dc, [dc_length]]
    stmdt['Donchian Channel'] = sargs

    return gpldt

def get_mdt_dema(astdt, gpldt, stmdt, tii, withparams = False, *arglist):          #0 # Double Exponential Moving Avearge
    # dema_length = int(config['Double_Exponential_Moving_Avearge']['dema_length'])
    dema_length = get_input_value(tii, 'dema_length')

    if withparams:
        dema_length = arglist[0]

    dema = dema_indicator(astdt, dema_length)
    
    pclm = dema
    clname = dema.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_eom(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #1 # Ease of Movement
    # eom_length   = int(config['Ease_of_Movement']['eom_length'])
    eom_length = get_input_value(tii, 'eom_length')

    if withparams:
        eom_length = arglist[0]
    
    eom = ease_of_movement(astdt, eom_length)
    
    pclm = eom
    clname = eom.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_hma(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #0 # Hull Moving Average
    # hma_period = int(config['Hull_Moving_Average']['hma_period'])
    hma_period = get_input_value(tii, 'hma_period')
    close_col = get_input_value(tii, 'close_col')

    if withparams:
        hma_period = arglist[0]
        close_col = arglist[1]

    hma = hma_indicator(data=astdt, n=hma_period, close_col=close_col)
    
    pclm = hma
    clname = hma.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_ic(astdt, gpldt, stmdt, tii, withparams = False, *arglist):            #0 # Ichimoku Cloud
    # ic_n1   = int(config['Ichimoku_Cloud']['ic_conversion_line_period'])
    # ic_n2   = int(config['Ichimoku_Cloud']['ic_baseline_period'])
    # ic_n3   = int(config['Ichimoku_Cloud']['ic_lagging_spen_period'])
    # ic_n4   = int(config['Ichimoku_Cloud']['ic_displacement'])

    ic_n1 = get_input_value(tii, 'ic_conversion_line_period')
    ic_n2 = get_input_value(tii, 'ic_baseline_period')
    ic_n3 = get_input_value(tii, 'ic_lagging_spen_period')
    ic_n4 = get_input_value(tii, 'ic_displacement')

    if withparams:
        ic_n1 = arglist[0]
        ic_n2 = arglist[1]
        ic_n3 = arglist[2]
        ic_n4 = arglist[3]

    ic_ = ichimoku_cloud_indicator(astdt, ic_n1, ic_n2, ic_n3, ic_n4)
    
    apltdt = ic_
    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    return gpldt

def get_mdt_po(astdt, gpldt, stmdt, tii, withparams = False, *arglist):        #T  #1 # Price Oscillator
    # po_short_length = int(config['Price_Oscillator']['po_short_length'])
    # po_long_length  = int(config['Price_Oscillator']['po_long_length'])
    po_short_length = get_input_value(tii, 'po_short_length')
    po_long_length = get_input_value(tii, 'po_long_length')
    close_col = get_input_value(tii, 'close_col')

    if withparams:
        po_short_length = arglist[0]
        po_long_length = arglist[1]
        close_col = arglist[2]

    apltdt, bsrets = trade_with_po(astdt, po_short_length, po_long_length, close_col)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_po, [po_short_length, po_long_length, close_col]]
    stmdt['Price Oscillator'] = sargs

    return gpldt

def get_mdt_kc(astdt, gpldt, stmdt, tii, withparams = False, *arglist):        #T  #0 # Keltner Channels
    # kc_length   = int(config['Keltner_Channels']['kc_length'])
    kc_length = get_input_value(tii,'kc_length')
    if withparams:
        kc_length = arglist[0]
    apltdt, bsrets = trade_with_kc(astdt, kc_length)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_kc, [kc_length]]
    stmdt['Keltner Channels'] = sargs

    return gpldt

def get_mdt_kst(astdt, gpldt, stmdt, tii, withparams = False, *arglist):       #T  #1 # Know Sure Thing (KST) Oscillator
    # kst_roc_length_1    = int(config['KST_Oscillator']['kst_roc_length_1'])
    # kst_roc_length_2    = int(config['KST_Oscillator']['kst_roc_length_2'])
    # kst_roc_length_3    = int(config['KST_Oscillator']['kst_roc_length_3'])
    # kst_roc_length_4    = int(config['KST_Oscillator']['kst_roc_length_4'])
    # kst_sma_length_1    = int(config['KST_Oscillator']['kst_sma_length_1'])
    # kst_sma_length_2    = int(config['KST_Oscillator']['kst_sma_length_2'])
    # kst_sma_length_3    = int(config['KST_Oscillator']['kst_sma_length_3'])
    # kst_sma_length_4    = int(config['KST_Oscillator']['kst_sma_length_4'])
    # kst_sig_length      = int(config['KST_Oscillator']['kst_sig_length'])
    
    kst_roc_length_1 = get_input_value(tii,'kst_roc_length_1')
    kst_roc_length_2 = get_input_value(tii,'kst_roc_length_2')
    kst_roc_length_3 = get_input_value(tii,'kst_roc_length_3')
    kst_roc_length_4 = get_input_value(tii,'kst_roc_length_4')
    kst_sma_length_1 = get_input_value(tii,'kst_sma_length_1')
    kst_sma_length_2 = get_input_value(tii,'kst_sma_length_2')
    kst_sma_length_3 = get_input_value(tii,'kst_sma_length_3')
    kst_sma_length_4 = get_input_value(tii,'kst_sma_length_4')
    kst_sig_length = get_input_value(tii,'kst_sig_length')

    if withparams:
        kst_roc_length_1 = arglist[0]
        kst_roc_length_2 = arglist[1]
        kst_roc_length_3 = arglist[2]
        kst_roc_length_4 = arglist[3]
        kst_sma_length_1 = arglist[4]
        kst_sma_length_2 = arglist[5]
        kst_sma_length_3 = arglist[6]
        kst_sma_length_4 = arglist[7]
        kst_sig_length = arglist[8]
    
    apltdt, bsrets = trade_with_kst(astdt, kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, 
                                    kst_sma_length_1, kst_sma_length_2, kst_sma_length_3, kst_sma_length_4, kst_sig_length)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_kst, [kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, 
             kst_sma_length_1, kst_sma_length_2, kst_sma_length_3, kst_sma_length_4]]
    stmdt['KST Oscilator'] = sargs

    return gpldt

def get_mdt_macross(astdt, gpldt, stmdt, tii, withparams = False, *arglist):   #T  #0 # MA Cross
    # ma_type     = config['MA_Cross']['ma_type']
    # length_fast = int(config['MA_Cross']['length_fast'])
    # length_slow = int(config['MA_Cross']['length_slow'])
    ma_type = get_input_value(tii, 'ma_type')
    length_fast = get_input_value(tii, 'length_fast')
    length_slow = get_input_value(tii, 'length_slow')

    if withparams:
        ma_type = arglist[0]
        length_fast = arglist[1]
        length_slow = arglist[2]

    apltdt, bsrets = trade_with_macross(astdt, ma_type, length_fast, length_slow)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_macross, [ma_type, length_fast, length_slow]]
    stmdt['MA Cross'] = sargs

    return gpldt

def get_mdt_macd(astdt, gpldt, stmdt, tii, withparams = False, *arglist):      #T  #1 # MACD
    macd_short_period       = get_input_value(tii, 'macd_short_period')
    macd_long_period        = get_input_value(tii, 'macd_long_period')
    macd_signal_smoothing   = get_input_value(tii, 'macd_signal_smoothing')
    close_col   = get_input_value(tii, 'close_col')

    if withparams:
        macd_short_period = arglist[0]
        macd_long_period = arglist[1]
        macd_signal_smoothing = arglist[2]
        close_col = arglist[3]

    apltdt, bsrets = trade_with_macd(astdt, macd_short_period, macd_long_period,macd_signal_smoothing,close_col)

    macd_histogram = apltdt['MACD'] - apltdt['MACDSig']

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})

    gpldt.append({'x': astdt.Date, 'y': macd_histogram, 'type': 'histogram', 'name': 'MACDHistogram'})
    
    sargs = [train_for_macd, [macd_short_period, macd_long_period, macd_signal_smoothing, close_col]]
    stmdt['MACD'] = sargs

    return gpldt

def get_mdt_mi(astdt, gpldt, stmdt, tii, withparams = False, *arglist):            #1 # Mass Index
    # mi_high_period = int(config['Mass_Index']['mi_high_period'])
    # mi_low_period = int(config['Mass_Index']['mi_low_period'])

    mi_high_period = get_input_value(tii,'mi_high_period')
    mi_low_period = get_input_value(tii,'mi_low_period')

    if withparams:
        mi_high_period = arglist[0]
        mi_low_period = arglist[1]

    mi = mass_index(astdt, mi_low_period, mi_high_period)
    
    pclm = mi
    clname = mi.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_mom(astdt, gpldt, stmdt, tii, withparams = False, *arglist):       #T  #1 # Momentum
    # mom_length = int(config['Momentum']['mom_length'])
    mom_length = get_input_value(tii,'mom_length')
    if withparams:
        mom_length = arglist[0]
    apltdt, bsrets = trade_with_mom(astdt, mom_length)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_mom, [mom_length]]
    stmdt['Momentum'] = sargs

    return gpldt

def get_mdt_mfi(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #1 # Money Flow Index
    # mfi_length = int(config['Money_Flow_Index']['mfi_length'])
    mfi_length = get_input_value(tii,'mfi_length')
    if withparams:
        mfi_length = arglist[0]
    mfi = money_flow_index(astdt, mfi_length)
    
    pclm = mfi
    clname = mfi.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})

    sma_length = int(config['Money_Flow_Index']['sma_length'])
    mfi_sma = money_flow_index_sma(mfi, sma_length)

    # append mfi_sma
    pclm = mfi_sma
    clname = mfi_sma.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})

    l = len(pclm)
    mfi_high = pd.Series([80] * l, name='mfi_high')
    mfi_mid = pd.Series([50] * l, name='mfi_mid')
    mfi_low = pd.Series([20] * l, name='mfi_low')

    gpldt.append({'x': astdt.Date, 'y': mfi_high, 'type': 'line', 'name': mfi_high.name})
    gpldt.append({'x': astdt.Date, 'y': mfi_mid, 'type': 'line', 'name': mfi_mid.name})
    gpldt.append({'x': astdt.Date, 'y': mfi_low, 'type': 'line', 'name': mfi_low.name})

    return gpldt

def get_mdt_ema(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #0 # Moving Average Exponential
    # ema_length = int(config['Moving_Average_Exponential']['ema_length'])
    ema_length = get_input_value(tii, 'ema_length')
    close_col = get_input_value(tii, 'close_col')
    if withparams:
        ema_length = arglist[0]
        close_col = arglist[1]

    ema_ = ema_indicator(astdt[close_col], ema_length)
    
    pclm = ema_
    clname = ema_.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_sma(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #0 # Moving Average Simple
    # sma_length = int(config['Moving_Average_Simple']['sma_length'])
    sma_length = get_input_value(tii,'sma_length')
    if withparams:
        sma_length = arglist[0]
    sma_ = sma_indicator(astdt['Close'], sma_length)
    
    pclm = sma_
    clname = sma_.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_tema(astdt, gpldt, stmdt, tii, withparams = False, *arglist):          #0 # Triple EMA
    # tema_length = int(config['Triple_Exponential_Moving_Avearge']['tema_length'])
    tema_length = get_input_value(tii,'tema_length')
    if withparams:
        tema_length = arglist[0]
    tema = tema_indicator(astdt, tema_length)
    
    pclm = tema
    clname = tema.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_obv(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #1 # On Balance Volume
    obv = on_balance_volume(astdt['Close'], astdt['Volume'], False)
    pclm = obv
    clname = obv.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_rsi(astdt, gpldt, stmdt, tii, withparams = False, *arglist):       #T  #1 # Relative Strength Index
    # rsi_length = int(config['Relative_Strength_Index']['rsi_length'])
    rsi_length = get_input_value(tii, 'rsi_length')
    close_col = get_input_value(tii, 'close_col')
    if withparams:
        rsi_length = arglist[0]
        close_col = arglist[1]
    apltdt, bsrets = trade_with_rsi(astdt, rsi_length, close_col)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_rsi, [rsi_length, close_col]]
    stmdt['Relative Strength Index'] = sargs

    return gpldt

def get_mdt_smma(astdt, gpldt, stmdt, tii, withparams = False, *arglist):          #0 # Smoothed Moving Average
    # smma_length = int(config['Smoothed_Moving_Average']['smma_length'])
    smma_length = get_input_value(tii, 'smma_length')
    close_col = get_input_value(tii, 'close_col')
    if withparams:
        smma_length = arglist[0]
        close_col = arglist[1]
    smma = smooth_ma_indicator(data=astdt, n=smma_length, close_col=close_col)
    
    pclm = smma
    clname = smma.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_stoch(astdt, gpldt, stmdt, tii, withparams = False, *arglist):     #T  #1 # Stochastic
    # s_k         = int(config['Stochastic']['s_k'])
    # s_d         = int(config['Stochastic']['s_d'])
    # s_smooth    = int(config['Stochastic']['s_smooth'])
    s_k = get_input_value(tii, 's_k')
    s_d = get_input_value(tii, 's_d')
    s_smooth = get_input_value(tii, 's_smooth')
    if withparams:
        s_k = arglist[0]
        s_d = arglist[1]
        s_smooth = arglist[2]


    apltdt, bsrets = trade_with_stoch(astdt, s_k, s_d, s_smooth)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_stoch, [s_k, s_d, s_smooth]]
    stmdt['Stochastic'] = sargs

    return gpldt

def get_mdt_stchrsi(astdt, gpldt, stmdt, tii, withparams = False, *arglist):   #T  #1 # Stochastic RSI
    # stch_length = int(config['StochasticRSI']['stch_length'])
    stch_length = get_input_value(tii, 'stch_length')
    close_col = get_input_value(tii, 'close_col')
    if withparams:
        stch_length = arglist[0]
        close_col = arglist[1]
    apltdt, bsrets = trade_with_stchrsi(astdt, stch_length, close_col)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_stchrsi, [stch_length]]
    stmdt['Stochastic RSI'] = sargs

    return gpldt

def get_mdt_trix(astdt, gpldt, stmdt, tii, withparams = False, *arglist):      #T  #1 # TRIX
    # trix_length = int(config['Trix']['trix_length'])
    trix_length = get_input_value(tii, 'trix_length')
    if withparams:
        trix_length = arglist[0]
    apltdt, bsrets = trade_with_trix(astdt, trix_length)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_trix, [trix_length]]
    stmdt['TRIX'] = sargs

    return gpldt

def get_mdt_tsi(astdt, gpldt, stmdt, tii, withparams = False, *arglist):       #T  #1 # True Strength Index
    # tsi_long_length  = int(config['True_Strength_Index']['tsi_long_length'])
    # tsi_short_length = int(config['True_Strength_Index']['tsi_short_length'])
    tsi_long_length = get_input_value(tii, 'tsi_long_length')
    tsi_short_length = get_input_value(tii, 'tsi_short_length')
    if withparams:
        tsi_long_length = arglist[0]
        tsi_short_length = arglist[1]
    apltdt, bsrets = trade_with_tsi(astdt, tsi_long_length, tsi_short_length)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_tsi, [tsi_long_length, tsi_short_length]]
    stmdt['True Strength Index'] = sargs

    return gpldt

def get_mdt_uo(astdt, gpldt, stmdt, tii, withparams = False, *arglist):            #1 # Ultimate Oscilator
    # uo_period_1 = int(config['Ultimate_Oscillator']['uo_period_1'])
    # uo_period_2 = int(config['Ultimate_Oscillator']['uo_period_2'])
    # uo_period_3 = int(config['Ultimate_Oscillator']['uo_period_3'])
    # uo_ws       = int(config['Ultimate_Oscillator']['uo_ws'])
    # uo_wm       = int(config['Ultimate_Oscillator']['uo_wm'])
    # uo_wl       = int(config['Ultimate_Oscillator']['uo_wl'])

    uo_period_1 = get_input_value(tii, 'uo_period_1')
    uo_period_2 = get_input_value(tii, 'uo_period_2')
    uo_period_3 = get_input_value(tii, 'uo_period_3')
    uo_ws = get_input_value(tii, 'uo_ws')
    uo_wm = get_input_value(tii, 'uo_wm')
    uo_wl = get_input_value(tii, 'uo_wl')

    if withparams:
        uo_period_1 = arglist[0]
        uo_period_2 = arglist[1]
        uo_period_3 = arglist[2]
        uo_ws = arglist[3]
        uo_wm = arglist[4]
        uo_wl = arglist[5]

    uo_ = uo(astdt, uo_period_1, uo_period_2, uo_period_3, uo_ws, uo_wm, uo_wl)
    
    pclm = uo_
    clname = uo_.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_volume(astdt, gpldt, stmdt, tii, withparams = False, *arglist):        #1 # Volume     
    volume_ = volume_index_indicator(astdt)
    
    apltdt = volume_
    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    return gpldt

def get_mdt_vo(astdt, gpldt, stmdt, tii, withparams = False, *arglist):            #1 # Volume Oscilator
    # vo_short_length = int(config['Volume_Oscillator']['vo_short_length'])
    # vo_long_length  = int(config['Volume_Oscillator']['vo_long_length'])
    vo_short_length = get_input_value(tii, 'vo_short_length')
    vo_long_length = get_input_value(tii, 'vo_long_length')
    if withparams:
        vo_short_length = arglist[0]
        vo_long_length = arglist[1]
    vo_ = vo_indicator(astdt, vo_short_length, vo_long_length)
    
    pclm = vo_
    clname = vo_.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_voi(astdt, gpldt, stmdt, tii, withparams = False, *arglist):       #T  #1 # Vortex Indicator
    # voi_length = int(config['Vortex_Indicator']['voi_length'])
    voi_length = get_input_value(tii, 'voi_length')
    if withparams:
        voi_length = arglist[0]
    apltdt, bsrets = trade_with_voi(astdt, voi_length)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_voi, [voi_length]]
    stmdt['Vortex Indicator'] = sargs

    return gpldt

def get_mdt_wma(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #0 # Weighted Moving Average
    # wma_length = int(config['Moving_Average_Weighted']['wma_length'])
    wma_length = get_input_value(tii, 'wma_length')
    close_col = get_input_value(tii, 'close_col')
    if withparams:
        wma_length = arglist[0]
        close_col = arglist[1]

    wma = wma_indicator(astdt[close_col], wma_length)
    
    pclm = wma
    clname = wma.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt

def get_mdt_wpr(astdt, gpldt, stmdt, tii, withparams = False, *arglist):       #T  #1 # Williams % R
    # wpr_length = int(config['Williams_PR']['wpr_length'])
    wpr_length = get_input_value(tii, 'wpr_length')
    if withparams:
        wpr_length = arglist[0]
    apltdt, bsrets = trade_with_wpr(astdt, wpr_length)

    clnames = list(apltdt.head(0))
    for idx in range(len(apltdt.columns)):
        pclm = apltdt.iloc[:, idx]
        gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clnames[idx]})
    
    sargs = [train_for_wpr, [wpr_length]]
    stmdt['Williams % R'] = sargs

    return gpldt


def get_mdt_bop(astdt, gpldt, stmdt, tii, withparams = False, *arglist):           #1 # Advance/Decline

    bop_ = bop(astdt)
    
    pclm = bop_
    clname = bop_.name
    gpldt.append({'x': astdt.Date, 'y': pclm, 'type': 'line', 'name': clname})
    
    return gpldt