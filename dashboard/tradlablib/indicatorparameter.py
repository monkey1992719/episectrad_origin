from dashboard import models
import configparser


# Read the params.ini file
config = configparser.ConfigParser()
ini = config.read('dashboard/tradlablib/params.ini')

def get_input_value(tii, param):

    iv = tii.indicatorinputvalue_set.filter(indicator_input__parameter=param).first()

    ii = models.IndicatorInput.objects.get(parameter=param)
    datatype = ii.datatype
    
    value = 0

    if not iv:
        value = config[tii.indicator.param_name][param]
    else:
        value = iv.value

    if datatype == 'int':
        value = int(value)
    elif datatype == 'string':
        value = str(value)
    elif datatype == 'float':
        value = float(value)

    return value


def get_input_default_value(ind, param):

    value = config[ind][param]

    return value


def set_input_value(tii, param, value):

    ii = tii.indicator.indicatorinputs.filter(parameter=param).first()

    iv = tii.indicatorinputvalue_set.filter(indicator_input=ii).first()
    if iv is None:
        iv = tii.indicatorinputvalue_set.create(indicator_input=ii, value=value)
    else:
        iv.value = value
        iv.save()

    return iv