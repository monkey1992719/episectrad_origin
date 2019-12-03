from dashboard.tradlablib.peakdetect import peakdetect

class AccumulationDistribution(object):

    def __init__(self, data, ao):
        self.data = data
        self.ao = ao

    
    def trigger(self):
        close = self.data['Close']
        date = self.data['Date']
        res = peakdetect(y_axis=close, lookahead=10)
        res = res[0]

        signals_x1 = []
        signals_x2 = []
        
        signals_y1 = []
        signals_y2 = []

        signals_main_y1 = []
        signals_main_y2 = []

        signal_graph = []
        print(signal_graph)
        for i in range(len(res)-1):
            peak = res[i]
            nextpeak = res[i+1]
            if (peak[1] > nextpeak[1] and close[peak[0]] < close[nextpeak[0]]) or (peak[1] < nextpeak[1] and close[peak[0]] > close[nextpeak[0]]):
                signals_x1.append(date[peak[0]])
                signals_x2.append(date[nextpeak[0]])
                signals_y1.append(peak[1])
                signals_y2.append(nextpeak[1])
                signals_main_y1.append(self.ao[peak[0]])
                signals_main_y2.append(self.ao[nextpeak[0]])

        signal_graph.append({'x1': signals_x1, 'y1': signals_y1, 'x2': signals_x2, 'y2': signals_y2, 'type': 'signal-line', 'name': 'ao_divergence', 'id': 'ao'})
        signal_graph.append({'x1': signals_x1, 'y1': signals_main_y1, 'x2': signals_x2, 'y2': signals_main_y2, 'type': 'signal-line', 'name': 'ao_divergence', 'id': 'main'})

        return signal_graph
        