# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import configparser
import json

import matplotlib
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import pyplot
from pylab import *

from pandas import DataFrame
from pandas_datareader import data
from pandas_datareader import data as pdr

from test_suite import *
from exec_trade import *
from model_stats import *
from model_guilib import *

# Read the params.ini file
config = configparser.ConfigParser()
ini = config.read('../params.ini')
indicators = json.loads(config.get("DEFAULT", "indicators"))
param3 = json.loads(config.get(indicators[3], 'iparams'))
ema_length = config[indicators[3]][param3[0]]
ema_length = config['Moving_Average_Exponential']['ema_length']


# Read the Data CSV file from path ../data
df = pd.read_csv('../data/NSEI.csv', sep=',')
df = pd.DataFrame(df)
df = dropna(df)

pltdt = pd.DataFrame()
pltdt['Date'] = df['Date']
pltdt['Close'] = df['Close']
#pltdt['Volume'] = df['Volume'].astype(int)





atr_length = int(config['Average_True_Range']['atr_length'])
#ts_atr_ti(df, atr_length)
argsatr = [train_for_atr, [atr_length]]
psetb, wlsts = get_stats_singleti(df, *argsatr)

bb_length   = int(config['Bollinger_Bands']['bb_length'])
bb_std_dev  = int(config['Bollinger_Bands']['bb_std_dev'])
args = (pltdt, bb_length, bb_std_dev)
args = (bb_length, bb_std_dev)
#ts_bb_ti(pltdt, *args)
argsbb = [train_for_bb, [bb_length, bb_std_dev]]
psetb, wlsts = get_stats_singleti(df, *argsbb)

dc_length = int(config['Donchian_Channel']['dc_length'])
#ts_dc_ti(df, dc_length)
argsdc = [train_for_dc, [dc_length]]
psetb, wlsts = get_stats_singleti(df, *argsdc)

kc_length   = int(config['Keltner_Channels']['kc_length'])
#ts_kc_ti(df, kc_length)
argskc = [train_for_kc, [kc_length]]
psetb, wlsts = get_stats_singleti(df, *argskc)

args1 = [argsdc, argskc, argsbb, argsatr]
ret, wlsts = get_stats_comboti(df, *args1)
print("combo of ATR, BB, DC, KC and Master is DC")
print('Returns%: '+str(ret))
print(wlsts)


''''''
ts_acc_ti(df)

adi_length = int(config['Average_Directional_Index']['adi_length'])
ts_adi_ti(df, adi_length)

aroon_length = int(config['Aroon']['aroon_length'])
ts_aroon_ti(df, aroon_length)

atr_length = int(config['Average_True_Range']['atr_length'])
ts_atr_ti(df, atr_length)
argsatr = [train_for_atr, [atr_length]]
psetb, wlsts = get_stats_singleti(df, *argsatr)
print_stats('Average True Range', psetb, wlsts)

ao_short_length = int(config['Awesome_Oscillator']['ao_short_length'])
ao_long_length  = int(config['Awesome_Oscillator']['ao_long_length'])
ts_ao_ti(df, ao_short_length, ao_long_length)
argsao = [train_for_ao, [ao_short_length, ao_long_length]]
psetb, wlsts = get_stats_singleti(df, *argsao)
print_stats('Awesome Oscillator', psetb, wlsts)

bb_length  = int(config['Bollinger_Bandwidth']['bb_length'])
bb_std_dev = int(config['Bollinger_Bandwidth']['bb_std_dev'])
ts_bb_bw_ti(df, bb_length, bb_std_dev)

bb_pb_length = int(config['Bollinger_Bands_PB']['bb_pb_length'])
bb_pb_std_dev = int(config['Bollinger_Bands_PB']['bb_pb_std_dev'])
ts_bb_pb_ti(df, bb_pb_length, bb_pb_std_dev)

bb_length   = int(config['Bollinger_Bands']['bb_length'])
bb_std_dev  = int(config['Bollinger_Bands']['bb_std_dev'])
#args1 = (pltdt, bb_length, bb_std_dev)
args = (bb_length, bb_std_dev)
ts_bb_ti(pltdt, *args)
argsbb = (train_for_bb, (bb_length, bb_std_dev))
psetb, wlsts = get_stats_singleti(df, *argsbb)
print_stats('Bollinger Bands', psetb, wlsts)

cc_length = int(config['Coppock_Curve']['cc_length'])
ts_cc_ti(df, cc_length)
argscc = [train_for_cc, [cc_length]]
psetb, wlsts = get_stats_singleti(df, *argscc)
print_stats('Coppock Curve', psetb, wlsts)

cmf_length = int(config['Chaikin_Money_Flow']['cmf_length'])
ts_cmf_ti(df, cmf_length)

cmo_length = int(config['Chande_Momentum_Oscillator']['cmo_length'])
ts_cmo_ti(df, cmo_length)

