from dashboard import models

def get_plot_setting(cp):
    cpdsetting = models.ChartPlotDefaultSetting.objects.filter(plot=cp).first()
    cpsetting = models.ChartPlotSetting.objects.filter(plot=cp).first()

    # get default plot settings
    settingval = {}

    if cpsetting is None:
        settingval = { 'plot_id': cp.id, 'plotname' : cp.plotname, 'color' : cpdsetting.color, 'width' : cpdsetting.width, 'defaultcolor' : cpdsetting.color, 'defaultwidth' : cpdsetting.width }
    else:
        settingval = { 'plot_id': cp.id, 'plotname' : cp.plotname, 'color' : cpsetting.color, 'width' : cpsetting.width,  'defaultcolor' : cpdsetting.color, 'defaultwidth' : cpdsetting.width }

    # return {'plot_id': cp.id, 'plotname' : cp.plotname, 'color' : color, 'width' : 1, 'indicator_id' : tii.indicator.id}
    return settingval


def get_plots_settings(cps):
    settingvals = []

    for cp in cps:
        if cp.setting_manual:
            settingvals.append(get_plot_setting(cp))
    
    return settingvals   
    

def get_tii_plot_settings(tii):
    return get_plots_settings(tii.indicator.chartplot_set.all())


def get_tiis_plot_settings(tiis):
    settingvals = []

    for tii in tiis:
        settingvals.extend(get_tii_plot_settings(tii))        
    
    return settingvals


def get_ti_plot_settings(ti):
    
    return get_tiis_plot_settings(ti.tradeindicatorindicator_set.all())


def get_tis_plot_settings(tis):
    settingvals = []

    for ti in tis:
        settingvals.extend(get_ti_plot_settings(ti))
    
    return settingvals