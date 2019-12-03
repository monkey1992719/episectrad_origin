from . import technicalindicator as tind
import pandas as pd
from dashboard import models


#add a first indicator
def get_trade_firstindicator_plotresult(df, tii):

    graphdata = tind.display_indicator(df, tii.indicator.name, tii)

    graph = {'id': tii.indicator.id_letter, 'name': tii.indicator.name, 'data': graphdata, 'tii_id': tii.id}

    return graph

#add an indicator to a existing trade
def get_trade_indicator_plotresult(dforg, tradei, ntii):

    df = dforg.copy()

    prevtii = None
    for tii in tradei.tradeindicatorindicator_set.all():
        if tii == ntii:
            continue
            
        prevtii = tii
        graphdata = tind.display_indicator(df, tii.indicator.name, tii)

        for pltdt in graphdata:
            df[pltdt['name']] = pltdt['y']

    if prevtii is not None:
        # create input_value
        cp = prevtii.indicator.chartplot_set.all().first()
        ii = ntii.indicator.indicatorinputs.get(parameter='close_col')
        if ii is not None:
            newiv = models.IndicatorInputValue(trade_indicator_indicator=ntii, indicator_input=ii, value=cp.plotname)
            newiv.save()

    return get_trade_firstindicator_plotresult(df, ntii)

# draw a trade    
def get_trade_plotresult(dforg, tradei):

    df = dforg.copy()

    graphs = []
    for tii in tradei.tradeindicatorindicator_set.all():
        graphdata = tind.display_indicator(df, tii.indicator.name, tii)

        for pltdt in graphdata:
            df[pltdt['name']] = pltdt['y']

        graph = {'id': tii.indicator.id_letter, 'name': tii.indicator.name, 'data': graphdata, 'tii_id': tii.id}

        graphs.append(graph)

    return {'tradeid': tradei.pk, 'indicators': graphs, 'with_main': tradei.with_main}


# draw trades
def get_trades_plotresult(dforg, tradeis):

    trades = []
    for ti in tradeis:
        trades.append(get_trade_plotresult(dforg, ti))

    return trades


# make all traditional trade choice 

def get_trade_traditional_choices(trade):
    
    return trade.tradeindicatorindicator_set.filter(indicator__value_indicator=0)


# make all trade plots choice 

def get_trade_plot_choices(trade):
    
    tiis = trade.tradeindicatorindicator_set.all()
    cps = []
    for tii in tiis:
        cps.extend(tii.indicator.chartplot_set.all())
    
    return cps


# make all trade choice and load trade setting choice
def get_trade_all_choices(trade):

    tiis = get_trade_traditional_choices(trade)

    #threshold choices
    thresholds = []
    cps = get_trade_plot_choices(trade)
    for cp in cps:
        threshold_b = 0
        threshold_s = 0
        tii = trade.tradeindicatorindicator_set.filter(indicator=cp.indicator).first()
        tipt = tii.tradeindicatorplotthreshold_set.filter(plot=cp).first()
        check = 0
        if tipt is not None:
            threshold_b = tipt.threshold_b
            threshold_s = tipt.threshold_s
            check=1
        thresholds.append({'cp_id': cp.id, 'tii_id': tii.pk, 'plotname': cp.plotname, 'threshold_b': threshold_b, 'threshold_s': threshold_s, 'check': check})

    # plot 2 plot
    cross2 = []
    i = 0
    while i < len(cps):
        cp1 = cps[i]
        tii1 = trade.tradeindicatorindicator_set.filter(indicator=cp1.indicator).first()
        j = i + 1
        while j < len(cps):
            cp2 = cps[j]
            tii2 = trade.tradeindicatorindicator_set.filter(indicator=cp2.indicator).first()
            tic2 = models.TradeIndicatorCross2.objects.filter(trade_indicator_indicator1=tii1, chart_plot1=cp1, trade_indicator_indicator2=tii2, chart_plot2=cp2).first()
            state='no'
            if tic2 is not None:
                state='yes'
            cross2.append({'tii1': tii1, 'cp1': cp1, 'tii2': tii2, 'cp2': cp2, 'state': state})
            j = j + 1
        i = i + 1

    # plot 2 vplot
    crossv = []
    for cp in cps:
        tii = trade.tradeindicatorindicator_set.filter(indicator=cp.indicator).first()
        state='no'
        ticv = models.TradeIndicatorCrossv.objects.filter(trade_indicator_indicator=tii, chart_plot=cp).first()
        if ticv is not None:
            state='yes'
        crossv.append({'tii': tii, 'cp': cp, 'state': state})

    allchoice = {'traditional':tiis, 'thresholds':thresholds, 'cross2':cross2, 'crossv':crossv}
    return allchoice