co_short_length = int(config['Chaikin_Oscillator']['co_short_length'])
co_long_length  = int(config['Chaikin_Oscillator']['co_long_length'])
ts_co_ti(df, co_short_length, co_long_length)

cci_length  = int(config['Commodity_Channel_Index']['cci_length'])
cci_mul     = float(config['Commodity_Channel_Index']['cci_mul'])
ts_cci_ti(df, cci_length, cci_mul)
argscci = [train_for_cci, [cci_length, cci_mul]]
psetb, wlsts = get_stats_singleti(df, *argscci)
print_stats('Commodity Channel Index', psetb, wlsts)

dema_length = int(config['Double_Exponential_Moving_Avearge']['dema_length'])
ts_dema_ti(df, dema_length)

dmi_length = int(config['Directional_Movement_Index']['dmi_length'])
ts_dmi_ti(df, dmi_length)
argsdmi = [train_for_adx, [dmi_length]]
psetb, wlsts = get_stats_singleti(df, *argsdmi)
print_stats('Directional_Movement_Index', psetb, wlsts)

dc_length = int(config['Donchian_Channel']['dc_length'])
ts_dc_ti(df, dc_length)
argsdc = [train_for_dc, [dc_length]]
psetb, wlsts = get_stats_singleti(df, *argsdc)
print_stats('Donchian_Channel', psetb, wlsts)

hma_period = int(config['Hull_Moving_Average']['hma_period'])
ts_hma_ti(df, hma_period)

ic_n1   = int(config['Ichimoku_Cloud']['ic_conversion_line_period'])
ic_n2   = int(config['Ichimoku_Cloud']['ic_baseline_period'])
ic_n3   = int(config['Ichimoku_Cloud']['ic_lagging_spen_period'])
ic_n4   = int(config['Ichimoku_Cloud']['ic_displacement'])
ts_ic_ti(df, ic_n1, ic_n2, ic_n3, ic_n4)

po_short_length = int(config['Price_Oscillator']['po_short_length'])
po_long_length  = int(config['Price_Oscillator']['po_long_length'])
ts_po_ti(df, po_short_length, po_long_length)
argspo = [train_for_po, [po_short_length, po_long_length]]
psetb, wlsts = get_stats_singleti(df, *argspo)
print_stats('Price_Oscillator', psetb, wlsts)

rsi_length = int(config['Relative_Strength_Index']['rsi_length'])
ts_rsi_ti(df, rsi_length)
argsatr = [train_for_rsi, [rsi_length]]
psetb, wlsts = get_stats_singleti(df, *argsatr)
print_stats('Relative_Strength_Index', psetb, wlsts)

kc_length   = int(config['Keltner_Channels']['kc_length'])
ts_kc_ti(df, kc_length)
argskc = [train_for_kc, [kc_length]]
psetb, wlsts = get_stats_singleti(df, *argskc)
print_stats('Keltner_Channels', psetb, wlsts)

kst_roc_length_1    = int(config['KST_Oscillator']['kst_roc_length_1'])
kst_roc_length_2    = int(config['KST_Oscillator']['kst_roc_length_2'])
kst_roc_length_3    = int(config['KST_Oscillator']['kst_roc_length_3'])
kst_roc_length_4    = int(config['KST_Oscillator']['kst_roc_length_4'])
kst_sma_length_1    = int(config['KST_Oscillator']['kst_sma_length_1'])
kst_sma_length_2    = int(config['KST_Oscillator']['kst_sma_length_2'])
kst_sma_length_3    = int(config['KST_Oscillator']['kst_sma_length_3'])
kst_sma_length_4    = int(config['KST_Oscillator']['kst_sma_length_4'])
kst_sig_length      = int(config['KST_Oscillator']['kst_sig_length'])
ts_kst_ti(pltdt, kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, 
          kst_sma_length_1, kst_sma_length_2, kst_sma_length_3, kst_sma_length_4)
argskst = [train_for_kst, [kst_roc_length_1, kst_roc_length_2, kst_roc_length_3, kst_roc_length_4, 
          kst_sma_length_1, kst_sma_length_2, kst_sma_length_3, kst_sma_length_4]]
psetb, wlsts = get_stats_singleti(df, *argskst)
print_stats('KST_Oscillator', psetb, wlsts)

macd_short_period       = int(config['MACD']['macd_short_period'])
macd_long_period        = int(config['MACD']['macd_long_period'])
macd_signal_smoothing   = int(config['MACD']['macd_signal_smoothing'])
ts_macd_ti(pltdt, macd_short_period, macd_long_period, macd_signal_smoothing)
argsmacd = [train_for_macd, [macd_short_period, macd_long_period, macd_signal_smoothing]]
psetb, wlsts = get_stats_singleti(df, *argsmacd)
print_stats('MACD', psetb, wlsts)

