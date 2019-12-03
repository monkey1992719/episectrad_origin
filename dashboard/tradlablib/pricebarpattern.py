import pandas as pd
import talib
import numpy as np


PriceBarTypes = ['BULLISH','BEARISH']
PriceBarBullishPatterns = ['BULLISH HAMMER','BULLISH BELT HOLD','BULLISH ENGULFING','BULLISH HARAMI','BULLISH HARAMI CROSS','BULLISH INVERTED HAMMER','BULLISH PIERCING LINE','BULLISH DOJI STAR','BULLISH MEETING LINE','BULLISH HOMING PIGEON','BULLISH MATCHING LOW','BULLISH KICKING','BULLISH ONE WHITE SOLDIER','BULLISH MORNING STAR','BULLISH MORNING DOJI STAR','BULLISH ABANDONED BABY','BULLISH TRI STAR','BULLISH DOWNSIDE GAP TWO RABBITS','BULLISH UNIQUE THREE RIVER BOTTOM','BULLISH THREE WHITE SOLDIERS','BULLISH DESCENT BLOCK','BULLISH DELIBERATION BLOCK','BULLISH TWO RABBITS','BULLISH THREE INSIDE UP','BULLISH THREE OUTSIDE UP','BULLISH SQUEEZE ALERT','BULLISH THREE GAP DOWNS','BULLISH BREAKAWAY','BULLISH LADDER BOTTOM','BULLISH AFTER BOTTOM GAP UP','BULLISH STOP LOSS']
PriceBarBearishPatterns = ['BEARISH HANGING MAN','BEARISH BELT HOLD','BEARISH ENGULFING','BEARISH HARAMI','BEARISH HARAMI CROSS','BEARISH SHOOTING STAR','BEARISH DARK CLOUD COVER','BEARISH DOJI STAR','BEARISH MEETING LINE','BEARISH DESCENDING HAWK','BEARISH MATCHING HIGH','BEARISH KICKING','BEARISH ONE BLACK CROW','BEARISH EVENING STAR','BEARISH EVENING DOJI STAR','BEARISH ABANDONED BABY','BEARISH TRI STAR','BEARISH UPSIDE GAP TWO CROWS','BEARISH UNIQUE THREE MOUNTAIN TOP','BEARISH THREE BLACK CROWS','BEARISH ADVANCE BLOCK','BEARISH DELIBERATION BLOCK','BEARISH TWO CROWS','BEARISH THREE INSIDE DOWN','BEARISH THREE OUTSIDE DOWN','BEARISH SQUEEZE ALERT','BEARISH THREE GAP UPS','BEARISH BREAKAWAY','BEARISH LADDER TOP','BEARISH AFTER TOP GAP DOWN','BEARISH STOP LOSS']


######### ???????????????????????????
#open[0] > open[1] and close[0] > open[0] and high[1] > open[0] and close[1] < open[1] and open[1]-close[1]>.02
def recogonewhitesoldier(open, high, close):
    t = np.zeros(len(open))
    for i in range(len(open)-1):
        if (open[i]>close[i] and open[i+1]<close[i+1] and open[i+1]>close[i] and open[i+1]<open[i] and close[i+1]>open[i]):
            t[i+1] = 100
        else:
            t[i+1] = 0
    return t


def recogoneblackcrow(open, high, close):
    t = np.zeros(len(open))
    for i in range(len(open)-1):
        if (open[i]<close[i] and open[i+1]>close[i+1] and open[i+1]<close[i] and open[i+1]>open[i] and close[i+1]<open[i]):        
            t[i+1] = 100
        else:
            t[i+1] = 0
    return t

def recogbullishmeetingline(open, close):
    t = np.zeros(len(open))
    for i in range(len(open)-1):
        if (open[i]>close[i] and open[i+1]<close[i+1] and close[i]==close[i+1]):
            t[i+1] = 100
        else:
            t[i+1] = 0
    return t

def recogbearishmeetingline(open, close):
    t = np.zeros(len(open))
    for i in range(len(open)-1):
        if (open[i]>close[i] and open[i+1]>close[i+1] and close[i]==close[i+1]):
            t[i+1] = 100
        else:
            t[i+1] = 0
    return t

