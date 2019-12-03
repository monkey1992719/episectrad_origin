# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from exec_trade import *
from model_train import *
from libind.volume import *


def print_res_ti(tiname, titag, tiparam_a, pltdtti):
    name_str = titag+'_'+'_'.join(str(tiparam) for tiparam in tiparam_a)
    name_str+='.csv'
    param_str = ' '.join(str(tiparam) for tiparam in tiparam_a)
    pltdtti.to_csv('../data/results/'+'pltdt-'+name_str)
    print()
    print(tiname+' Params: ['+param_str+'].\n')
    print('Data Frame with '+tiname+' indicator.\n')
    print(pltdtti)


def print_res_all(tiname, titag, tiparam_a, pltdtti, bsrets, psetb, bret):
    name_str = titag+'_'+'_'.join(str(tiparam) for tiparam in tiparam_a)
    name_str+='.csv'
    param_str = ' '.join(str(tiparam) for tiparam in tiparam_a)
    pltdtti.to_csv('../data/results/'+'pltdt-'+name_str)
    bsrets.to_csv('../data/results/'+'bsrets-'+name_str)
    bret.to_csv('../data/results/bret-'+titag+'.csv')
    print()
    print(tiname+' Params: ['+param_str+'].\n')
    print('Data Frame and Trade Returns with Buy/Sell.\n')
    print(pltdtti)
    print(bsrets)    
    print('\n')
    print('Training Results and best parameter set.\n')
    print(psetb)
    print(bret)

# 0-plot on src window, 1-plot in new window
    
"""-- Accumulation/Distribution Test --"""#1
def ts_acc_ti(df):
    acc_ = acc_dist_index(df)
    pltdtti = pd.concat([df, acc_], axis=1)
    print_res_ti('Accumulation/Distribution', 'acc', [], pltdtti)

"""-- Average Directional Index Test --"""#1
def ts_adi_ti(df, adi_length):
    adin    = adi_indicator(df, adi_length)
    pltdtti = pd.concat([df, adin], axis=1)
    print_res_ti('Average Directional Index', 'ad_index', [adi_length], pltdtti)

"""-- Aroon Indicator Test --"""#1
def ts_aroon_ti(df, aroon_length):
    aroon = aroon_indicator(df, aroon_length)
    pltdtti = pd.concat([df, aroon], axis=1)
    print_res_ti('Aroon Indicator', 'aroon', [aroon_length], pltdtti)

