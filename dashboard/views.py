from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import translation
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import BaseDeleteView, FormView
from django.utils.decorators import method_decorator
from django.db import transaction, connection
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django import forms as baseforms
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import json
from .tradlablib import chartpattern as cp
from .tradlablib import pricebarpattern as pp
from .tradlablib import technicalindicator as tind
from .tradlablib import pricedata as prd
from .tradlablib.indicatorparameter import *
from .tradlablib.plotsetting import *
from .tradlablib import tradelib
from . import forms, models, tasks
import structlog
import configparser
from episectrad import settings
from .tradlablib import backtest as bt

from .tradlablib.libind.indicators import *

MAX_TRADE_COUNT = 4


logger = structlog.get_logger()

def switch_language(request, language):
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language
    return redirect('/admin')


class LoginView(FormView):
    template_name = "dashboard/admin/login.html"
    form_class = forms.AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url = "/"

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        logger.bind(email=user.email).info("User had logged in")
        return super().form_valid(form)


class LogoutView(View):
    def post(self, request):
        if request.user.is_authenticated:
            logger.bind(email=request.user.email).info("User had logged out")
        logout(request)
        return redirect("index")


class SignupView(FormView):
    template_name = "dashboard/admin/signup.html"
    form_class = forms.UserCreationForm
    success_url = "/signup/email-sent"
    # success_url = "/signup/email-sent"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email_confirmed = False
        user.save()
        logger.bind(email=user.email).info("User had signed up (email confirmation pending)")
        request_context = {
            "domain": self.request.META["HTTP_HOST"],
            "protocol": "https" if self.request.is_secure() else "http",
        }

        # tasks.add.apply_async(2,2)
        
        # print(get_celery_worker_status())
        # r = tasks.send_signup_email.delay(1,2)
        # print(x.task_id)

        # r = tasks.send_signup_email.apply_async(kwargs={"user_pk": user.pk,
        #                                             "extra_email_context": request_context},
        #                                     countdown=30)
        # print("asdf"+r.state)

        # tasks.send_signup_email(user_pk= user.pk, extra_email_context=request_context)

        return super().form_valid(form)


class SignupEmailSentView(TemplateView):
    template_name = "dashboard/admin/signup_email_sent.html"


class SignupConfirmView(TemplateView):
    template_name = "dashboard/signup_bad_link.html"
    token_generator = default_token_generator
    success_url = "/dashboard/"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        assert "uidb64" in kwargs and "token" in kwargs

        user = self.get_user(kwargs["uidb64"])
        if user is not None and not user.email_confirmed:
            log = logger.bind(user=user, email=user.email)
            token = kwargs["token"]
            if self.token_generator.check_token(user, token):
                log.info("User had confirmed their email address")
                user.email_confirmed = True
                user.save(update_fields=["email_confirmed"])
                if not self.request.user.is_authenticated():
                    login(self.request, user)
                request_context = {
                    "domain": self.request.META["HTTP_HOST"],
                    "protocol": "https" if self.request.is_secure() else "http",
                }
                tasks.send_signup_confirmed_email.apply_async(kwargs={"user_pk": user.pk,
                                                                      "extra_email_context": request_context})
                return redirect(self.success_url)
            else:
                log.warn("User had visited invalid or expired link")
        elif user is not None:
            logger.bind(user=user, email=user.email).info("Email address is already confirmed")
        else:
            logger.warn("Bad signup link - user not found")

        # Display the "Invalid or expired link" page.
        return self.render_to_response(self.get_context_data(user=user))

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring on Python 3
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = models.User.objects.select_for_update().get(pk=uid)
        except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
            user = None
        return user


symbol = 'AAPL'
period = '36m'
interval = '5min'
bIntraday = 0
df = pd.DataFrame()

pricebarpatternalert = dict()

