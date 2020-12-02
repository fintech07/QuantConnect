from datetime import timedelta

class OpenRangeBreakout(QCAlgorithm):
    
    openingBar = None
    currentBar = None

    def Initialize(self):
        self.SetStartDate(2018, 7, 10) # Set Start Date  
        self.SetEndDate(2019, 6, 30) # Set End Date 
        self.SetCash(100000)  # Set Strategy Cash 
        
        # Subscribe to TSLA with Minute Resolution
        self.symbol = self.AddEquity("TSLA", Resolution.Minute)
        
        #1. Create our consolidator with a timedelta of 30 min
        self.Consolidate("TSLA", timedelta(minutes=30), self.OnDataConsolidated)
        
    def OnData(self, data):
        pass
    
    #2. Create a function OnDataConsolidator which saves the currentBar as bar
    def OnDataConsolidated(self, bar):
        self.currentBar = bar