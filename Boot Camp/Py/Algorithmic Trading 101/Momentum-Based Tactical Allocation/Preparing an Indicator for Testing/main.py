class MomentumBasedTacticalAllocation(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2007, 8, 1)  
        self.SetEndDate(2010, 8, 1)  
        self.SetCash(3000)  
        
        self.AddEquity("SPY", Resolution.Hour)  
        self.AddEquity("BND", Resolution.Hour) 
        
        self.spyMomentum = self.MOMP("SPY", 50, Resolution.Daily) 
        self.bondMomentum = self.MOMP("BND", 50, Resolution.Daily) 
        
        #1. Set SPY Benchmark
        self.SetBenchmark("SPY")
        
        #2. Warm up algorithm for 50 days to populate the indicators prior to the start date
        self.SetWarmUp(50)
    
    def OnData(self, data):
        # You should validate indicators are ready before using them:
        if self.spyMomentum is None or self.bondMomentum is None or not self.bondMomentum.IsReady or not self.spyMomentum.IsReady:
            return