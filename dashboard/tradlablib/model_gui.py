# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
import configparser
import json
import threading
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

import plotly.graph_objs as go
import plotly.tools as tls
import ipdb

from pandas import DataFrame
from pandas_datareader import data
from pandas_datareader import data as pdr
from dash.dependencies import Input, Output, State, Event

from model_guilib import *
from model_stats import *
from exec_trade import *
from model_train import *
from libind.volume import *


app = dash.Dash()

# Read the params.ini file
config = configparser.ConfigParser()
ini = config.read('params.ini')

# Read the Data CSV file from path ../data
df = pd.read_csv('../data/NSEI.csv', sep=',')

df = pd.DataFrame(df)
df = dropna(df)

pltdt = pd.DataFrame()
pltdt['Date'] = df['Date']
pltdt['Close'] = df['Close']

# buySellData = []
initial = []
globalArray = []
stats_mdt = {}
globalStats = {}

globalbuysellSlectedValue = 0

data = []
data.append({'x': pltdt.Date, 'y': pltdt.Close, 'type': 'line', 'name': 'Close'})

def get_results(*args):
    print('Arguments for get_result:')
    print(args)
    print(stats_mdt)
    
    spv = ''
    if args[0] == 'All':    # Run for indicator combination.
        sargslist = []
        master = args[3]
        sargslist.append(stats_mdt[master]) # Add the master key first.
        for key in stats_mdt.keys():
            if key != master:
                sargslist.append(stats_mdt[key])
        
        ret, wlsts = get_stats_comboti(df, *sargslist)
        
        spv = 'Returns%: '+str(round(ret, 2))
        spv += '\n'
    else:   # Run for single indicator.
        sargs = stats_mdt[args[0]]
        psetb, wlsts = get_stats_singleti(df, *sargs)

        spv = 'Best Params and Returns ('+args[0]+'):'
        spv += '\n'
        values = list(psetb)
        spv += '[ '
        nprms = len(values) - 2
        for idx in range(nprms):
            if idx == nprms - 1:
                spv += str(values[idx])+' ]' # last param element
            else:    
                spv += str(values[idx])+', '
        spv += ', ' + str(round(values[nprms], 2))+'%'
        spv += '\n'
        
    spv += '\n'
    spv += 'Win/Loss Stats'
    spv += '\n'
    spv += 'Win% (win/loss): '+ str(round(wlsts.loc[0][2], 2)) + '% (' + str(wlsts.loc[0][0]) + '/' + str(wlsts.loc[0][1]) + ')'
    spv += '\n'
    
    return spv


# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})  # noqa: E501

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