ma_type     = config['MA_Cross']['ma_type']
length_fast = int(config['MA_Cross']['length_fast'])
length_slow = int(config['MA_Cross']['length_slow'])
ts_ma_cross_ti(pltdt, ma_type, length_fast, length_slow)
argsmac = [train_for_ma_cross, [ma_type, length_fast, length_slow]]
psetb, wlsts = get_stats_singleti(df, *argsmac)
print_stats('MA_Cross', psetb, wlsts)

mfi_length = int(config['Money_Flow_Index']['mfi_length'])
ts_mfi_ti(df, mfi_length)

mom_length = int(config['Momentum']['mom_length'])
ts_mom_ti(df, mom_length)
argsmom = [train_for_mom, [mom_length]]
psetb, wlsts = get_stats_singleti(df, *argsmom)
print_stats('Momentum', psetb, wlsts)

mi_high_period = int(config['Mass_Index']['mi_high_period'])
mi_low_period = int(config['Mass_Index']['mi_low_period'])
ts_mi_ti(df, mi_low_period, mi_high_period)

eom_length   = int(config['Ease_of_Movement']['eom_length'])
ts_eom_ti(df, eom_length)

ema_length = int(config['Moving_Average_Exponential']['ema_length'])
ts_ema_ti(pltdt, ema_length)

stch_length = int(config['StochasticRSI']['stch_length'])
ts_stchrsi_ti(df, stch_length)
argsastchrsi = [train_for_stchrsi, [stch_length]]
psetb, wlsts = get_stats_singleti(df, *argsastchrsi)
print_stats('StochasticRSI', psetb, wlsts)

smma_length = int(config['Smoothed_Moving_Average']['smma_length'])
ts_smooth_ma_ti(df, smma_length)

sma_length = int(config['Moving_Average_Simple']['sma_length'])
ts_sma_ti(pltdt, sma_length)

tema_length = int(config['Triple_Exponential_Moving_Avearge']['tema_length'])
ts_tema_ti(df, tema_length)

trix_length = int(config['Trix']['trix_length'])
ts_trix_ti(df, trix_length)
argstrix = [train_for_trix, [trix_length]]
psetb, wlsts = get_stats_singleti(df, *argstrix)
print_stats('Trix', psetb, wlsts)

tsi_long_length  = int(config['True_Strength_Index']['tsi_long_length'])
tsi_short_length = int(config['True_Strength_Index']['tsi_short_length'])
ts_tsi_ti(df, tsi_long_length, tsi_short_length)
argstsi = [train_for_tsi, [tsi_long_length, tsi_short_length]]
psetb, wlsts = get_stats_singleti(df, *argstsi)
print_stats('True_Strength_Index', psetb, wlsts)

wma_length = int(config['Moving_Average_Weighted']['wma_length'])
ts_wma_ti(df, wma_length)

ts_obv_ti(df)

s_k         = int(config['Stochastic']['s_k'])
s_d         = int(config['Stochastic']['s_d'])
s_smooth    = int(config['Stochastic']['s_smooth'])
ts_stoch_ti(df, s_k, s_d, s_smooth)
argsastch = [train_for_stoch, [s_k, s_d, s_smooth]]
psetb, wlsts = get_stats_singleti(df, *argsastch)
print_stats('Stochastic', psetb, wlsts)

uo_period_1 = int(config['Ultimate_Oscillator']['uo_period_1'])
uo_period_2 = int(config['Ultimate_Oscillator']['uo_period_2'])
uo_period_3 = int(config['Ultimate_Oscillator']['uo_period_3'])
uo_ws       = int(config['Ultimate_Oscillator']['uo_ws'])
uo_wm       = int(config['Ultimate_Oscillator']['uo_wm'])
uo_wl       = int(config['Ultimate_Oscillator']['uo_wl'])
ts_uo_ti(df, uo_period_1, uo_period_2, uo_period_3, uo_ws, uo_wm, uo_wl)

ts_vi_ti(df)

vo_short_length = int(config['Volume_Oscillator']['vo_short_length'])
vo_long_length  = int(config['Volume_Oscillator']['vo_long_length'])
ts_vo_ti(df, vo_short_length, vo_long_length)

voi_length = int(config['Vortex_Indicator']['voi_length'])
ts_voi_ti(df, voi_length)
argsavoi = [train_for_voi, [voi_length]]
psetb, wlsts = get_stats_singleti(df, *argsavoi)
print_stats('Vortex_Indicator', psetb, wlsts)

wpr_length = int(config['Williams_PR']['wpr_length'])
ts_wpr_ti(df, wpr_length)
argsawpr = [train_for_wpr, [wpr_length]]
psetb, wlsts = get_stats_singleti(df, *argsawpr)
print_stats('Williams_PR', psetb, wlsts)
''''''
