from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.tradlab.dashtradlab, name='dashboard'),
    path('<int:dashboard_id>/', views.tradlab.dashtradlab),
    path('recogchartpattern', views.tradlab.recogchartpattern),
    path('addchartpattern', views.tradlab.addchartpattern),
    path('recogpricebarpattern', views.tradlab.recogpricebarpattern),
    path('addpricebarpattern', views.tradlab.addpricebarpattern),
    path('symbolperiodchange', views.tradlab.symbolperiodchange),
    path('indicatorsetting', views.tradlab.IndicatorSetting),
    path('searchsymbols', views.tradlab.SearchSymbols),
    path('addtradingindicator', views.tradlab.AddTradingIndicator),
    path('addtradingindicatorindicator', views.tradlab.AddTradingIndicatorIndicator),
    path('removetradingindicator', views.tradlab.RemoveTradingIndicator),
    path('removetradingindicatorindicator', views.tradlab.RemoveTradingIndicatorIndicator),
    path('removebacktest', views.tradlab.RemoveBacktest),
    path('refreshBacktestListPanel', views.tradlab.RefreshBacktestListPanel),
    path('tradingindicatoroption', views.tradlab.TradingIndicatorOption),
    path('tradingindicatoroptionsave', views.tradlab.TradingIndicatorOptionSave),
    path('entersignalsave', views.tradlab.EnterSignalSave),
    path('backtest', views.tradlab.Backtest),
    path('backtestattributesave', views.tradlab.BacktestAttributeSave),
    path('setbestparameters', views.tradlab.SetBestParameters),
    path('dashboardsetting', views.tradlab.DashboardSetting),
    path('deletedashboard/<int:dashboard_id>/', views.tradlab.DeleteDashboard),
    path('triggersignal/<str:indicator_letter>/', views.tradlab.TriggerSignal),
    path('optimaltrade/<str:indicator_letter>/', views.tradlab.OptimalTrade),


    url(r"^login$", views.LoginView.as_view(), name="login"),
    url(r"^signup$", views.SignupView.as_view(), name="signup"),
    url(r"^signup/email-sent$", views.SignupEmailSentView.as_view(), name="signup_email_sent"),
    url(r"^signup/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.SignupConfirmView.as_view(), name="signup_confirm"),
]
