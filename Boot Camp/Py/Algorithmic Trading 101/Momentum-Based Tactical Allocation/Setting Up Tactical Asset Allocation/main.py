class MomentumBasedTacticalAllocation(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2007, 8, 1)  # Set Start Date
        self.SetEndDate(2010, 8, 1)  # Set End Date
        
        #1. Subscribe to SPY -- S&P 500 Index ETF -- using daily resolution
        self.spy = self.AddEquity("SPY", Resolution.Daily)
        
        #2. Subscribe to BND -- Vanguard Total Bond Market ETF -- using daily resolution
        self.bnd = self.AddEquity("BND", Resolution.Daily)
        
        #3. Set strategy cash to $3000
        self.SetCash(3000)
        
    def OnData(self, data):
        
        pass