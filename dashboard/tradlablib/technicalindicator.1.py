from .model_guilib import *
from .model_stats import *
from .exec_trade import *
from .model_train import *
from .libind.volume import *

all_options = {
    'Momentum': ['Awesome Oscillator', 'Chande Momentum Oscillator', 'Coppock Curve', 'Momentum', 'Money Flow Index', 'Price Oscillator',
                 'Relative Strength Index', 'Stochastic', 'Stochastic RSI', 'True Strength Index', 'Ultimate Oscillator', 'Williams % R'],
    'Trend': ['Aroon', 'Average Directional Index', 'Commodity Channel Index', 'Directional Movement Index', 
              'Double Exponential Moving Avearge', 'Hull MA', 'Ichimoku Cloud', 'Know Sure Thing (KST) Oscillator', 'MA Cross', 
              'MACD', 'Mass Index', 'Moving Average Exponential', 'Moving Average Simple', 'Moving Average Weighted', 'Smoothed Moving Average', 
              'TRIX', 'Triple EMA', 'Vortex Indicator'],
    'Volatility': ['Average True Range', 'Bollinger Bands', 'Bollinger Bands % B', 'Bollinger Bands Width', 'Donchian Channels', 'Keltner Channels'],
    'Volume': ['Accumulation Distribution Index', 'Chaikin Money Flow', 'Chaikin Oscillator', 'Ease of Movement', 'On Balance Volume', 'Volume',
               'Volume Oscillator'],
}

all_options_ids = {
    'Momentum': [['Awesome Oscillator','ao'], ['Chande Momentum Oscillator','cmo'], ['Coppock Curve','cc'], ['Momentum','mom'], ['Money Flow Index','mfi'], ['Price Oscillator','po'],
                 ['Relative Strength Index','rsi'], ['Stochastic','stoch'], ['Stochastic RSI','stchrsi'], ['True Strength Index','tsi'], ['Ultimate Oscillator','uo'], ['Williams % R','wpr']],
    'Trend': [['Aroon','aroon'], ['Average Directional Index','adi'], ['Commodity Channel Index','cci'], ['Directional Movement Index','dmi'], 
              ['Double Exponential Moving Avearge','dema'], ['Hull MA','hma'], ['Ichimoku Cloud','ic'], ['Know Sure Thing (KST) Oscillator','kst'], ['MA Cross','mc'], 
              ['MACD','macd'], ['Mass Index','mi'], ['Moving Average Exponential','mae'], ['Moving Average Simple','mas'], ['Moving Average Weighted','maw'], ['Smoothed Moving Average','sma'], 
              ['TRIX','trix'], ['Triple EMA','tema'], ['Vortex Indicator','voi']],
    'Volatility': [['Average True Range','atr'], ['Bollinger Bands','bb'], ['Bollinger Bands % B','bb_pb'], ['Bollinger Bands Width','bb_bw'], ['Donchian Channels','dc'], ['Keltner Channels','kc']],
    'Volume': [['Accumulation Distribution Index','acc'], ['Chaikin Money Flow','cmf'], ['Chaikin Oscillator','co'], ['Ease of Movement','eom'], ['On Balance Volume','obv'], ['Volume','volume'],
               ['Volume Oscillator','vo']],
}



