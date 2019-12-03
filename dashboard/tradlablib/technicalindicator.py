from . import model_guilib

from dashboard import models

# Parameters
# df : data
# indname : indicatorname
# tii : trade_indicator_indicator
def display_indicator(df, indname, tii, withparams = False, *arglist):

    stats_mdt = {}

    indicator = models.Indicator.objects.get(name=indname)
    id = indicator.id_letter

    method_get_mdt = getattr(model_guilib, 'get_mdt_' + id)
    data = method_get_mdt(df, [], stats_mdt, tii, withparams, *arglist)

    for pltdt in data:
        pltdt['x'] = pltdt['x'].tolist()
        pltdt['y'] = pltdt['y'].fillna(0).tolist()

    return data