class tradlab:

    def dashtradlab(request, dashboard_id=0):
        assert isinstance(request, HttpRequest)

        # config = configparser.ConfigParser()
        # ini = config.read('dashboard/tradlablib/params.2.ini')
        # for ind in config.sections():
        #     print(ind)
        #     i = models.Indicator.objects.get(param_name=ind)
        #     for option in config[ind]:
        #         if option == 'close_col':
        #             ii1 = models.IndicatorInput.objects.get(parameter=option)
        #             i.indicatorinputs.add(ii1)
                    
        #     i.save()

        if request.user.is_authenticated:
            dashboard = models.Dashboard.objects.filter(user=request.user)

        if dashboard_id == 0:
            dashboard = models.Dashboard.objects.all().first()
        else:
            dashboard = models.Dashboard.objects.get(id=dashboard_id)

        if dashboard is None:
            # dashboard = models.Dashboard(user=request.user)
            dashboard = models.Dashboard()
            dashboard.save()

            df = prd.importLiveData(dashboard)

            if df is None:
                return HttpResponse('Data Importing Failed!')
        else:
            df = pd.read_csv(settings.MEDIA_ROOT+'/labdata/OHLC'+str(dashboard.id)+'.csv', sep=',')
            df = pd.DataFrame(df)

        # getting all dashboards
        # dashboards = models.Dashboard.objects.filter(user=request.user)
        dashboards = models.Dashboard.objects.all()

        symbol = dashboard.symbol
        period = dashboard.period
        interval = dashboard.interval
        bIntraday = dashboard.bIntraday

        pricebarpatternalert = pp.patternanal(df)

        # trade ready

        # TradeSettingIndicator.objects.get(user=request.user)
        tradeis = models.TradeIndicator.objects.filter(backtest__dashboard__id = dashboard.id)

        trades = tradelib.get_trades_plotresult(df, tradeis)
            
        # options ready
        chartpatterns = []
        for i in range(len(cp.bullishpatternnames)):
            chartpatterns.append({'bullish':cp.bullishpatternnames[i], 'bearish':cp.bearishpatternnames[i]})

        barpatterns = []
        for i in range(len(pp.PriceBarBullishPatterns)):
            barpatterns.append({'bullish':pp.PriceBarBullishPatterns[i], 'bearish':pp.PriceBarBearishPatterns[i]})

        now = datetime.now()
        nowdatestr = now.strftime("%d/%m/%y")

        backtest_choices = []

        for m in prd.HISTORICAL_TIMESERIES_PERIODS:
            days = prd.PREIOD_DAYS.get(m)
            past = now - timedelta(days=days)
            pastdatestr = past.strftime("%d/%m/%y")
            backtest_choices.append({'period':m, 'start':pastdatestr, 'end':nowdatestr})

        all_indicators = {}
        with connection.cursor() as cursor:
            cursor.execute("select category from indicators group by category")
            rows = cursor.fetchall()
            for row in rows:
                indids = []
                for i in models.Indicator.objects.filter(category=row[0]):
                    indids.append([i.name, i.id_letter, i.possible_combine])
                all_indicators[row[0]] = indids

        # plot setting ready

        # if request.user.is_authenticated:
            # userplotmodel = models.ChartPlotSetting.objects.get(user=request.user, string=strmodel)

        plot_settings = get_tis_plot_settings(tradeis)
        
        return render(
            request,
            'dashboard/dashboard/tradelaboratory.html',
            context={
                'ChartPatterns': chartpatterns,
                'BarPatterns': barpatterns,
                'Prices' : df.to_json(orient='records'),
                'Indicators' : all_indicators,
                'Intervals' : prd.INTRADAY_TIMESERIES_INTERVAL,
                'Periods' : backtest_choices,
                'Interval' : interval,
                'Period' : period,
                'bIntraday' : bIntraday,
                'Symbol' : symbol,
                'Backtests' : dashboard.backtest_set.all(),
                'TradingIndicatorResults' : trades,
                'PlotSettings': plot_settings,
                'EnterSignal': dashboard.enter_signal,
                'Dashboard_ID': dashboard.id,
                'Dashboards': dashboards,
            }
        )


    def recogpricebarpattern(request):
        assert isinstance(request, HttpRequest)

        patternname = request.GET.get('patternname', 'BULLISH HAMMER')
        dashboard_id = request.GET.get('dashboard_id', 0)

        df = pd.read_csv(settings.MEDIA_ROOT+'/labdata/OHLC'+str(dashboard_id)+'.csv', sep=',')
        df = pd.DataFrame(df)
        data = pp.patternrecog(df, patternname)
        highs = list(np.array(df.High)[data['indexes']])
        lows = list(np.array(df.Low)[data['indexes']])
        result = {'dates':data['dates'], 'indexes':str(data['indexes']), 'lows':lows, 'highs':highs}

        response = JsonResponse(result, safe=True)
        return response

    def addpricebarpattern(request):
        assert isinstance(request, HttpRequest)

        patternname = request.GET.get('patternname', 'BULLISH HAMMER')
        dashboard_id = request.GET.get('dashboard_id', 0)

        backtest = models.Backtest()
        backtest.dashboard = models.Dashboard.objects.get(id=dashboard_id)
        backtest.mode = 1
        backtest.pricebar_pattern = patternname
        backtest.save()

        return HttpResponse("success")


    def recogchartpattern(request):
        assert isinstance(request, HttpRequest)

        patternname = request.GET.get('patternname', 'Ascending Triangle')
        dashboard_id = request.GET.get('dashboard_id', 0)
        df = pd.read_csv(settings.MEDIA_ROOT+'/labdata/OHLC'+str(dashboard_id)+'.csv', sep=',')
        df = pd.DataFrame(df)
        result = cp.recogchartpattern(df, patternname)
        response = JsonResponse(result, safe=True)
        return response

    
    def addchartpattern(request):
        assert isinstance(request, HttpRequest)

        patternname = request.GET.get('patternname', 'Ascending Triangle')
        dashboard_id = request.GET.get('dashboard_id', 0)
        backtest = models.Backtest()
        backtest.dashboard = models.Dashboard.objects.get(id=dashboard_id)
        backtest.mode = 2
        backtest.chart_pattern = patternname
        backtest.save() 
        return HttpResponse("success")


    def symbolperiodchange(request):
        assert isinstance(request, HttpRequest)

        dashboard_id = request.GET.get('dashboard_id', 0)

        newsymbol = request.GET.get('symbol', '')
        if newsymbol != '':
            symbol = newsymbol

        indicators = request.GET.getlist('indicators[]')

        bIntraday = int(request.GET.get('bIntraday', 0))
        newperiod = request.GET.get('period', '')
        newinterval = request.GET.get('interval', '')

        if newperiod != '':
            period = newperiod

        if newinterval != '':
            interval = newinterval

        # save setting start
        # if request.user.is_authenticated:
        #     dashboard = models.Dashboard.objects.get(user=request.user)

        dashboard = models.Dashboard.objects.get(id=dashboard_id)
        dashboard.bIntraday = bIntraday
        dashboard.period = period
        dashboard.interval = interval
        dashboard.symbol = symbol
        # save setting end

        df = prd.importLiveData(dashboard)

        if df is None:
            return JsonResponse(status=404, data={'status':'false','message':'Invalid symbol name'})

        dashboard.save()

        # trade ready

        # TradeSettingIndicator.objects.get(user=request.user)
        tradeis = models.TradeIndicator.objects.filter(backtest__dashboard__id = dashboard.id)        
        trades = tradelib.get_trades_plotresult(df, tradeis)

        plot_settings = get_tis_plot_settings(tradeis)        

        return JsonResponse({'prices' : df.to_json(orient='records'), 'trades' : trades, 'settings': plot_settings}, safe=True)


    def IndicatorSetting(request):
        assert isinstance(request, HttpRequest)

        if request.method == 'POST':
            # if not request.user.is_authenticated:
            #     return HttpResponse("user is not authenticated")
            tii_id = request.POST.get('tii_id', 0)
            dashboard_id = request.POST.get('dashboard_id', 0)
            # get model by ind id
            tii = models.TradeIndicatorIndicator.objects.get(id=tii_id)
            plots = tii.indicator.chartplot_set.all()

            settingvals = []
            for cp in plots:
                if cp.setting_manual:
                    color = request.POST.get('color_'+str(cp.id))
                    cpsetting = models.ChartPlotSetting.objects.update_setting(plot=cp, color=color)
                    # cpsetting = models.ChartPlotSetting.objects.update_setting(user=request.user, plot=cp, color=color)

                    # setting = models.ChartPlotSetting.objects.filter(plot=cp).first()

                    # if setting is None:
                    #     setting = models.ChartPlotSetting(plot=cp)
                    # setting.color = color
                    # setting.save()

                    settingvals.append({'plot_id': cp.id, 'plotname' : cp.plotname, 'color' : color, 'width' : 1, 'indicator_id' : tii.indicator.id})

            iis = tii.indicator.indicatorinputs.all()

            for ii in iis:
                value = request.POST.get('input_'+ii.parameter)
                set_input_value(tii, ii.parameter, value)

            df = pd.read_csv(settings.MEDIA_ROOT+'/labdata/OHLC'+str(dashboard_id)+'.csv', sep=',')
            df = pd.DataFrame(df)
            ti = tii.trade_indicator
            graphs = tradelib.get_trade_plotresult(df, ti)

            return JsonResponse({'tradeid': ti.id, 'trade' : graphs, 'settings': settingvals, 'with_main':ti.with_main}, safe=True)

        else:

            tii_id = request.GET.get('tii_id', 0)
            dashboard_id = request.GET.get('dashboard_id', 0)

            # get model by ind id
            tii = models.TradeIndicatorIndicator.objects.get(id=tii_id)

            #  chart plot setting must be filtered by also user
            plot_settings = get_tii_plot_settings(tii)


            # get trigger signal inputs
            signal_inputs = {}
            if tii.indicator.value_indicator == 1:
                if tii.indicator.id_letter == 'adr':
                    cp = models.ChartPlot.objects.filter(indicator__id_letter=tii.indicator.id_letter).first()

                    tipt = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator = tii).first()
                    if tipt is None:
                        tipt = models.TradeIndicatorPlotThreshold(trade_indicator_indicator = tii, plot = cp)
                        tipt.threshold_b = float(1.25)
                        tipt.threshold_s = float(0.9)
                        tipt.save()
                    signal_inputs = { 'ovb': tipt.threshold_b, 'ovs': tipt.threshold_s }
                elif tii.indicator.id_letter == 'aroon':
                    cp = models.ChartPlot.objects.filter(indicator__id_letter=tii.indicator.id_letter).first()

                    tipt = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator = tii).first()
                    if tipt is None:
                        tipt = models.TradeIndicatorPlotThreshold(trade_indicator_indicator = tii, plot = cp)
                        tipt.threshold_b = float(80)
                        tipt.threshold_s = float(20)
                        tipt.save()
                    signal_inputs = { 'ovb': tipt.threshold_b, 'ovs': tipt.threshold_s }
                elif tii.indicator.id_letter == 'bop':
                    cp = models.ChartPlot.objects.filter(indicator__id_letter=tii.indicator.id_letter).first()

                    tipt = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator = tii).first()
                    if tipt is None:
                        tipt = models.TradeIndicatorPlotThreshold(trade_indicator_indicator = tii, plot = cp)
                        tipt.threshold_b = float(0.75)
                        tipt.threshold_s = float(-0.75)
                        tipt.save()
                    signal_inputs = { 'ovb': tipt.threshold_b, 'ovs': tipt.threshold_s }

            # get input value models
            inputs = []
            iis = tii.indicator.indicatorinputs.all()

            config = configparser.ConfigParser()
            ini = config.read('dashboard/tradlablib/params.ini')

            for ii in iis:
                value = get_input_value(tii, ii.parameter)
                defvalue = get_input_default_value(tii.indicator.param_name, ii.parameter)

                # source candidates
                cand = []

                if ii.parameter == 'close_col':
                    cand = ['Open', 'High', 'Low', 'Close']
                    for atii in tii.trade_indicator.tradeindicatorindicator_set.all():
                        if atii.id != tii.id:
                            for acp in atii.indicator.chartplot_set.all():
                                cand.append(acp.plotname)

                inputs.append({'parameter': ii.parameter, 'value': value, 'defvalue': defvalue, 'cand': cand})

        return render(
            request,
            'dashboard/dashboard/indicatorsetting.html',
            context={
                'dashboard_id': dashboard_id,
                'tii_id': tii_id,
                'tii_letter': tii.indicator.id_letter,
                'PlotSettings': plot_settings,
                'Inputs': inputs,
                'SignalInputs': signal_inputs
            }
        )

    def SearchSymbols(request):
        assert isinstance(request, HttpRequest)

        keyword = request.GET.get('keyword', '')

        candidates = prd.symbolSearch(keyword)

        return JsonResponse(candidates, safe=False)


    def AddTradingIndicator(request):
        assert isinstance(request, HttpRequest)

        # if not request.user.is_authenticated:
        #     return HttpResponse("user is not authenticated")

        indid = request.GET.get('indid', '')
        dashboard_id = request.GET.get('dashboard_id', '')
        indicator = models.Indicator.objects.get(id_letter=indid)

        tis = models.TradeIndicator.objects.filter(backtest__dashboard__id = dashboard_id)
        wmtis = models.TradeIndicator.objects.filter(backtest__dashboard__id = dashboard_id, with_main=1)
        if len(tis) - len(wmtis) + 1 == MAX_TRADE_COUNT:
            return HttpResponse("countlimit")


        if indicator.combine_main:
            # ntrade = models.TradeIndicator.objects.get(user=request.user, with_main=True)
            ntrade = models.TradeIndicator.objects.filter(backtest__dashboard_id=dashboard_id, with_main=1).first()     # if exist, its not new trade
            if ntrade is None:
                # ntrade = models.TradeIndicator(user=request.user, trade_mode=0)
                ntrade = models.TradeIndicator(backtest_mode=0, with_main=1)
                if indicator.value_indicator > 0:
                    ntrade.backtest_mode = 1
                ntrade.save()
                backtest = models.Backtest()
                backtest.dashboard = models.Dashboard.objects.get(id=dashboard_id)
                backtest.mode = 0
                backtest.tradeindicator = ntrade
                backtest.save()
        else:
            # ntrade = models.TradeIndicator(user=request.user, trade_mode=0)
            ntrade = models.TradeIndicator(backtest_mode=0)
            if indicator.value_indicator > 0:
                ntrade.backtest_mode = 1
            ntrade.save()
            backtest = models.Backtest()
            backtest.dashboard = models.Dashboard.objects.get(id=dashboard_id)
            backtest.mode = 0
            backtest.tradeindicator = ntrade
            backtest.save()

        ntii = ntrade.tradeindicatorindicator_set.create(indicator=indicator)

        df = pd.read_csv(settings.MEDIA_ROOT+'/labdata/OHLC'+str(dashboard_id)+'.csv', sep=',')
        df = pd.DataFrame(df)
        graph = tradelib.get_trade_firstindicator_plotresult(df, ntii)

        return JsonResponse({'trade_id': ntrade.pk, 'graph': graph, 'with_main': indicator.combine_main}, safe=False)

    
    def AddTradingIndicatorIndicator(request):
        assert isinstance(request, HttpRequest)

        # if not request.user.is_authenticated:
        #     return HttpResponse("user is not authenticated")

        indid = request.GET.get('indid', '')
        trade_indicator_id = int(request.GET.get('trade_indicator_id', 0))
        dashboard_id = int(request.GET.get('dashboard_id', 0))
        if trade_indicator_id == 0:
            return HttpResponse("Trading Indicator ID is required!")
            # return tradlab.AddTradingIndicator(request)

        indicator = models.Indicator.objects.get(id_letter=indid)

        ntrade = models.TradeIndicator.objects.get(pk=trade_indicator_id)

        etii = ntrade.tradeindicatorindicator_set.filter(indicator=indicator)
        if etii.exists():
            return HttpResponse("Same Indicator already exists!")

        if ntrade.tradeindicatorindicator_set.all().count() == 2:
            return HttpResponse("Indicator combination count limit!")

        ntii = ntrade.tradeindicatorindicator_set.create(indicator=indicator)

        df = pd.read_csv(settings.MEDIA_ROOT+'/labdata/OHLC'+str(dashboard_id)+'.csv', sep=',')
        df = pd.DataFrame(df)
        graph = tradelib.get_trade_indicator_plotresult(df, ntrade, ntii)

        return JsonResponse({'trade_id': ntrade.pk, 'graph': graph}, safe=False)


    def RemoveTradingIndicatorIndicator(request):
        assert isinstance(request, HttpRequest)

        # if not request.user.is_authenticated:
        #     return HttpResponse("user is not authenticated")

        indid = request.GET.get('indid', '')
        trade_indicator_id = request.GET.get('trade_indicator_id', 0)

        indicator = models.Indicator.objects.get(id_letter=indid)

        trade = models.TradeIndicator.objects.get(pk=trade_indicator_id)
        trade_indicator = models.TradeIndicatorIndicator.objects.get(trade_indicator=trade, indicator=indicator)
        trade_indicator.delete()

        if trade.tradeindicatorindicator_set.all().count() == 0:
            trade.delete()

        return HttpResponse("success")


    def RemoveTradingIndicator(request):
        assert isinstance(request, HttpRequest)

        # if not request.user.is_authenticated:
        #     return HttpResponse("user is not authenticated")

        trade_indicator_id = request.GET.get('trade_indicator_id', 0)
        trade = models.TradeIndicator.objects.get(pk=trade_indicator_id)
        trade.delete()

        return HttpResponse("success")


    def RemoveBacktest(request):
        assert isinstance(request, HttpRequest)


        backtest_id = request.GET.get('backtest_id', 0)
        backtest = models.Backtest.objects.get(pk=backtest_id)
        backtest.delete()

        return HttpResponse("success")


    def RefreshBacktestListPanel(request): 
        assert isinstance(request, HttpRequest)

        dashboard_id = request.GET.get('dashboard_id', 0)
        backtests = models.Backtest.objects.filter(dashboard__id=dashboard_id).all()
        return render(
            request,
            'dashboard/dashboard/backtestlist.html',
            context={
                'Backtests' : backtests,
            }
        )

        
    def TradingIndicatorOptionSave(request):
        assert isinstance(request, HttpRequest)

        jsonstr = request.GET.get('data')
        data = json.loads(jsonstr)
        # data = json.loads(list(request.GET.keys())[0])

        # trade = models.TradeIndicator.objects.get(id=data['trade_indicator_id'])
        # trade.signal = data['signal']
        # trade.attribute = data['attribute']
        # trade.save()
        tiid = data['trade_indicator_id']
        backtest_mode = data['backtest_mode']

        ti = models.TradeIndicator.objects.get(id=tiid)
        ti.backtest_mode = backtest_mode
        ti.save()

        tradelib.save_trade_indicator_options(data['options'])

        return HttpResponse("successfully saved!")



    def TradingIndicatorOption(request):
        assert isinstance(request, HttpRequest)

        tradeid = request.GET.get('trade_indicator_id', 0)

        tradei = models.TradeIndicator.objects.get(pk=tradeid)
        allchoices = tradelib.get_trade_all_choices(tradei)

        return render(
            request,
            'dashboard/dashboard/tradingindicatoroptions.html',
            context={
                'Ti' : tradei,
                'Choice' : allchoices,
            }
        )


    def EnterSignalSave(request):
        assert isinstance(request, HttpRequest)

        signal = request.GET.get('signal', 0)

        if request.user.is_authenticated:
            chartsetting = models.ChartSetting.objects.get(user=request.user)

        chartsetting = models.ChartSetting.objects.all()[0]
        chartsetting.enter_signal = signal
        chartsetting.save()

        return HttpResponse('Success Saved!')

    
    def Backtest(request):
        assert isinstance(request, HttpRequest)     

        # backtest_id = request.GET.get('backtest_id')
        dashboard_id = request.GET.get('dashboard_id', 0)
        optmode = int(request.GET.get('optmode', 0))

        df = pd.read_csv(settings.MEDIA_ROOT+'/labdata/OHLC'+str(dashboard_id)+'.csv', sep=',')
        df = pd.DataFrame(df)
        dates = df['Date'].tolist()

        backtests = models.Backtest.objects.filter(dashboard__id = dashboard_id)
        invalids = ValidateBacktests(backtests)
        if len(invalids) > 0:
            return JsonResponse({'state': 'error', 'value': "Please set the backtest options of " + ",".join(invalids)})

        if optmode == 0:
            actmap, result, acts = bt.get_results(df, backtests)

            html = render(
                    request,
                    'dashboard/dashboard/tradlabstats.html',
                    context={
                        'result' : result,
                    }
                ).getvalue().decode("utf-8")

            html2 = render(
                    request,
                    'dashboard/dashboard/actmap.html',
                    context={
                        'backtests' : backtests,
                        'actmap' : actmap,
                        'acts' : acts,
                        'dates' : dates,
                    }
                ).getvalue().decode("utf-8")
            
            return JsonResponse({'state': 'ok', 'actmap': actmap, 'result' : result, 'acts': acts, 'html': html, 'html2': html2}, safe=True)
        elif optmode == 1:
            actmap, result, acts, bestparams = bt.get_optresults(df, backtests)

            html = render(
                    request,
                    'dashboard/dashboard/tradlabstats.html',
                    context={
                        'result' : result,
                    }
                ).getvalue().decode("utf-8")

            html1 = render(
                    request,
                    'dashboard/dashboard/bestparams.html',
                    context={
                        'bestparams' : bestparams,
                    }
                ).getvalue().decode("utf-8")    

            html2 = render(
                    request,
                    'dashboard/dashboard/actmap.html',
                    context={
                        'actmap' : actmap,
                        'acts' : acts,
                        'dates' : dates,
                        'backtests' : backtests,
                    }
                ).getvalue().decode("utf-8")

            return JsonResponse({'state': 'ok', 'actmap': actmap, 'result' : result, 'acts': acts, 'html': html, 'html1': html1, 'html2': html2}, safe=True)


    def SetBestParameters(request):
        assert isinstance(request, HttpRequest)

        backtest_id = request.GET.get('backtest_id')
        dashboard_id = request.GET.get('dashboard_id')

        backtest = models.Backtest.objects.get(id=backtest_id)

        if backtest.mode == 0:
            for tii in backtest.tradeindicator.tradeindicatorindicator_set.all():
                for ii in tii.indicator.indicatorinputs.all():
                    value = request.GET.get(ii.parameter)
                    set_input_value(tii, ii.parameter, value)


            if backtest.tradeindicator.backtest_mode == 1:
                tipt = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator__trade_indicator = backtest.tradeindicator).first()
                tipt.threshold_b = request.GET.get('ovb')
                tipt.threshold_s = request.GET.get('ovs')
                tipt.save()

            df = pd.read_csv(settings.MEDIA_ROOT+'/labdata/OHLC'+str(dashboard_id)+'.csv', sep=',')
            df = pd.DataFrame(df)
            ti = backtest.tradeindicator
            graphs = tradelib.get_trade_plotresult(df, ti)

            return JsonResponse({'tradeid': ti.id, 'trade' : graphs, 'with_main':ti.with_main}, safe=True)

    def DashboardSetting(request):
        assert isinstance(request, HttpRequest)

        if request.method == 'POST':
            # if not request.user.is_authenticated:
            #     return HttpResponse("user is not authenticated")
            dashboard_id = int(request.POST.get('dashboard_id', 0))

            # get model by dashboard id
            if dashboard_id == 0:
                # if not request.user.is_authenticated:
                #     return HttpResponse("user is not authenticated")
                # dashboard = models.Dashboard(user=request.user)
                dashboard = models.Dashboard()
            else:
                dashboard = models.Dashboard.objects.filter(id=dashboard_id).first()

            dashboard.title = request.POST.get('title', 'My Dashboard')
            dashboard.bIntraday = request.POST.get('bIntraday', 0)
            dashboard.interval = request.POST.get('interval', '15min')
            dashboard.period = request.POST.get('period', '36m')
            dashboard.symbol = request.POST.get('symbol', 'GOLD')

            dashboard.save()

            df = prd.importLiveData(dashboard)

            if df is None:
                dashboard.symbol = 'GOLD'
                dashboard.save()
                return HttpResponse('Data Importing Failed!')

            # return JsonResponse({'tradeid': ti.id, 'trade' : graphs, 'settings': settingvals, 'with_main':ti.with_main}, safe=True)
            return redirect('/'+str(dashboard.id))

        else:

            dashboard_id = int(request.GET.get('dashboard_id', 0))

            if dashboard_id == 0:
                # if not request.user.is_authenticated:
                #     return HttpResponse("user is not authenticated")
                dashboard = models.Dashboard()
            else:
                dashboard = models.Dashboard.objects.filter(id=dashboard_id).first()


        return render(
            request,
            'dashboard/dashboard/dashboardsetting.html',
            context={
                'dashboard': dashboard,
                'dashboard_id': dashboard_id,
                'Intervals' : prd.INTRADAY_TIMESERIES_INTERVAL,
                'Periods' : prd.HISTORICAL_TIMESERIES_PERIODS,
            }
        )


    def DeleteDashboard(request, dashboard_id):
        assert isinstance(request, HttpRequest)

        # dashboards = models.Dashboard.objects.filter(user=request.user)
        dashboard_cnt = models.Dashboard.objects.all().count()
        if dashboard_cnt == 1:
            return redirect('/'+str(dashboard_id))

        dashboard = models.Dashboard.objects.get(id=dashboard_id)
        dashboard.delete()

        return redirect('/0')

    
    def BacktestAttributeSave(request):
        assert isinstance(request, HttpRequest)

        backtest_id = request.GET.get('backtest_id', 0)
        attribute = request.GET.get('attribute', 0)

        backtest = models.Backtest.objects.get(id = backtest_id)
        backtest.attribute = attribute
        backtest.save()

        return HttpResponse('success')


    def TriggerSignal(request, indicator_letter):
        assert isinstance(request, HttpRequest)

        dashboard_id = int(request.GET.get('dashboard_id', 0))
        tii_id = int(request.GET.get('tii_id', 0))

        df = pd.read_csv(settings.MEDIA_ROOT+'/labdata/OHLC'+str(dashboard_id)+'.csv', sep=',')
        df = pd.DataFrame(df)

        tii = models.TradeIndicatorIndicator.objects.get(id=tii_id)

        ti = tii.trade_indicator


        if tii.indicator.value_indicator == 1:
            ovb = request.GET.get('ovb')
            ovs = request.GET.get('ovs')

            tipt = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator__trade_indicator = ti).first()
            tipt.threshold_b = float(request.GET.get('ovb'))
            tipt.threshold_s = float(request.GET.get('ovs'))
            tipt.save()


        if indicator_letter=='acc':
            ind = acc.AccumulationDistribution(df, graph_['data'])
            signal_graph = ind.trigger()
        elif indicator_letter=='adr':
            ind = adr.AdvanceDeclineRatio(df, tii, ti)
            signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
        elif indicator_letter=='aroon':
            ind = aroon.Aroon(df, tii, ti)
            signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
        elif indicator_letter=='bop':
            ind = bop.BalanceOfPower(df, tii, ti)
            signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)

            
        return JsonResponse({"signal_graph":signal_graph, "traderet": traderet}, safe=True)


    def OptimalTrade(request, indicator_letter):
        assert isinstance(request, HttpRequest)

        dashboard_id = int(request.GET.get('dashboard_id', 0))
        tii_id = int(request.GET.get('tii_id', 0))

        df = pd.read_csv(settings.MEDIA_ROOT+'/labdata/OHLC'+str(dashboard_id)+'.csv', sep=',')
        df = pd.DataFrame(df)

        tii = models.TradeIndicatorIndicator.objects.get(id=tii_id)

        ti = tii.trade_indicator

        bt = models.Backtest.objects.get(tradeindicator=ti)

        if indicator_letter=='acc':
            ind = acc.AccumulationDistribution(df)
            signal_graph = ind.trigger()
        elif indicator_letter=='adr':
            ind = adr.AdvanceDeclineRatio(df, tii, ti)
            psetb, pret, signalsmap = ind.train()
        elif indicator_letter=='aroon':
            ind = aroon.Aroon(df, tii, ti)
            psetb, pret, signalsmap = ind.train()
        elif indicator_letter=='bop':
            ind = bop.BalanceOfPower(df, tii, ti)
            psetb, pret, signalsmap = ind.train()
        
            
        bestparams = []
        param = []

        for i,v in psetb.items():
            if i != 'Returns%' and i != 'MaxR':
                param.append({'parameter':i, 'value':v})

        bestparams.append({'backtest_id': bt.id, 'title': ti.title(), 'tradeindicator_id': ti.id, 'params': param })

        html1 = render(
                request,
                'dashboard/dashboard/bestparams.html',
                context={
                    'bestparams' : bestparams,
                }
            ).getvalue().decode("utf-8")    

        return JsonResponse({'html': html1}, safe=True)