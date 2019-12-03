from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib

class BalanceOfPower(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'bop':
                self.bop=pltdt['y']
                break

    
    def trigger(self, ovb, ovs):
        bop = self.bop

        signals_ovbs = []

        signals_ovbe = []

        signals_ovss = []

        signals_ovse = []

        signal_graph = []

        signals = []    # 0: stop 1: buy 2: sell
        prevsig = 0
        signals.append(prevsig)
        for i in range(1, len(bop)):
            if (bop[i] >= ovb and bop[i-1] < ovb):
                #overbought start
                signals_ovbs.append({'x': i, 'y': bop[i]})
                prevsig = 0
            elif (bop[i-1] > ovb and bop[i] <= ovb):
                #overbought end, sell start
                signals_ovbe.append({'x': i, 'y': bop[i]})
                prevsig = 2
            elif (bop[i-1] > ovs and bop[i] <= ovs):
                #oversold start
                signals_ovss.append({'x': i, 'y': bop[i]})
                prevsig = 0
            elif (bop[i-1] < ovs and bop[i] >= ovs):
                #oversold end, buy start
                signals_ovse.append({'x': i, 'y': bop[i]})
                prevsig = 1
            
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
        
        cols.extend(['ovb', 'ovs', 'Returns%', 'MaxR'])
        pret = pd.DataFrame(columns=cols)

        signalsmap = dict()

        ipret = 0
        
        maxv = max(self.bop)
        minv = min(self.bop)
        ovba = np.arange((maxv+minv)/2, maxv, (maxv-minv)/20, dtype=int)
        ovsa = np.arange((maxv+minv)/2, minv, -(maxv-minv)/20, dtype=int)

        ovba = np.delete(ovba, 0)
        ovsa = np.delete(ovsa, 0)
        for ovb in ovba:
            for ovs in ovsa:
                signal_graph, signals, traderet = self.trigger(ovb, ovs)
                if traderet['winlossratio'] is None or traderet['winlossratio'] == np.inf:
                    traderet = 0
                else:
                    traderet = traderet['winlossratio']

                parama = [ovb, ovs, traderet, '']
                pret.loc[ipret] = parama
                signalsmap[ipret] = signals
                ipret+=1
        
        retcol = pret['Returns%']
        imax = np.array(retcol).argmax()
        pret.at[imax, 'MaxR'] = 'MR'
        psetb = pret.loc[imax]
        return psetb, pret, signalsmap[imax]