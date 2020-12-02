class FadingTheGap(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2017, 11, 1)
        self.SetEndDate(2018, 7, 1)
        self.SetCash(100000) 
        self.AddEquity("TSLA", Resolution.Minute)
        
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.BeforeMarketClose("TSLA", 0), self.ClosingBar) 
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TSLA", 1), self.OpeningBar)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TSLA", 45), self.ClosePositions) 
        
        self.window = RollingWindow[TradeBar](2)
        
    def ClosingBar(self):
        self.window.Add(self.CurrentSlice["TSLA"])
    
    def OpeningBar(self):
        if "TSLA" in self.CurrentSlice.Bars:
            self.window.Add(self.CurrentSlice["TSLA"])
        
        #1. If our window is not full use return to wait for tomorrow
        if not self.window.IsReady:
            return
        
        #2. Calculate the change in overnight price
        delta = self.window[0].Open - self.window[1].Close
        
        #3. If delta is less than -$2.5, SetHoldings() to 100% TSLA
        if delta < -2.5:
            self.SetHoldings("TSLA", 1)
        
    def ClosePositions(self):
        self.Liquidate()