"""-- Average True Range Test --"""#1
def ts_atr_ti(df, atr_length):
    apltdt, bsrets = trade_with_atr(df, atr_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_atr(df, atr_length)
    print_res_all('Average True Range', 'atr', [atr_length], pltdtti, bsrets, psetb, bret)

"""-- Awesome Oscillator Test --"""#1
def ts_ao_ti(df, ao_short_length, ao_long_length):
    apltdt, bsrets = trade_with_ao(df, ao_short_length, ao_long_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_ao(df, ao_short_length, ao_long_length)
    print_res_all('Awesome Oscillator', 'ao', [ao_short_length, ao_long_length], pltdtti, bsrets, psetb, bret)
    
"""-- Bollinger Band Test --"""#0
def ts_bb_ti(pltdt, bb_length, bb_std_dev):
    apltdt, bsrets = trade_with_bb(pltdt, bb_length, bb_std_dev)
    pltdtti = pd.concat([pltdt, apltdt], axis=1)
    psetb, bret = train_for_bb(pltdt, bb_length, bb_std_dev)
    print_res_all('Bollinger Band', 'bb', [bb_length, bb_std_dev], pltdtti, bsrets, psetb, bret)

"""-- Bollinger Bands Width Test --"""#1
def ts_bb_bw_ti(df, bb_length, bb_std_dev):
    bw = bb_bw_indicator(df, bb_length, bb_std_dev)
    pltdtti = pd.concat([df, bw], axis=1)
    print_res_ti('Bollinger Bands Width', 'bw', [bb_length, bb_std_dev], pltdtti)

"""-- Bollinger Bands %B Test --"""#1
def ts_bb_pb_ti(df, bb_pb_length, bb_pb_std_dev):
    bb_pb = bb_pb_indicator(df, bb_pb_length, bb_pb_std_dev)
    pltdtti = pd.concat([df, bb_pb], axis=1)
    print_res_ti('Bollinger Bands %B', 'bb_pb', [bb_pb_length, bb_pb_std_dev], pltdtti)
    
"""-- Chaikin Money Flow Test --"""#1
def ts_cmf_ti(df, cmf_length):
    cmf = chaikin_money_flow(df, cmf_length)
    pltdtti = pd.concat([df, cmf], axis=1)
    print_res_ti('Chaikin Money Flow', 'cmf', [cmf_length], pltdtti)


"""-- Chaikin Oscillator Test --"""#1
def ts_co_ti(df, co_short_length, co_long_length):
    ch_osc = chaikin_oscillator(df, co_short_length, co_long_length)
    pltdtti = pd.concat([df, ch_osc], axis=1)
    print_res_ti('Chaikin Oscilator', 'co', [co_short_length, co_long_length], pltdtti)

"""-- Chande Momentum Oscillator Test --"""#1
def ts_cmo_ti(df, cmo_length):
    cmo_ = cmo(df, cmo_length)
    pltdtti = pd.concat([df, cmo_], axis=1)
    print_res_ti('Chande Momentum Oscillator', 'cmo', [cmo_length], pltdtti)
   
"""-- Commodity Channel Index Test --"""#1
def ts_cci_ti(df, cci_length, cci_mul):
    apltdt, bsrets = trade_with_cci(df, cci_length, cci_mul)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_cci(df, cci_length, cci_mul)
    print_res_all('Commodity Channel Index', 'cci', [cci_length, cci_mul], pltdtti, bsrets, psetb, bret)
   
"""-- Coppock Curve Test --"""#1
def ts_cc_ti(df, cc_length):
    apltdt, bsrets = trade_with_cc(df, cc_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_cc(df, cc_length)
    print_res_all('Coppock Curve', 'cc', [cc_length], pltdtti, bsrets, psetb, bret)

"""-- Directional Movement Index Test --"""#1
def ts_dmi_ti(df, dmi_length):
    apltdt, bsrets = trade_with_adx(df, dmi_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_adx(df, dmi_length)
    print_res_all('Directional Movement Index', 'dmi',  [dmi_length], pltdtti, bsrets, psetb, bret)

"""-- Donchian Channel Test -- """#0
def ts_dc_ti(df, dc_length):
    apltdt, bsrets = trade_with_dc(df, dc_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_dc(df, dc_length)
    print_res_all('Donchian Channel', 'dc', [dc_length], pltdtti, bsrets, psetb, bret)

"""-- Double Exponential Moving Avearge Test --"""#0
def ts_dema_ti(df, dema_length):
    dema = dema_indicator(df, dema_length)
    pltdtti = pd.concat([df, dema], axis=1)
    print_res_ti('Double Exponential Moving Avearge', 'dema', [dema_length], pltdtti)    
    
"""-- Ease of Movement Test--"""#1
def ts_eom_ti(df, eom_length):
    eom = ease_of_movement(df, eom_length)
    pltdtti = pd.concat([df, eom], axis=1)
    print_res_ti('Ease of Movement', 'eom', [eom_length], pltdtti)

"""-- Hull Moving Average Test --"""#0
def ts_hma_ti(df, hma_period):
    hma = hma_indicator(df, hma_period)
    pltdtti = pd.concat([df, hma], axis=1)
    print_res_ti('Hull Moving Average', 'hma', [hma_period], pltdtti) 

"""-- Ichimoku Cloud Test -- """#0
def ts_ic_ti(df, ic_conversion_line_period, ic_baseline_period, ic_lagging_spen_period, ic_displacement):
    ic_ = ichimoku_cloud_indicator(df, ic_conversion_line_period, ic_baseline_period, ic_lagging_spen_period, ic_displacement)
    pltdtti = pd.concat([df, ic_], axis=1)
    print_res_ti('Ichimoku Cloud', 'ic', [ic_conversion_line_period, ic_baseline_period, ic_lagging_spen_period, ic_displacement], pltdtti)

"""-- Price Oscillator Test --"""#1
def ts_po_ti(df, po_short_length, po_long_length):
    apltdt, bsrets = trade_with_po(df, po_short_length, po_long_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_po(df, po_short_length, po_long_length)
    print_res_all('Price Oscilator', 'po', [po_short_length, po_long_length], pltdtti, bsrets, psetb, bret)
    
"""-- Keltner Channels Test --"""#0
def ts_kc_ti(df, kc_length):
    apltdt, bsrets = trade_with_kc(df, kc_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_kc(df, kc_length)
    print_res_all('Keltner Channels ', 'kc', [kc_length], pltdtti, bsrets, psetb, bret)

"""-- KST Oscilator Test --"""#1
def ts_kst_ti(pltdt, kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, kst_sma_length_1, 
            kst_sma_length_2, kst_sma_length_3, kst_sma_length_4):
    
    apltdt, bsrets = trade_with_kst(pltdt, kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, kst_sma_length_1, 
            kst_sma_length_2, kst_sma_length_3, kst_sma_length_4)
    pltdtti = pd.concat([pltdt, apltdt], axis=1)
    psetb, bret = train_for_kst(pltdt, kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, kst_sma_length_1, 
            kst_sma_length_2, kst_sma_length_3, kst_sma_length_4)
    print_res_all('KST Oscilator', 'kst', [kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, kst_sma_length_1, 
            kst_sma_length_2, kst_sma_length_3, kst_sma_length_4], pltdtti, bsrets, psetb, bret)
    
"""-- MA Cross Test --"""#0
def ts_ma_cross_ti(pltdt, ma_type, ma_length_fast, ma_length_slow):
    apltdt, bsrets = trade_with_ma_cross(pltdt, ma_type, ma_length_fast, ma_length_slow)
    pltdtti = pd.concat([pltdt, apltdt], axis=1)
    psetb, bret = train_for_ma_cross(pltdt, ma_type, ma_length_fast, ma_length_slow)
    print_res_all('MA Cross', 'ma_cross', [ma_type, ma_length_fast, ma_length_slow], pltdtti, bsrets, psetb, bret)
    
"""-- MACD Test --"""#1
def ts_macd_ti(pltdt, macd_short_period, macd_long_period, macd_signal_smoothing):
    apltdt, bsrets = trade_with_macd(pltdt, macd_short_period, macd_long_period, macd_signal_smoothing)
    pltdtti = pd.concat([pltdt, apltdt], axis=1)
    psetb, bret = train_for_macd(pltdt, macd_short_period, macd_long_period, macd_signal_smoothing)
    print_res_all('MACD', 'macd', [macd_short_period, macd_long_period, macd_signal_smoothing], pltdtti, bsrets, psetb, bret)

"""-- Mass Index Test --"""#1
def ts_mi_ti(df, mi_low_period, mi_high_period):
    mi = mass_index(df, mi_low_period, mi_high_period)
    pltdtti = pd.concat([df, mi], axis=1)
    print_res_ti('Mass Index', 'mi', [mi_low_period, mi_high_period], pltdtti)

"""-- Momentum Test --"""#1
def ts_mom_ti(df, mom_length):
    apltdt, bsrets = trade_with_mom(df, mom_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_mom(df, mom_length)
    print_res_all('Momentum', 'mom', [mom_length], pltdtti, bsrets, psetb, bret)
   
"""-- Money Flow Index Test --"""#1
def ts_mfi_ti(df, mfi_length):
    mfi = money_flow_index(df, mfi_length)
    pltdtti = pd.concat([df, mfi], axis=1)
    print_res_ti('Money Flow Index Test', 'mfi', [mfi_length], pltdtti)

"""-- Moving Averages Tests --"""
"""-- Exponential Moving Average Tests --"""#0
def ts_ema_ti(pltdt, ema_length):
    ema_ = ema_indicator(pltdt['Close'], ema_length)
    pltdtti = pd.concat([pltdt, ema_], axis=1)
    print_res_ti('EMA', 'ema', [ema_length], pltdtti)

"""-- Simple Moving Average Test --"""#0
def ts_sma_ti(pltdt, sma_length):
    sma = sma_indicator(pltdt['Close'], sma_length)
    pltdtti = pd.concat([pltdt, sma], axis=1)
    print_res_ti('Simple Moving Average', 'sma', [sma_length], pltdtti)

"""-- Triple EMA Test --"""#0
def ts_tema_ti(df, tema_length):
    tema = tema_indicator(df, tema_length)
    pltdtti = pd.concat([df, tema], axis=1)
    print_res_ti('Triple Exponential Moving Avearge', 'tema', [tema_length], pltdtti)

"""-- On Balance Volume Test --"""#1
def ts_obv_ti(df):
    obv = on_balance_volume(df['Close'], df['Volume'], False)
    pltdtti = pd.concat([df, obv], axis=1)
    print_res_ti('On Blance Volume', 'obv', [], pltdtti)

"""-- Relative Strength Index Test --"""#1
def ts_rsi_ti(df, rsi_length):
    apltdt, bsrets = trade_with_rsi(df, rsi_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_rsi(df, rsi_length)
    print_res_all('Relative Strength Index', 'rsi',  [rsi_length], pltdtti, bsrets, psetb, bret)

"""-- Smoothed Moving Average Test --"""#0
def ts_smooth_ma_ti(df, sma_length):
    smooth_ma = smooth_ma_indicator(df, sma_length)
    pltdtti = pd.concat([df, smooth_ma], axis=1)
    print_res_ti('Smoothed Moving Average', 'smooth_ma', [sma_length], pltdtti)

"""-- Stochastic Test --"""#1
def ts_stoch_ti(df, s_k, s_d, s_smooth):
    apltdt, bsrets = trade_with_stoch(df, s_k, s_d, s_smooth)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_stoch(df, s_k, s_d, s_smooth)
    print_res_all('Stochastic', 'stoch', [s_k, s_d, s_smooth], pltdtti, bsrets, psetb, bret)
    
"""-- Stochastic RSI Test --"""#1
def ts_stchrsi_ti(df, stch_length):
    apltdt, bsrets = trade_with_stchrsi(df, stch_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_stchrsi(df, stch_length)
    print_res_all('Stochastic RSI', 'stch_rsi',  [stch_length], pltdtti, bsrets, psetb, bret)
  
"""-- Trix Indicator Test --"""#1
def ts_trix_ti(df, trix_length):
    apltdt, bsrets = trade_with_trix(df, trix_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_trix(df, trix_length)
    print_res_all('TRIX', 'trix', [trix_length], pltdtti, bsrets, psetb, bret)
    
"""-- True Strength Index Test --"""#1
def ts_tsi_ti(df, tsi_long_length, tsi_short_length):
    apltdt, bsrets = trade_with_tsi(df, tsi_long_length, tsi_short_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_tsi(df, tsi_long_length, tsi_short_length)
    print_res_all('True Strength Index', 'tsi',  [tsi_long_length, tsi_short_length], pltdtti, bsrets, psetb, bret)

"""-- Ultimate Oscilator Test --"""#1
def ts_uo_ti(df, uo_period_1, uo_period_2, uo_period_3, uo_ws, uo_wm, uo_wl):
    uo_ = uo(df, uo_period_1, uo_period_2, uo_period_3, uo_ws, uo_wm, uo_wl)
    pltdtti = pd.concat([df, uo_], axis=1)
    print_res_ti('Ultimate Oscilator', 'uo', [uo_period_1, uo_period_2, uo_period_3, uo_period_3, uo_ws, uo_wm, uo_wl], pltdtti)
    
"""-- Volume Index Test --"""#1 # This is skipped. Wrapper not written.
def ts_vi_ti(df):
    vo_index = volume_index_indicator(df)
    pltdtti = pd.concat([df, vo_index], axis=1)
    print_res_ti('Volume Index', 'vi', [], pltdtti)

"""-- Volume Oscilator Test --"""#1
def ts_vo_ti(df, vo_short_length, vo_long_length):
    vo = vo_indicator(df, vo_short_length, vo_long_length)
    pltdtti = pd.concat([df, vo], axis=1)
    print_res_ti('Volume Oscilator', 'vo', [vo_short_length, vo_long_length], pltdtti)

"""-- Vortex Indicator Test --"""#1  
def ts_voi_ti(df, voi_length):
    apltdt, bsrets = trade_with_voi(df, voi_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_voi(df, voi_length)
    print_res_all('Vortex Indicator', 'voi',  [voi_length], pltdtti, bsrets, psetb, bret)

"""-- Weighted Moving Average Test --"""#0
def ts_wma_ti(df, wma_length):
    wma = wma_indicator(df['Close'], wma_length)
    pltdtti = pd.concat([df, wma], axis=1)
    print_res_ti('Weighted Moving Average Test', 'wma', [wma_length], pltdtti)

"""-- Williams %R Test --"""#1
def ts_wpr_ti(df, wpr_length):
    apltdt, bsrets = trade_with_wpr(df, wpr_length)
    pltdtti = pd.concat([df, apltdt], axis=1)
    psetb, bret = train_for_wpr(df, wpr_length)
    print_res_all('Williams%R', 'wpr_rsi',  [wpr_length], pltdtti, bsrets, psetb, bret)
   
    

