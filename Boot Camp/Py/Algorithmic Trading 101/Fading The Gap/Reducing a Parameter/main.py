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
                
        #1. Create a manual Standard Deviation indicator to track recent volatility
        self.volatility = StandardDeviation("TSLA", 60)
        
    def OnData(self, data):
        if data["TSLA"] is not None: 
            #2. Update our standard deviation indicator manually with algorithm time and TSLA's close price
            self.volatility.Update(self.Time, data["TSLA"].Close)
    
    def OpeningBar(self):
        if "TSLA" in self.CurrentSlice.Bars:
            self.window.Add(self.CurrentSlice["TSLA"])
        
        #3. Use IsReady to check if both volatility and the window are ready, if not ready 'return'
        if not self.window.IsReady or not self.volatility.IsReady:
            return
        
        delta = self.window[0].Open - self.window[1].Close
        
        #4. Save an approximation of standard deviations to our deviations variable by dividing delta by the current volatility value:
        #   Normally this is delta from the mean, but we'll approximate it with current value for this lesson. 
        deviations = delta / self.volatility.Current.Value 
        
        #5. SetHoldings to 100% TSLA if deviations is less than -3 standard deviations from the mean:
        if deviations < -3:
            self.SetHoldings("TSLA", 1)
        
    def ClosePositions(self):
        self.Liquidate()
        
    def ClosingBar(self):
        self.window.Add(self.CurrentSlice["TSLA"])