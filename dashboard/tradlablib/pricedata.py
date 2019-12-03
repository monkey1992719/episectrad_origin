import pandas as pd
import requests
from datetime import datetime, timedelta
import time
from pandas_datareader import data
from episectrad import settings


INTRADAY_TIMESERIES_INTERVAL = ['1min', '3min', '5min', '15min', '30min', '60min', '240min']
HISTORICAL_TIMESERIES_PERIODS = ['1m', '6m', '12m', '24m', '36m']
PREIOD_DAYS = {
    '1w' : 7,
    '1m' : 30,
    '6m' : 180,
    '12m' : 360,
    '24m' : 720,
    '36m' : 1095
}

CHANGE_UNIT = {
    'GOLD' : 100.0                    #once to 100once
}

#get intraday data
def alphavantageRequest(symbol, interval):

    # api-endpoint 
    URL = "https://www.alphavantage.co/query"

    # my alphavantage api key
    apikey = 'S9NTOECM3PL6PAZ8'

    bIntraday = True

    if bIntraday:      # if intraday
        function = 'TIME_SERIES_INTRADAY'

        # defining a params dict for the parameters to be sent to the API 
        sinterval = interval

        if interval == '3min':
            sinterval = '1min'
        elif interval == '240min':
            sinterval = '60min'

        PARAMS = {'function' : function, 'symbol' : symbol, 'outputsize' : 'full', 'apikey' : apikey, 'interval' : sinterval} 
    else:
        function = 'TIME_SERIES_DAILY'

        # defining a params dict for the parameters to be sent to the API 
        PARAMS = {'function' : function, 'symbol' : symbol, 'outputsize' : 'full', 'apikey' : apikey} 

        
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS) 
    
    # extracting data in json format 
    data = r.json()

    if bIntraday:
        keystr = 'Time Series (' + sinterval + ')'
    else:
        keystr = 'Time Series (Daily)'

    prices = data.get(keystr)

    # if bIntraday:
    #     # sort by date

    #     newprices = dict()
    #     datekeys = list(prices.keys())
    #     datekeys.sort()
        
    #     days = PREIOD_DAYS.get(period, 1095)
    #     past = datetime.now() - timedelta(days=days)

    #     for k in datekeys:
    #         curdate = datetime.strptime(k, '%Y-%m-%d')
    #         if bIntraday or curdate >= past:
    #             newprices[k] = prices[k]

    #     prices = newprices
    
    newprices = dict()
    index = 0

    mul = CHANGE_UNIT.get(symbol, 1.0)

    replacekey = {'1. open' : 'Open', '2. high' : 'High', '3. low' : 'Low', '4. close' : 'Close', '5. volume' : 'Volume'}
    for k in list(prices.keys()):
        v = prices[k]
        item = dict()
        item['Date'] = k
        for k1, v1 in v.items():
            item[replacekey[k1]] = float(v1) * mul
            
        newprices[index] = item
        index = index + 1

    prices = newprices

    prices = pd.DataFrame.from_dict(prices, orient = 'index', columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    prices = prices.sort_values(by=['Date'])


    if interval == '3min' or interval == '240min':
        pastdatetimestr = "1970-02-07 00:00:00"

        newprices = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

        seconds = 180
        if interval == '240min':
            seconds = 60 * 240

        i = 0
        for index, row in prices.iterrows():
            pastdate = datetime.strptime(pastdatetimestr, '%Y-%m-%d %H:%M:%S').date()
            curdate = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S').date()

            if curdate != pastdate:
                newprices.loc[i] = row
                i = i + 1
                pastdatetimestr = row['Date']
            else:
                pasttime = datetime.strptime(pastdatetimestr, '%Y-%m-%d %H:%M:%S')
                curtime = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')

                if curtime - pasttime == timedelta(seconds=seconds):
                    newprices.loc[i] = row
                    i = i + 1
                    pastdatetimestr = row['Date']

        prices = newprices
    
    return prices

def otherRequest(site, ticker, period):
    now = datetime.now()
    days = PREIOD_DAYS.get(period, 1095)
    past = now - timedelta(days=days)

    panel_data = data.DataReader(ticker, site, past, now)

    dates = []
    for v in list(panel_data.High.keys()):
        dates.append(v.strftime("%Y-%m-%d"))

    mul = CHANGE_UNIT.get(ticker, 1.0)

    prices = pd.DataFrame({'Date' : dates,
                            'Open' : [float(i) * mul for i in list(panel_data.Open)],
                            'High' : [float(i) * mul for i in list(panel_data.High)],
                            'Low' : [float(i) * mul for i in list(panel_data.Low)],
                            'Close' : [float(i) * mul for i in list(panel_data.Close)],
                            'Volume' : list(panel_data.Volume)})
    
    prices = prices.sort_values(by=['Date'])

    return prices


#get symbol tickers
def symbolSearch(keyword):

    # api-endpoint 
    URL = "https://www.alphavantage.co/query"

    # my alphavantage api key
    apikey = 'S9NTOECM3PL6PAZ8'

    PARAMS = {'function' : 'SYMBOL_SEARCH', 'keywords' : keyword, 'apikey' : apikey} 
        
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS) 
    
    # extracting data in json format 
    data = r.json()

    return data["bestMatches"]


def importLiveData(dashboard):

    symbol = dashboard.symbol
    bIntraday = int(dashboard.bIntraday)
    period = dashboard.period
    interval = dashboard.interval
        
    try:
        if bIntraday:
            df = alphavantageRequest(symbol, interval)
        else:
            df = otherRequest("yahoo", symbol, period)
        df = df.dropna()
        df.to_csv(path_or_buf=settings.MEDIA_ROOT + '/labdata/OHLC' + str(dashboard.id) + '.csv', index=False)
    except ValueError:
        return None

    return df