from datetime import datetime

class AgTD(PythonData):
    ''' Ag(T+D) '''

    def GetSource(self, config, date, isLive):
        source = "https://www.dropbox.com/s/bdwce94elrt7bem/Ag%28T%2BD%29.csv?dl=0"
        return SubscriptionDataSource(source, SubscriptionTransportMedium.RemoteFile)


    def Reader(self, config, line, date, isLive):
        # If first character is not digit, pass
        if not (line.strip() and line[0].isdigit()): return None

        data = line.split(',')
        agtd = AgTD()
        agtd.Symbol = config.Symbol
        agtd.Time = datetime.strptime(data[0], '%Y/%m/%d %H:%M:%S.%f')
        agtd.Value = decimal.Decimal(data[1])
        agtd["Bid"] = float(data[1])
        agtd["Ask"] = float(data[2])
        agtd.Value = (agtd["Ask"] + agtd["Bid"]) / 2

        return agtd

class UncoupledMultidimensionalRegulators(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 11, 9)  # Set Start Date
        #self.SetEndDate(2020, 11, 24)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.Debug("Loading data.");
        self.AgTD = self.AddData(AgTD, "AgTD", Resolution.Tick).Symbol
        self.Debug("Complete loading data. ");

    def OnData(self, data):
        if data.ContainsKey("AgTD"):
            agtd = data["AgTD"]
            mid = agtd.Value
            self.Plot("Price Chart", "Ag(T+D)", mid)
            
            self.Debug(datetime.strftime(agtd.Time) + " : " + str(mid))