def display_graphs(df, selector):

    stats_mdt = {}
    graphs = []     #### will draw with seperate
    if 'Accumulation Distribution Index' in selector:
        graphs.append({
            'id' : 'acc',
            'data': get_mdt_acc(df, [], stats_mdt),
            'title': 'Accumulation Distribution Index',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Accumulation Distribution Index', None)

    if 'Aroon' in selector:
        graphs.append({
            'id' : 'aroon',
            'data': get_mdt_aroon(df, [], stats_mdt),
            'title': 'Aroon',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Aroon', None)

    if 'Average Directional Index' in selector:
        graphs.append({
            'id' : 'adi',
            'data': get_mdt_adi(df, [], stats_mdt),
            'title': 'Average Directional Index',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Average Directional Index', None)

    if 'Average True Range' in selector:
        graphs.append({
            'id' : 'atr',
            'data': get_mdt_atr(df, [], stats_mdt),
            'title': 'Average True Range',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Average True Range', None)

    if 'Awesome Oscillator' in selector:
        graphs.append({
            'id' : 'ao',
            'data': get_mdt_ao(df, [], stats_mdt),
            'title': 'Awesome Oscillator',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Awesome Oscillator', None)

    if 'Bollinger Bands % B' in selector:
        graphs.append({
            'id' : 'bb_pb',
            'data': get_mdt_bb_pb(df, [], stats_mdt),
            'title': 'Bollinger Bands % B',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Bollinger Bands % B', None)
        
    if 'Bollinger Bands Width' in selector:
        graphs.append({
            'id' : 'bb_bw',
            'data': get_mdt_bb_bw(df, [], stats_mdt),
            'title': 'Bollinger Bands Width',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Bollinger Bands Width', None)
        
    if 'Chaikin Money Flow' in selector:
        graphs.append({
            'id' : 'cmf',
            'data': get_mdt_cmf(df, [], stats_mdt),
            'title': 'Chaikin Money Flow',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Chaikin Money Flow', None)
        
    if 'Chaikin Oscillator' in selector:
        graphs.append({
            'id' : 'co',
            'data': get_mdt_co(df, [], stats_mdt),
            'title': 'Chaikin Oscillator',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Chaikin Oscillator', None)
        
    if 'Chande Momentum Oscillator' in selector:
        graphs.append({
            'id' : 'cmo',
            'data': get_mdt_cmo(df, [], stats_mdt),
            'title': 'Chande Momentum Oscillator',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Chande Momentum Oscillator', None)
        
    if 'Commodity Channel Index' in selector:
        graphs.append({
            'id' : 'cci',
            'data': get_mdt_cci(df, [], stats_mdt),
            'title': 'Commodity Channel Index',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Commodity Channel Index', None)
        
    if 'Coppock Curve' in selector:
        graphs.append({
            'id' : 'cc',
            'data': get_mdt_cc(df, [], stats_mdt),
            'title': 'Coppock Curve',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Coppock Curve', None)
        
    if 'Directional Movement Index' in selector:
        graphs.append({
            'id' : 'dmi',
            'data': get_mdt_dmi(df, [], stats_mdt),
            'title': 'Directional Movement Index',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Directional Movement Index', None)
        
    if 'Ease of Movement' in selector:
        graphs.append({
            'id' : 'eom',
            'data': get_mdt_eom(df, [], stats_mdt),
            'title': 'Ease of Movement',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Ease of Movement', None)
        
    if 'Know Sure Thing (KST) Oscillator' in selector:
        graphs.append({
            'id' : 'kst',
            'data': get_mdt_kst(df, [], stats_mdt),
            'title': 'Know Sure Thing (KST) Oscillator',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Know Sure Thing (KST) Oscillator', None)

    if 'MACD' in selector:
        graphs.append({
            'id' : 'macd',
            'data': get_mdt_macd(df, [], stats_mdt),
            'title': 'MACD',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('MACD', None)
        
    if 'Mass Index' in selector:
        graphs.append({
            'id' : 'mi',
            'data': get_mdt_mi(df, [], stats_mdt),
            'title': 'Mass Index',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Mass Index', None)
        
    if 'Momentum' in selector:
        graphs.append({
            'id' : 'mom',
            'data': get_mdt_mom(df, [], stats_mdt),
            'title': 'Momentum',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Momentum', None)
        
    if 'Money Flow Index' in selector:
        graphs.append({
            'id' :'mfi',
            'data': get_mdt_mfi(df, [], stats_mdt),
            'title': 'Money Flow Index',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Money Flow Index', None)
        
    if 'On Balance Volume' in selector:
        graphs.append({
            'id' :'obv',
            'data': get_mdt_obv(df, [], stats_mdt),
            'title': 'On Balance Volume',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('On Balance Volume', None)
        
    if 'Price Oscillator' in selector:
        graphs.append({
            'id' :'po',
            'data': get_mdt_po(df, [], stats_mdt),
            'title': 'Price Oscillator',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Price Oscillator', None)
        
    if 'Relative Strength Index' in selector:
        graphs.append({
            'id' :'rsi',
            'data': get_mdt_rsi(df, [], stats_mdt),
            'title': 'Relative Strength Index',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Relative Strength Index', None)
        
    if 'Stochastic' in selector:
        graphs.append({
            'id' :'stoch',
            'data': get_mdt_stoch(df, [], stats_mdt),
            'title': 'Stochastic',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Stochastic', None)
        
    if 'Stochastic RSI' in selector:
        graphs.append({
            'id' :'stchrsi',
            'data': get_mdt_stchrsi(df, [], stats_mdt),
            'title': 'Stochastic RSI',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Stochastic RSI', None)
        
    if 'TRIX' in selector:
        graphs.append({
            'id' :'trix',
            'data': get_mdt_trix(df, [], stats_mdt),
            'title': 'TRIX',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('TRIX', None)
        
    if 'True Strength Index' in selector:
        graphs.append({
            'id' :'tsi',
            'data': get_mdt_tsi(df, [], stats_mdt),
            'title': 'True Strength Index',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('True Strength Index', None)
        
    if 'Ultimate Oscillator' in selector:
        graphs.append({
            'id' :'uo',
            'data': get_mdt_uo(df, [], stats_mdt),
            'title': 'Ultimate Oscillator',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Ultimate Oscillator', None)
        
    if 'Volume' in selector:
        graphs.append({
            'id' :'volume',
            'data': get_mdt_volume(df, [], stats_mdt),
            'title': 'Volume',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Volume', None)
        
    if 'Volume Oscillator' in selector:
        graphs.append({
            'id' :'vo',
            'data': get_mdt_vo(df, [], stats_mdt),
            'title': 'Volume Oscillator',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Volume Oscillator', None)
        
    if 'Vortex Indicator' in selector:
        graphs.append({
            'id' :'voi',
            'data': get_mdt_voi(df, [], stats_mdt),
            'title': 'Vortex Indicator',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Vortex Indicator', None)
        
    if 'Williams % R' in selector:
        graphs.append({
            'id' : 'wpr',
            'data': get_mdt_wpr(df, [], stats_mdt),
            'title': 'Williams % R',
            'displayModeBar': False
        })
    else:
        res = stats_mdt.pop('Williams % R', None)


    orgdata = []           ## will draw with the main chart body

    ######## update source image
    if 'Bollinger Bands' in selector:
        orgdata.append({ 'id' : 'bb', 'data' : get_mdt_bb(df, [], stats_mdt), 'title' : 'Bollinger Bands'})
    else:
        res = stats_mdt.pop('Bollinger Bands', None)

    if 'Donchian Channels' in selector:
        orgdata.append({ 'id' : 'dc', 'data' : get_mdt_dc(df, [], stats_mdt), 'title' : 'Donchian Channels'})
    else:
        res = stats_mdt.pop('Donchian Channels', None)

    if 'Double Exponential Moving Avearge' in selector:
        orgdata.append({ 'id' : 'dema', 'data' : get_mdt_dema(df, [], stats_mdt), 'title' : 'Double Exponential Moving Avearge'})
    else:
        res = stats_mdt.pop('Double Exponential Moving Avearge', None)

    if 'Hull MA' in selector:
        orgdata.append({ 'id' : 'hma', 'data' : get_mdt_hma(df, [], stats_mdt), 'title' : 'Hull MA'})
    else:
        res = stats_mdt.pop('Hull MA', None)

    if 'Ichimoku Cloud' in selector:
        orgdata.append({ 'id' : 'ic', 'data' : get_mdt_ic(df, [], stats_mdt), 'title' : 'Ichimoku Cloud'})
    else:
        res = stats_mdt.pop('Ichimoku Cloud', None)

    if 'Keltner Channels' in selector:
        orgdata.append({ 'id' : 'kc', 'data' : get_mdt_kc(df, [], stats_mdt), 'title' : 'Keltner Channels'})
    else:
        res = stats_mdt.pop('Keltner Channels', None)

    if 'MA Cross' in selector:
        orgdata.append({ 'id' : 'mc', 'data' : get_mdt_macross(df, [], stats_mdt), 'title' : 'MA Cross'})
    else:
        res = stats_mdt.pop('MA Cross', None)
        
    if 'Moving Average Exponential' in selector:
        orgdata.append({ 'id' : 'mae', 'data' : get_mdt_ema(df, [], stats_mdt), 'title' : 'Moving Average Exponential'})
    else:
        res = stats_mdt.pop('Moving Average Exponential', None)

    if 'Moving Average Simple' in selector:
        orgdata.append({ 'id' : 'mas', 'data' : get_mdt_sma(df, [], stats_mdt), 'title' : 'Moving Average Simple'})
    else:
        res = stats_mdt.pop('Moving Average Simple', None)

    if 'Smoothed Moving Average' in selector:
        orgdata.append({ 'id' : 'sma', 'data' : get_mdt_smma(df, [], stats_mdt), 'title' : 'Smoothed Moving Average'})
    else:
        res = stats_mdt.pop('Smoothed Moving Average', None)

    if 'Triple EMA' in selector:
        orgdata.append({ 'id' : 'tema', 'data' : get_mdt_tema(df, [], stats_mdt), 'title' : 'Triple EMA'})
    else:
        res = stats_mdt.pop('Triple EMA', None)

    if 'Moving Average Weighted' in selector:
        orgdata.append({ 'id' : 'maw', 'data' : get_mdt_wma(df, [], stats_mdt), 'title' : 'Moving Average Weighted'})
    else:
        res = stats_mdt.pop('Moving Average Weighted', None)


    for dt in graphs:
        for pltdt in dt['data']:
            pltdt['x'] = pltdt['x'].tolist()
            pltdt['y'] = pltdt['y'].fillna(0).tolist()

    for dt in orgdata:
        for pltdt in dt['data']:
            pltdt['x'] = pltdt['x'].tolist()
            pltdt['y'] = pltdt['y'].fillna(0).tolist()

    return orgdata, graphs


def display_indicators(df, selector):

    stats_mdt = {}
    graphs = []     #### will draw with seperate

    if 'Accumulation Distribution Index' in selector:
        graphs.append({
            'id' : 'acc',
            'data': get_mdt_acc(df, [], stats_mdt),
            'title': 'Accumulation Distribution Index',
        })
    else:
        res = stats_mdt.pop('Accumulation Distribution Index', None)

    orgdata = []           ## will draw with the main chart body

    ######## update source image
    if 'Bollinger Bands' in selector:
        orgdata.append({ 'id' : 'bb', 'data' : get_mdt_bb(df, [], stats_mdt), 'title' : 'Bollinger Bands'})
    else:
        res = stats_mdt.pop('Bollinger Bands', None)
