class MomentumBasedTacticalAllocation(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2007, 8, 1) 
        self.SetEndDate(2010, 8, 1) 
        self.SetCash(3000)   
        
        self.spy = self.AddEquity("SPY", Resolution.Daily)  
        self.bnd = self.AddEquity("BND", Resolution.Daily)  
        
        self.spyMomentum = self.MOMP("SPY", 50, Resolution.Daily)
        self.bondMomentum = self.MOMP("BND", 50, Resolution.Daily) 
        
        self.SetBenchmark("SPY")  
        self.SetWarmUp(50) 
        
    def OnData(self, data):
        
        # Don't place trades until our indicators are warmed up:
        if self.IsWarmingUp:
            return
        
        #1. If SPY has more upward momentum than BND, then we liquidate our holdings in BND and allocate 100% of our equity to SPY
        if self.spyMomentum.Current.Value > self.bondMomentum.Current.Value:
            self.Liquidate("BND")
            self.SetHoldings("SPY", 1)
            

        #2. Otherwise we liquidate our holdings in SPY and allocate 100% to BND
        if self.spyMomentum.Current.Value < self.bondMomentum.Current.Value:
            self.Liquidate("SPY")
            self.SetHoldings("BND", 1)