def recogpricebarpattern(alldates, t, value):
    indexes = np.where(t == value)
    dates = np.array(alldates)[indexes]
    indexes = list(indexes[0])
    dates = list(dates)
    return indexes, dates
    

def makepricebarpatterndata(alldates,pricebarpatternalert, t, n):
    ## Search Bullish
    indexes, dates = recogpricebarpattern(alldates, t, 100)
    bullish = {'indexes':indexes, 'dates':dates}
    ## Search Bearish
    indexes, dates = recogpricebarpattern(alldates, t, -100)
    bearish = {'indexes':indexes, 'dates':dates}
    pattern = {'BULLISH':bullish, 'BEARISH':bearish}
    pricebarpatternalert[PriceBarBullishPatterns[n]] = pattern


def makepricebarinvertedpatterndata(alldates,pricebarpatternalert, t, n):
    ## Search Bullish
    indexes, dates = recogpricebarpattern(alldates, t, -100)
    bullish = {'indexes':indexes, 'dates':dates}
    ## Search Bearish
    indexes, dates = recogpricebarpattern(alldates, t, 100)
    bearish = {'indexes':indexes, 'dates':dates}
    pattern = {'BULLISH':bullish, 'BEARISH':bearish}
    pricebarpatternalert[PriceBarBullishPatterns[n]] = pattern


