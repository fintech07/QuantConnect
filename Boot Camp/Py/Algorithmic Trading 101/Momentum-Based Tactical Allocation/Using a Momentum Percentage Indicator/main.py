class MomentumBasedTacticalAllocation(QCAlgorithm):

    spyMomentum = None
    bondMomentum = None

    def Initialize(self):
        self.SetStartDate(2007, 6, 1)  
        self.SetEndDate(2010, 6, 1)  
        self.SetCash(3000)   
        
        self.spy = self.AddEquity("SPY", Resolution.Daily)  
        self.bnd = self.AddEquity("BND", Resolution.Daily)  
        
        #1. Add 50-day Momentum Percent indicator for SPY
        self.spyMomentum = self.MOMP("SPY", 50, Resolution.Daily)
        
        #2. Add 50-day Momentum Percent indicator for BND
        self.bondMomentum = self.MOMP("BND", 50, Resolution.Daily)

    def OnData(self, data):
        pass