# Root DIV
app.layout = html.Div([ 

# Children DIV
    html.Div([

#  children First DIV
       html.Div([
        # Header Div   
        html.Div([
            html.H1(children='Trading Laboratory')

        ],style={ 'backgroundColor':'#fff',} ),

        # Button Div  
        html.Div([
         html.Button('Indicators', id='indicatorButton'),
         ],style={ 
         'backgroundColor':'#fff' }),

        # Pop up window
           html.Div(id='popUpWindow', children=[
 html.Div([
        html.Div(
            [
                html.P('Indicators:',
                        className='nine columns'),
               
            ], className="row",style={
                           'border-bottom': '1px solid #dedede',
                    }),
 
        html.Div(
            [
                html.Div(
                    [
                        html.P('Category:'),
                        dcc.RadioItems(
                                id = 'Category',
                                options=[{'label': k, 'value': k} for k in all_options.keys()],
                                value='Trend'
                        )
                    ],
                    
                    className='four columns'),
                html.Div(
                    [
                        html.P('Technical Indicator:'),

                        dcc.Checklist(
                                id = 'TechnicalIndicator',
                                options=[
                                     {'label': 'Aroon', 'value': 'Aroon'},
                                ],
                                     values=['']
                            
                        )
                    ],
                    
                    className='eight columns',
                    style={
                           'border-left': '1px solid #dedede',
                           'padding-left':'5px',
                    }
                )
            ], className="row")
    ], style={ 
         'backgroundColor':'#fff',
         'border': '2px solid #dedede',
         'border-radius':'5px',
         'padding-left':'5px',

         'zIndex':'9',
         'position':'absolute' ,
         'width':'800px',
         'top':'110px'
          
         
         
        } ,className='five columns offset-by-one')  
    ], hidden=True),

        

        # Plot1 Div  
        html.Div([
            dcc.Graph(
                id='src-graph',
                figure={
                    'data': data,
                    'layout': {
                    #    'height': 300
                    }
                },
                config={
                    'displayModeBar': False
                }  
            ),

        html.Div(id='newGraphWindow'),
            html.Div(
                dcc.Graph(
                    id='empty',
                     figure={'data': []}
                     ),
                      style={'display': 'none'}
                     )
        ],
        style={ 
            'height':'60vh'
         }
    ),
       ], className= 'eight columns'),

# children Second DIV
       html.Div(id='TLOptions',children=[
        #    option buy sell signal div
        html.Div([
            html.Label('Option buy/sell signal:',style={

                'font-size':'30px'
            }),

            html.Div(id='RadioButtonWindow'),
            html.Div(
               dcc.RadioItems(
                 id = 'optionBuySells',
                  options=[],
                #  value='',
                #  style={
                #    'padding-right':'10px',
                #    'font-size':'17px',
                #    'display': 'none'
                #    },
                )
            ),
            # All button div
        # html.Div(id='AllButtonDiv',children=[
        #     html.Button('All', id='AllButton')
        # ],style = {
        #      'display': 'none'
        # }),
        html.Div(id='AllButtonDiv',children=[
          html.Div(
              dcc.RadioItems(
                 id = 'AllButton',
                 options=[ {'label': 'All', 'value': 'All'}],
                 value='',
                 style={
                   },
                )
              
            #   html.Button('All', id='AllButton'),
            #  style={
                #  'display': 'block'
                
                 )
        ]),
        
        
        html.Div(id='popUpWindowForAllButton',children=[
        html.Div(id='closeButton',children=[

        ], style={'display': 'none'})
        ]),
        html.Div(id='popwinTesting'),
                        html.Div(
                            dcc.RadioItems(
                                id = 'InsidePopUp',
                                options=[],
                        )
                        ),
       
        html.Div([
        html.Label('Signal Close:',style={

                'font-size':'30px',
                'margin-top': '15px'
            }),
            html.Div(id='SignalClose'),
             html.Div(
                 dcc.RadioItems(
                 id = 'signal Active',
                 options=[{'label': 'Signal Active until it changes', 'value': 'signalActive'}],
                 value='',
                 style={
                   'font-size':'17px'},
                )
             )
          ]),

          html.Div([
           html.Label('Backtest Length:',style={

                'font-size':'30px',
                'margin-top': '15px'
            }),
             html.Div(id='backTest'),
             html.Div(
               dcc.RadioItems(
              id = 'BackTestLength',
            options=[
                {'label': 'default', 'value': '0'},
                {'label': '6 months', 'value': '6'},
                {'label': '12 months', 'value': '12'},
                {'label': '36 months', 'value': '36'}
           ],
           style={
                'padding-right':'10px',
                'font-size':'17px'
            },
                labelStyle={'display': 'inline-block'}
                )
             )
          

          ]),
          html.Div(id='runButton',children=[
              html.Button('run')
          ])
     
           
        
        ],style={ 
            'border-bottom': '1px solid #dedede'
               }),
        #  Trading lab statics  div
        html.Div(id='container'),
        html.Div(
             style={'display': 'none'}
        )
        
       ] ,style={ 
         'backgroundColor':'#fff',
          'border-left': '5px solid #dedede',
         'border-radius':'5px',
         'padding-left':'5px',
         'margin-left': '0px',
         
        } ,className= 'four columns',hidden=False)

    ],className = "row")

])

