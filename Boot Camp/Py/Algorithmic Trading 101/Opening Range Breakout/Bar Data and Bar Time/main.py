class OpeningRangeBreakout(QCAlgorithm):
    
    openingBar = None 
  
    def Initialize(self):
        self.SetStartDate(2018, 7, 10)  
        self.SetEndDate(2019, 6, 30)  
        self.SetCash(100000)  
        self.AddEquity("TSLA", Resolution.Minute)
        self.Consolidate("TSLA", timedelta(minutes=30), self.OnDataConsolidated)
        
    def OnData(self, data):
        pass
        
    def OnDataConsolidated(self, bar):
        #1. Check the time, we only want to work with the first 30min after Market Open
        if bar.Time.hour == 9 and bar.Time.minute == 30:
            #2. Save one bar as openingBar 
            self.openingBar = bar