def patternanal(ohlcdata):
    # either start with numpy.ndarray, or convert to it like this
    # (making sure to specify the ``dtype`` (or "data type") is
    # 64-bit floating point which is what ``talib`` expects):
    open = np.array(ohlcdata.Open, dtype=float)
    high = np.array(ohlcdata.High, dtype=float)
    low = np.array(ohlcdata.Low, dtype=float)
    close = np.array(ohlcdata.Close, dtype=float)

    pricebarpatternalert = dict()


    ################################# Hammer pattern #################################
    t = talib.CDLHAMMER(open, high, low, close)
    ## Search Bullish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bullish = {'indexes':indexes, 'dates':dates}

    t = talib.CDLHANGINGMAN(open, high, low, close)
    ## Search Bearish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bearish = {'indexes':indexes, 'dates':dates}

    pattern = {'BULLISH':bullish, 'BEARISH':bearish}
    pricebarpatternalert[PriceBarBullishPatterns[0]] = pattern

    ################################# Belt hold pattern #################################
    t = talib.CDLBELTHOLD(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 1)

    ################################# Engulfing pattern #################################
    t = talib.CDLENGULFING(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 2)

    ################################# HARAMI pattern #################################
    t = talib.CDLHARAMI(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 3)

    ################################# HARAMICROSS pattern #################################
    t = talib.CDLHARAMICROSS(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 4)

    ################################# INVERTEDHAMMER pattern #################################
    t = talib.CDLINVERTEDHAMMER(open, high, low, close)
    ## Search Bullish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bullish = {'indexes':indexes, 'dates':dates}

    t = talib.CDLSHOOTINGSTAR(open, high, low, close)
    ## Search Bearish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bearish = {'indexes':indexes, 'dates':dates}

    pattern = {'BULLISH':bullish, 'BEARISH':bearish}
    pricebarpatternalert[PriceBarBullishPatterns[5]] = pattern

    ################################# PIERCING  pattern #################################
    t = talib.CDLPIERCING(open, high, low, close)
    ## Search Bullish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bullish = {'indexes':indexes, 'dates':dates}

    t = talib.CDLDARKCLOUDCOVER(open, high, low, close)
    ## Search Bearish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bearish = {'indexes':indexes, 'dates':dates}

    pattern = {'BULLISH':bullish, 'BEARISH':bearish}
    pricebarpatternalert[PriceBarBullishPatterns[6]] = pattern

    #makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 6)

    ################################# DOJISTAR pattern #################################
    t = talib.CDLHARAMICROSS(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 7)

    ################################# Meeting line pattern #################################
    t = talib.CDLHARAMICROSS(open, high, low, close)########????########
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 8)

    ################################# HOMINGPIGEON pattern #################################
    t = talib.CDLHOMINGPIGEON(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 9)

    ################################# MATCHINGLOW pattern #################################
    t = talib.CDLMATCHINGLOW(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 10)

    ################################# KICKING pattern #################################
    t = talib.CDLKICKING(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 11)

    ################################# WHITESOLDIERS pattern #################################????????????
    ####oneWhiteSoldier() => open[0] > open[1] and close[0] > open[0] and high[1] > open[0] and close[1] < open[1] and open[1]-close[1]>.02
    
    t = recogonewhitesoldier(open, high, close)
    ## Search Bullish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bullish = {'indexes':indexes, 'dates':dates}
    
    t = recogoneblackcrow(open, high, close)
    ## Search Bearish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bearish = {'indexes':indexes, 'dates':dates}

    pattern = {'BULLISH':bullish, 'BEARISH':bearish}
    pricebarpatternalert[PriceBarBullishPatterns[12]] = pattern

    ################################# MORNINGSTAR pattern #################################
    t = talib.CDLMORNINGSTAR(open, high, low, close)
    ## Search Bullish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bullish = {'indexes':indexes, 'dates':dates}

    t = talib.CDLEVENINGSTAR(open, high, low, close)
    ## Search Bearish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bearish = {'indexes':indexes, 'dates':dates}

    pattern = {'BULLISH':bullish, 'BEARISH':bearish}
    pricebarpatternalert[PriceBarBullishPatterns[13]] = pattern

    ################################# MORNINGDOJISTAR pattern #################################
    t = talib.CDLMORNINGDOJISTAR(open, high, low, close)
    ## Search Bullish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bullish = {'indexes':indexes, 'dates':dates}

    t = talib.CDLEVENINGDOJISTAR(open, high, low, close)
    ## Search Bearish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bearish = {'indexes':indexes, 'dates':dates}

    pattern = {'BULLISH':bullish, 'BEARISH':bearish}
    pricebarpatternalert[PriceBarBullishPatterns[14]] = pattern

    ################################# ABANDONEDBABY  pattern #################################
    t = talib.CDLABANDONEDBABY (open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 15)

    ################################# TRISTAR pattern #################################
    t = talib.CDLTRISTAR(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 16)

    ################################# downside gap two rabbits pattern #################################
    t = talib.CDL2CROWS(open, high, low, close)
    ## Search Bullish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bullish = {'indexes':indexes, 'dates':dates}

    t = talib.CDLUPSIDEGAP2CROWS(open, high, low, close)
    ## Search Bearish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bearish = {'indexes':indexes, 'dates':dates}

    pattern = {'BULLISH':bullish, 'BEARISH':bearish}
    pricebarpatternalert[PriceBarBullishPatterns[17]] = pattern

    ################################# UNIQUE3RIVER pattern #################################
    t = talib.CDLUNIQUE3RIVER(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 18)

    ################################# 3WHITESOLDIERS pattern #################################
    t = talib.CDL3WHITESOLDIERS(open, high, low, close)
    ## Search Bullish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bullish = {'indexes':indexes, 'dates':dates}

    t = talib.CDL3BLACKCROWS(open, high, low, close)
    ## Search Bearish
    indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    bearish = {'indexes':indexes, 'dates':dates}

    pattern = {'BULLISH':bullish, 'BEARISH':bearish}
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 19)

    ################################# DESCENT BLOCK pattern #################################
    t = talib.CDLADVANCEBLOCK(open, high, low, close)
    makepricebarinvertedpatterndata(ohlcdata.Date,pricebarpatternalert, t, 20)########################????????????

    ################################# deliberation block pattern #################################
    t = talib.CDL3INSIDE(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 21)###############???????????????

    ################################# 2Rabbits pattern #################################
    t = talib.CDL2CROWS(open, high, low, close)
    makepricebarinvertedpatterndata(ohlcdata.Date,pricebarpatternalert, t, 22)##############??????????????

    ################################# 3INSIDE pattern #################################
    t = talib.CDL3INSIDE(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 23)

    ################################# 3OUTSIDE pattern #################################
    t = talib.CDL3OUTSIDE(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 24)

    ################################# squeeze alert pattern #################################
    t = talib.CDLHARAMICROSS(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 25)##############??????????

    ################################# three gap down pattern #################################
    t = talib.CDLXSIDEGAP3METHODS(open, high, low, close)
    makepricebarinvertedpatterndata(ohlcdata.Date,pricebarpatternalert, t, 26)############?????????

    ################################# BREAKAWAY pattern #################################
    t = talib.CDLBREAKAWAY(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 27)

    ################################# CDLLADDERBOTTOM pattern #################################
    t = talib.CDLLADDERBOTTOM(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 28)

    ################################# after bottom gap up pattern #################################
    t = talib.CDLGAPSIDESIDEWHITE(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 29)

    ################################# stop loss pattern #################################
    t = talib.CDLHARAMICROSS(open, high, low, close)
    makepricebarpatterndata(ohlcdata.Date,pricebarpatternalert, t, 30) ############????????????????????????????????????????

    return pricebarpatternalert

    