# Trading indicators graph update callback


@app.callback(dash.dependencies.Output('src-graph', 'figure'), [dash.dependencies.Input('TechnicalIndicator', 'values')])
def update_src_image(selector):
    # print('two')
    data = []
    data.append({'x': pltdt.Date, 'y': pltdt.Close, 'type': 'line', 'name': 'Close'})
   
    if 'Bollinger Bands' in selector:
        data = get_mdt_bb(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Bollinger Bands', None)

    if 'Donchian Channels' in selector:
        data = get_mdt_dc(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Donchian Channels', None)

    if 'Double Exponential Moving Avearge' in selector:
        data = get_mdt_dema(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Double Exponential Moving Avearge', None)

    if 'Hull MA' in selector:
        data = get_mdt_hma(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Hull MA', None)

    if 'Ichimoku Cloud' in selector:
        data = get_mdt_ic(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Ichimoku Cloud', None)

    if 'Keltner Channels' in selector:
        data = get_mdt_kc(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Keltner Channels', None)

    if 'MA Cross' in selector:
        data = get_mdt_macross(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('MA Cross', None)
        
    if 'Moving Average Exponential' in selector:
        data = get_mdt_ema(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Moving Average Exponential', None)

    if 'Moving Average Simple' in selector:
        data = get_mdt_sma(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Moving Average Simple', None)

    if 'Smoothed Moving Average' in selector:
        data = get_mdt_smma(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Smoothed Moving Average', None)

    if 'Triple EMA' in selector:
        data = get_mdt_tema(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Triple EMA', None)

    if 'Moving Average Weighted' in selector:
        data = get_mdt_wma(df, data, stats_mdt)
    else:
        res = stats_mdt.pop('Moving Average Weighted', None)

    # print(stats_mdt)
   
    figure = {
        'data': data,
        'layout': {
            #'height': 300
        }
    }
    
    return figure
   
# Techincal indicators listing in pop up callback

@app.callback(
    dash.dependencies.Output('TechnicalIndicator', 'options'),
    [dash.dependencies.Input('Category', 'value')])
def set_categories_options(selected_category):
    return [{'label': i, 'value': i} for i in all_options[selected_category]]


# Indidicator button callback
@app.callback(
    dash.dependencies.Output('popUpWindow', 'style'),
    [dash.dependencies.Input('indicatorButton', 'n_clicks')],
    )
def button_toggle(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


# All button callback
@app.callback(
    dash.dependencies.Output('popUpWindowForAllButton', 'children'),
    [dash.dependencies.Input('AllButton', 'value')],
    )
def button_all_toggle(allbuttonSel):
    
    if 'All' in allbuttonSel:
        # print('something is clicking')
        time.sleep(1)
        return  html.Div(id= 'popUp',children=[

    html.Div([
                html.Div([
                html.P('Select Master:',
                        className='nine columns'),
                #html.Button('close',id='closeButton',className='three columns')
                
               
            ], className="row",style={
                           'border-bottom': '1px solid #dedede',
                    }),
 
        html.Div(
            [
                html.Div(
                    [
                        #html.P('Technical Indicator:'),
                        html.Div(id='popwinTesting'),
                        html.Div(
                            dcc.RadioItems(
                                id = 'InsidePopUp',
                                options=[{'label': k, 'value': k} for k in stats_mdt.keys()],
                        )
                        )
                        
                    ])
            ], className="row")
    ], style={ 
         'backgroundColor':'#fff',
         'border': '2px solid #dedede',
         'border-radius':'5px',
         'padding-left':'5px',

         'zIndex':'9',
         'position':'absolute' ,
         'width':'225px',
         'top':'60px',
         'right':'50px'
          
         
         
        } )
         
        ],style={ 
         'backgroundColor':'#fff',
         'display': 'block'
         },hidden=False)
    # else:
        # return {'display': 'none'}


@app.callback(
    dash.dependencies.Output('AllButtonDiv', 'style'),
    [dash.dependencies.Input('TechnicalIndicator', 'values')],
    )
def bu_toggle(selector):
    '''
    if 'Average True Range' in selector:
        return {'display': 'block'}
    if 'Awesome Oscillator' in selector:
        return {'display': 'block'}
    if 'Bollinger Bands' in selector:
        return {'display': 'block'}
    if 'Commodity Channel Index' in selector:
        return {'display': 'block'}
    if 'Coppock Curve' in selector:
        return {'display': 'block'}
    if 'Directional Movement Index' in selector:
        return {'display': 'block'}
    if 'Donchian Channels' in selector:
        return {'display': 'block'}
    if 'Keltner Channels' in selector:
        return {'display': 'block'}
    if 'Know Sure Thing (KST) Oscillator' in selector:
        return {'display': 'block'}
    if 'Momentum' in selector:
        return {'display': 'block'}
    if 'Relative Strength Index' in selector:
        return {'display': 'block'}
    if 'Stochastic' in selector:
        return {'display': 'block'}
    if 'Stochastic RSI' in selector:
        return {'display': 'block'}
    if 'TRIX' in selector:
        return {'display': 'block'}
    if 'True Strength Index' in selector:
        return {'display': 'block'}
    if 'Vortex Indicator' in selector:
        return {'display': 'block'}
    if 'Williams % R' in selector:
        return {'display': 'block'}
    '''
    if 'MACD' in selector:
        return {'display': 'block'}
    if 'MA Cross' in selector:
        return {'display': 'block'}
    if 'Price Oscillator' in selector:
        return {'display': 'block'}
       
    else:
        return {'display': 'none'}


@app.callback(Output('newGraphWindow', 'children'), [Input('TechnicalIndicator', 'values')])
def display_graphs(selector):
    # print('three')
    graphs = []
    if 'Accumulation Distribution Index' in selector:
        graphs.append(dcc.Graph(
            id = 'acc',
            figure={
                'data': get_mdt_acc(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Accumulation Distribution Index'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Accumulation Distribution Index', None)

    if 'Aroon' in selector:
        graphs.append(dcc.Graph(
            id = 'aroon',
            figure={
                'data': get_mdt_aroon(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Aroon'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Aroon', None)

    if 'Average Directional Index' in selector:
        graphs.append(dcc.Graph(
            id = 'adi',
            figure={
                'data': get_mdt_adi(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Average Directional Index'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Average Directional Index', None)

    if 'Average True Range' in selector:
        graphs.append(dcc.Graph(
            id = 'atr',
            figure={
                'data': get_mdt_atr(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Average True Range'
                }
            },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Average True Range', None)

    if 'Awesome Oscillator' in selector:
        graphs.append(dcc.Graph(
            id = 'ao',
            figure={
                'data': get_mdt_ao(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Awesome Oscillator'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Awesome Oscillator', None)

    if 'Bollinger Bands % B' in selector:
        graphs.append(dcc.Graph(
            id = 'bb_pb',
            figure={
                'data': get_mdt_bb_pb(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Bollinger Bands % B'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Bollinger Bands % B', None)
        
    if 'Bollinger Bands Width' in selector:
        graphs.append(dcc.Graph(
            id = 'bb_bw',
            figure={
                'data': get_mdt_bb_bw(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Bollinger Bands Width'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Bollinger Bands Width', None)
        
    if 'Chaikin Money Flow' in selector:
        graphs.append(dcc.Graph(
            id = 'cmf',
            figure={
                'data': get_mdt_cmf(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Chaikin Money Flow'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Chaikin Money Flow', None)
        
    if 'Chaikin Oscillator' in selector:
        graphs.append(dcc.Graph(
            id = 'co',
            figure={
                'data': get_mdt_co(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Chaikin Oscillator'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Chaikin Oscillator', None)
        
    if 'Chande Momentum Oscillator' in selector:
        graphs.append(dcc.Graph(
            id = 'cmo',
            figure={
                'data': get_mdt_cmo(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Chande Momentum Oscillator'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Chande Momentum Oscillator', None)
        
    if 'Commodity Channel Index' in selector:
        graphs.append(dcc.Graph(
            id = 'cci',
            figure={
                'data': get_mdt_cci(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Commodity Channel Index'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Commodity Channel Index', None)
        
    if 'Coppock Curve' in selector:
        graphs.append(dcc.Graph(
            id = 'cc',
            figure={
                'data': get_mdt_cc(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Coppock Curve'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Coppock Curve', None)
        
    if 'Directional Movement Index' in selector:
        graphs.append(dcc.Graph(
            id = 'dmi',
            figure={
                'data': get_mdt_dmi(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Directional Movement Index'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Directional Movement Index', None)
        
    if 'Ease of Movement' in selector:
        graphs.append(dcc.Graph(
            id = 'eom',
            figure={
                'data': get_mdt_eom(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Ease of Movement'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Ease of Movement', None)
        
    if 'Know Sure Thing (KST) Oscillator' in selector:
        graphs.append(dcc.Graph(
            id = 'kst',
            figure={
                'data': get_mdt_kst(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Know Sure Thing (KST) Oscillator'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Know Sure Thing (KST) Oscillator', None)

    if 'MACD' in selector:
        graphs.append(dcc.Graph(
            id = 'macd',
            figure={
                'data': get_mdt_macd(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'MACD'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('MACD', None)
        
    if 'Mass Index' in selector:
        graphs.append(dcc.Graph(
            id = 'mi',
            figure={
                'data': get_mdt_mi(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Mass Index'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Mass Index', None)
        
    if 'Momentum' in selector:
        graphs.append(dcc.Graph(
            id = 'mom',
            figure={
                'data': get_mdt_mom(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Momentum'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Momentum', None)
        
    if 'Money Flow Index' in selector:
        graphs.append(dcc.Graph(
            id = 'mfi',
            figure={
                'data': get_mdt_mfi(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Money Flow Index'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Money Flow Index', None)
        
    if 'On Balance Volume' in selector:
        graphs.append(dcc.Graph(
            id = 'obv',
            figure={
                'data': get_mdt_obv(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'On Balance Volume'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('On Balance Volume', None)
        
    if 'Price Oscillator' in selector:
        graphs.append(dcc.Graph(
            id = 'po',
            figure={
                'data': get_mdt_po(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Price Oscillator'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Price Oscillator', None)
        
    if 'Relative Strength Index' in selector:
        graphs.append(dcc.Graph(
            id = 'rsi',
            figure={
                'data': get_mdt_rsi(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Relative Strength Index'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Relative Strength Index', None)
        
    if 'Stochastic' in selector:
        graphs.append(dcc.Graph(
            id = 'stoch',
            figure={
                'data': get_mdt_stoch(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Stochastic'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Stochastic', None)
        
    if 'Stochastic RSI' in selector:
        graphs.append(dcc.Graph(
            id = 'stchrsi',
            figure={
                'data': get_mdt_stchrsi(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Stochastic RSI'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Stochastic RSI', None)
        
    if 'TRIX' in selector:
        graphs.append(dcc.Graph(
            id = 'trix',
            figure={
                'data': get_mdt_trix(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'TRIX'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('TRIX', None)
        
    if 'True Strength Index' in selector:
        graphs.append(dcc.Graph(
            id = 'tsi',
            figure={
                'data': get_mdt_tsi(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'True Strength Index'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('True Strength Index', None)
        
    if 'Ultimate Oscillator' in selector:
        graphs.append(dcc.Graph(
            id = 'uo',
            figure={
                'data': get_mdt_uo(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Ultimate Oscillator'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Ultimate Oscillator', None)
        
    if 'Volume' in selector:
        graphs.append(dcc.Graph(
            id = 'volume',
            figure={
                'data': get_mdt_volume(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Volume'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Volume', None)
        
    if 'Volume Oscillator' in selector:
        graphs.append(dcc.Graph(
            id = 'vo',
            figure={
                'data': get_mdt_vo(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Volume Oscillator'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Volume Oscillator', None)
        
    if 'Vortex Indicator' in selector:
        graphs.append(dcc.Graph(
            id = 'voi',
            figure={
                'data': get_mdt_voi(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Vortex Indicator'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Vortex Indicator', None)
        
    if 'Williams % R' in selector:
        graphs.append(dcc.Graph(
            id = 'wpr',
            figure={
                'data': get_mdt_wpr(df, [], stats_mdt),
                'layout': {
                    'height': 300,
                    'title': 'Williams % R'
                    }
                },
            config={
                'displayModeBar': False
                }
        ))
    else:
        res = stats_mdt.pop('Williams % R', None)

    # print(stats_mdt)
    
    return html.Div(graphs)


@app.callback(
    Output('RadioButtonWindow', 'children'),
    [Input('TechnicalIndicator', 'values'),Input('optionBuySells', 'value')])
def set_indicators(selected_Indicator,selected_optionbuysell):
    buySellData = []
    buySellData.append(selected_optionbuysell)
    globalArray.append(buySellData[0])
    time.sleep(1)
    if selected_optionbuysell is None :
        print('Inside if')
        return html.Div(dcc.RadioItems(
                id = 'optionBuySells',
                options=[{'label': k, 'value': k} for k in stats_mdt.keys()],
            ))
    else:
        print('Inside else')
        return html.Div(dcc.RadioItems(
                id = 'optionBuySells',
                options=[{'label':ki, 'value': ki} for ki in stats_mdt.keys()],
            ))

         
@app.callback(
    Output('SignalClose', 'children'),
    [Input('signal Active', 'value')])
def set_signalClose(selected_signalClose):
    signalActive =[]
    signalActive.append(selected_signalClose)
    print('second')
    globalArray.append('1')
    

@app.callback(
    Output('backTest', 'children'),
    [Input('BackTestLength', 'value')])
def set_backTest(selected_backtest):
    back =[]
    if selected_backtest in initial:
        print('same vlaue not appending')
    else:
       initial.insert(0,selected_backtest)
       back.insert(0,selected_backtest)

       print(globalArray)
      
       globalArray.append(back[0])
      
       if(len(initial)>1): 
        del(globalArray[globalArray.index(initial[1])])
       print('global arry after append:')
       print(globalArray)
       
    
    

@app.callback(
    Output('popwinTesting', 'children'),
    [Input('InsidePopUp', 'value')])
def set_insidepopup(selected_insidepopup):
    insidepopup =[]
    insidepopup.append(selected_insidepopup)
    # print(selected_insidepopup)
    print('fourth')
    # print(globalArray)
    globalArray.append(insidepopup[0])

@app.callback(Output('container', 'children'), [Input('runButton', 'n_clicks')])
def display_tradingLab(n_clicks):
    initial.clear()
    # n = 3
    print('fifth')
    print(globalArray)
    mylist = globalArray
    mylist.reverse()
    print('reverse')
    
    print(mylist)
    newlist = mylist[:4]
    
    newlist.reverse()
    print('sixth')
    print(newlist)
    
    arg = []
    if (newlist[0] is None or newlist[0] =='1'):
        print('inside if')
        newlist.remove(None)
        print(newlist)
        if(newlist[2].isdigit()):
            newlist.append('')
        else:  
            newlist.insert(0,'All')
    else:
        print('Inside else')
        if(len(newlist)==4):
          del newlist[3]
        newlist.append('')


    print('final')
    print(newlist)
    arg = newlist
    del globalArray[:]
    for i in range(n_clicks):
       return  html.Div(id= 'tradingLab',children=[
         html.Label('Trading Lab Statisics:',style={'font-size':'30px'}),
         html.Label(children='{}'.format(get_results(*arg)))
         
        ],style={ 
         'backgroundColor':'#fff'})



if __name__ == '__main__':
    app.run_server(debug=True)

