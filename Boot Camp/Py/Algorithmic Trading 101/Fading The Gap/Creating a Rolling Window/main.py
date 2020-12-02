class FadingTheGap(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2017, 11, 1) 
        self.SetEndDate(2018, 7, 1) 
        self.SetCash(100000)
        self.AddEquity("TSLA", Resolution.Minute)
        
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.BeforeMarketClose("TSLA", 0), self.ClosingBar)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TSLA", 1), self.OpeningBar)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TSLA", 45), self.ClosePositions) 
        
        #1. Save a RollingWindow with type TradeBar and length of 2 as self.window
        self.window = RollingWindow[TradeBar](2)
    
    def ClosingBar(self):
        #2. Add the final bar of TSLA to our rolling window
        self.window.Add(self.CurrentSlice["TSLA"])
 
    def OpeningBar(self):
        #3. If "TSLA" is in the current slice, add the current slice to the window
        if "TSLA" in self.CurrentSlice.Bars:
            self.window.Add(self.CurrentSlice["TSLA"])
        
    def ClosePositions(self):
        self.Liquidate()