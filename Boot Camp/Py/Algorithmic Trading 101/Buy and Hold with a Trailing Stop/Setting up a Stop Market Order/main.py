class BootCampTask(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 12, 1) # Set Start Date
        self.SetEndDate(2019, 4, 1) # Set End Date
        self.SetCash(100000) # Set Strategy Cash
        
        #1. Subscribe to SPY in raw mode
        self.spy = self.AddEquity("SPY", Resolution.Daily)
        self.spy.SetDataNormalizationMode(DataNormalizationMode.Raw)
        
    def OnData(self, data):
        
        if not self.Portfolio.Invested:
            #2. Create market order to buy 500 units of SPY
            self.MarketOrder("SPY", 500)
            
            #3. Create a stop market order to sell 500 units at 90% of the SPY current price
            self.StopMarketOrder("SPY", -500, 0.9 * self.Securities["SPY"].Close)