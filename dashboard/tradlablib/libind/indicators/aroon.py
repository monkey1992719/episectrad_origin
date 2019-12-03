from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind

class Aroon(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'aroon_up':
                self.aroon_up=pltdt['y']
            elif pltdt['name'] == 'aroon_down':
                self.aroon_down=pltdt['y']

    
    def trigger(self, ovb, ovs):
        aroon_up = self.aroon_up
        aroon_down = self.aroon_down

        signals_ovbs = []

        signals_ovbe = []

        signals_ovss = []

        signals_ovse = []

        signal_graph = []

        signals = []    # 0: stop 1: buy 2: sell
        prevsig = 0
        signals.append(prevsig)
        for i in range(1, len(aroon_up)):
            if aroon_up[i-1] < ovb and aroon_up[i] >= ovb:
                prevsig = 2
                signals_ovbe.append({'x': i, 'y': aroon_up[i]})

            if aroon_down[i-1] < ovb and aroon_down[i] >= ovb:
                prevsig = 1
                signals_ovse.append({'x': i, 'y': aroon_up[i]})

            if aroon_up[i-1] > ovb and aroon_up[i] <= ovb:
                prevsig = 0
                signals_ovbs.append({'x': i, 'y': aroon_up[i]})

            if aroon_down[i-1] > ovb and aroon_down[i] <= ovb:
                prevsig = 0
                signals_ovss.append({'x': i, 'y': aroon_up[i]})

            signals.append(prevsig)

        signal_graph.append({'data': signals_ovbs, 'type': 'signal-ovbs', 'name': 'signal-ovbs', 'id': self.ti.pk})
        signal_graph.append({'data': signals_ovbe, 'type': 'signal-ovbe', 'name': 'signal-ovbe', 'id': self.ti.pk})
        signal_graph.append({'data': signals_ovss, 'type': 'signal-ovss', 'name': 'signal-ovss', 'id': self.ti.pk})
        signal_graph.append({'data': signals_ovse, 'type': 'signal-ovse', 'name': 'signal-ovse', 'id': self.ti.pk})

        signal_graph.append({'y': [ovb], 'type': 'signal-threshold-ovb', 'name': 'signal-threshold-ovb', 'id': self.ti.pk})
        signal_graph.append({'y': [ovs], 'type': 'signal-threshold-ovs', 'name': 'signal-threshold-ovs', 'id': self.ti.pk})

        traderet = trade_with_signals(self.data, signals)

        return signal_graph, signals, traderet
        

    def train(self):
        cols = []
        params1 = []
        for ii in self.tii.indicator.indicatorinputs.all():
            params1.append(get_input_value(self.tii, ii.parameter))
            cols.append(ii.parameter)

        if len(params1) > 0:
            params1 = prepare_params_for_aroon(*params1)

        cols.extend(['ovb', 'ovs', 'Returns%', 'MaxR'])
        pret = pd.DataFrame(columns=cols)

        arglist = [[]]      # make all possible parameter combinations
        for p in params1:
            newarglist = []
            for pp in p:
                for argset in arglist:
                    newargset = argset.copy()
                    newargset.append(pp)
                    newarglist.append(newargset)

            arglist = newarglist
        
        signalsmap = dict()

        ipret = 0
        for argset in arglist:
            graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii, True, *argset)
            for pltdt in graphdata:
                if pltdt['name'] == 'aroon_up':
                    pltdt1=pltdt['y']
                elif pltdt['name'] == 'aroon_down':
                    pltdt2=pltdt['y']

            maxv = max(pltdt1)
            minv = min(pltdt1)
            ovba = np.arange((maxv+minv)/2, maxv, (maxv-minv)/10, dtype=int)
            ovsa = np.arange((maxv+minv)/2, minv, -(maxv-minv)/10, dtype=int)

            ovba = np.delete(ovba, 0)
            ovsa = np.delete(ovsa, 0)
            for ovb in ovba:
                for ovs in ovsa:
                    self.aroon_up = pltdt1
                    self.aroon_down = pltdt2

                    signal_graph, signals, traderet = self.trigger(ovb, ovs)
                    if traderet['winlossratio'] is None or traderet['winlossratio'] == np.inf:
                        traderet = 0
                    else:
                        traderet = traderet['winlossratio']

                    parama = argset.copy()
                    parama.extend([ovb, ovs, traderet, ''])
                    pret.loc[ipret] = parama
                    signalsmap[ipret] = signals
                    ipret+=1
        
        retcol = pret['Returns%']
        imax = np.array(retcol).argmax()
        pret.at[imax, 'MaxR'] = 'MR'
        psetb = pret.loc[imax]
        return psetb, pret, signalsmap[imax]