def patternrecog(ohlcdata, patternname):
    # either start with numpy.ndarray, or convert to it like this
    # (making sure to specify the ``dtype`` (or "data type") is
    # 64-bit floating point which is what ``talib`` expects):
    open = np.array(ohlcdata.Open, dtype=float)
    high = np.array(ohlcdata.High, dtype=float)
    low = np.array(ohlcdata.Low, dtype=float)
    close = np.array(ohlcdata.Close, dtype=float)

    indexes = []
    dates = []

    if patternname == 'BULLISH HAMMER':

        ################################# Hammer pattern #################################
        t = talib.CDLHAMMER(open, high, low, close)
        ## Search Bullish
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BEARISH HANGING MAN':
    
        t = talib.CDLHANGINGMAN(open, high, low, close)
        ## Search Bearish
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BULLISH BELT HOLD':

        ################################# Belt hold pattern #################################

        t = talib.CDLBELTHOLD(open, high, low, close)
        ## Search Bearish
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BEARISH BELT HOLD':    

        t = talib.CDLBELTHOLD(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH ENGULFING':    
        t = talib.CDLENGULFING(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BEARISH ENGULFING':    
        t = talib.CDLENGULFING(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH HARAMI':    
        ################################# HARAMI pattern #################################
        t = talib.CDLHARAMI(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH HARAMI':    
        ################################# HARAMI pattern #################################
        t = talib.CDLHARAMI(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH HARAMI CROSS':    
        ################################# HARAMICROSS pattern #################################
        t = talib.CDLHARAMICROSS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH HARAMI CROSS':    
        ################################# HARAMICROSS pattern #################################
        t = talib.CDLHARAMICROSS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH INVERTED HAMMER':    
        ################################# INVERTEDHAMMER pattern #################################
        t = talib.CDLINVERTEDHAMMER(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH SHOOTING STAR':    
        t = talib.CDLSHOOTINGSTAR(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BULLISH PIERCING LINE':    
        ################################# PIERCING  pattern #################################
        t = talib.CDLPIERCING(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH DARK CLOUD COVER':    
        t = talib.CDLDARKCLOUDCOVER(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BULLISH DOJI STAR':    
        ################################# DOJI STAR  pattern #################################
        t = talib.CDLDOJISTAR(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH DOJI STAR':    
        t = talib.CDLDOJISTAR(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH MEETING LINE':    
        ################################# MEETING LINE  pattern #################################
        t = recogbullishmeetingline(open, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH MEETING LINE':    
        t = recogbearishmeetingline(open, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BULLISH HOMING PIGEON':    
        ################################# HOMING PIGEON  pattern #################################
        t = talib.CDLHOMINGPIGEON(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH DESCENDING HAWK':    
        t = talib.CDLHOMINGPIGEON(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH MATCHING LOW':    
        ################################# MATCHING LOW  pattern #################################
        t = talib.CDLMATCHINGLOW(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH MATCHING HIGH':    
        t = talib.CDLMATCHINGLOW(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH KICKING':    
        ################################# KICKING   pattern #################################
        t = talib.CDLKICKING(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH KICKING':    
        t = talib.CDLKICKING(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)


    elif patternname == 'BULLISH ONE WHITE SOLDIER':    
        ################################# WHITESOLDIERS pattern #################################????????????
        t = recogonewhitesoldier(open, high, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH ONE BLACK CROW':    
        t = recogoneblackcrow(open, high, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BULLISH MORNING STAR':    
        ################################# MORNING STAR pattern #################################????????????
        t = talib.CDLMORNINGSTAR(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH EVENING STAR':    
        t = talib.CDLEVENINGSTAR(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BULLISH MORNING DOJI STAR':    
        ################################# MORNING DOJI STAR pattern #################################????????????
        t = talib.CDLMORNINGDOJISTAR(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH EVENING DOJI STAR':    
        t = talib.CDLEVENINGDOJISTAR(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BULLISH ABANDONED BABY':    
        ################################# ABANDONEDBABY pattern #################################????????????
        t = talib.CDLABANDONEDBABY (open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH ABANDONED BABY':    
        t = talib.CDLABANDONEDBABY (open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH TRI STAR':    
        ################################# TRI STAR pattern #################################????????????
        t = talib.CDLTRISTAR(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH TRI STAR':    
        t = talib.CDLTRISTAR(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH DOWNSIDE GAP TWO RABBITS':    
        t = talib.CDLUPSIDEGAP2CROWS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)
    elif patternname == 'BEARISH UPSIDE GAP TWO CROWS':    
        t = talib.CDLUPSIDEGAP2CROWS(open, high, low, close)        
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BULLISH UNIQUE THREE RIVER BOTTOM':    
        t = talib.CDLUNIQUE3RIVER(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH UNIQUE THREE MOUNTAIN TOP':    
        t = talib.CDLUNIQUE3RIVER(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH THREE WHITE SOLDIERS':    
        t = talib.CDL3WHITESOLDIERS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH THREE BLACK CROWS':    
        t = talib.CDL3BLACKCROWS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BULLISH DESCENT BLOCK':    
        t = talib.CDLADVANCEBLOCK(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)
    elif patternname == 'BEARISH ADVANCE BLOCK':    
        t = talib.CDLADVANCEBLOCK(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)

    elif patternname == 'BULLISH DELIBERATION BLOCK':    
        t = talib.CDL3INSIDE(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH DELIBERATION BLOCK':    
        t = talib.CDL3INSIDE(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)


    elif patternname == 'BULLISH TWO RABBITS':    
        t = talib.CDL2CROWS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)
    elif patternname == 'BEARISH TWO CROWS':    
        t = talib.CDL2CROWS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)


    elif patternname == 'BULLISH THREE INSIDE UP':    
        t = talib.CDL3INSIDE(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BULLISH THREE INSIDE DOWN':    
        t = talib.CDL3INSIDE(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH THREE OUTSIDE UP':    
        t = talib.CDL3OUTSIDE(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BULLISH THREE OUTSIDE DOWN':    
        t = talib.CDL3OUTSIDE(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH SQUEEZE ALERT':    
        t = talib.CDLHARAMICROSS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH SQUEEZE ALERT':    
        t = talib.CDLHARAMICROSS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH THREE GAP DOWNS':    
        t = talib.CDLXSIDEGAP3METHODS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH THREE GAP UPS':    
        t = talib.CDLXSIDEGAP3METHODS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)


    elif patternname == 'BULLISH BREAKAWAY':    
        t = talib.CDLBREAKAWAY(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH BREAKAWAY':    
        t = talib.CDLBREAKAWAY(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH LADDER BOTTOM':    
        t = talib.CDLLADDERBOTTOM(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH LADDER TOP':    
        t = talib.CDLLADDERBOTTOM(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH AFTER BOTTOM GAP UP':    
        t = talib.CDLGAPSIDESIDEWHITE(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BULLISH AFTER BOTTOM GAP DOWN':    
        t = talib.CDLGAPSIDESIDEWHITE(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    elif patternname == 'BULLISH STOP LOSS':    
        t = talib.CDLHARAMICROSS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, 100)
    elif patternname == 'BEARISH STOP LOSS':    
        t = talib.CDLHARAMICROSS(open, high, low, close)
        indexes, dates = recogpricebarpattern(ohlcdata.Date, t, -100)

    return {'indexes':indexes, 'dates':dates}