# save indicator trade options
def save_trade_indicator_options(options):

    # traditional tii save
    for t in options['traditional']:
        tii = models.TradeIndicatorIndicator.objects.filter(pk=t).first()
        tii.traditional = 1
        tii.save()

    # not traditional tii save
    for t in options['ntraditional']:
        tii = models.TradeIndicatorIndicator.objects.filter(pk=t).first()
        tii.traditional = 0
        tii.save()

    # threshold save
    for t in options['threshold']:
        tii = models.TradeIndicatorIndicator.objects.filter(pk=t['tii_id']).first()
        cp = models.ChartPlot.objects.filter(pk=t['cp_id']).first()
        th = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator = tii, plot = cp).first()
        if th is None:
            th = models.TradeIndicatorPlotThreshold(trade_indicator_indicator = tii, plot = cp)
        th.threshold_b = float(t['value_b'])
        th.threshold_s = float(t['value_s'])
        th.save()

    # not threshold delete
    for t in options['nthreshold']:
        tii = models.TradeIndicatorIndicator.objects.filter(pk=t['tii_id']).first()
        cp = models.ChartPlot.objects.filter(pk=t['cp_id']).first()
        th = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator = tii, plot = cp)
        if th.exists():
            th.delete()

    # cross2 save
    for c in options['cross2']:
        tii1 = models.TradeIndicatorIndicator.objects.filter(pk=c['tii1id']).first()
        cp1 = models.ChartPlot.objects.filter(pk=c['cp1id']).first()
        tii2 = models.TradeIndicatorIndicator.objects.filter(pk=c['tii2id']).first()
        cp2 = models.ChartPlot.objects.filter(pk=c['cp2id']).first()
        cr2 = models.TradeIndicatorCross2.objects.filter(trade_indicator_indicator1 = tii1, chart_plot1 = cp1, trade_indicator_indicator2 = tii2, chart_plot2 = cp2).first()
        if cr2 is None:
            cr2 = models.TradeIndicatorCross2.objects.create(trade_indicator_indicator1 = tii1, chart_plot1 = cp1, trade_indicator_indicator2 = tii2, chart_plot2 = cp2)
        

    # not cross2 delete
    for c in options['ncross2']:
        tii1 = models.TradeIndicatorIndicator.objects.filter(pk=c['tii1id']).first()
        cp1 = models.ChartPlot.objects.filter(pk=c['cp1id']).first()
        tii2 = models.TradeIndicatorIndicator.objects.filter(pk=c['tii2id']).first()
        cp2 = models.ChartPlot.objects.filter(pk=c['cp2id']).first()
        cr2 = models.TradeIndicatorCross2.objects.filter(trade_indicator_indicator1 = tii1, chart_plot1 = cp1, trade_indicator_indicator2 = tii2, chart_plot2 = cp2)
        if cr2.exists():
            cr2.delete()

    # crossv save
    for c in options['crossv']:
        tii = models.TradeIndicatorIndicator.objects.filter(pk=c['tiiid']).first()
        cp = models.ChartPlot.objects.filter(pk=c['cpid']).first()
        crv = models.TradeIndicatorCrossv.objects.filter(trade_indicator_indicator = tii, chart_plot = cp).first()
        if crv is None:
            crv = models.TradeIndicatorCrossv.objects.create(trade_indicator_indicator = tii, chart_plot = cp)
        

    # not crossv delete
    for c in options['ncrossv']:
        tii = models.TradeIndicatorIndicator.objects.filter(pk=c['tiiid']).first()
        cp = models.ChartPlot.objects.filter(pk=c['cpid']).first()
        crv = models.TradeIndicatorCrossv.objects.filter(trade_indicator_indicator = tii, chart_plot = cp)
        if crv.exists():
            crv.delete()