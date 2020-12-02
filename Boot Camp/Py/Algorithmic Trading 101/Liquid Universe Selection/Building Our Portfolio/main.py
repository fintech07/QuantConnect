class LiquidUniverseSelection(QCAlgorithm):
    
    filteredByPrice = None
    
    def Initialize(self):
        self.SetStartDate(2019, 1, 11)  
        self.SetEndDate(2019, 7, 1) 
        self.SetCash(100000)  
        self.AddUniverse(self.CoarseSelectionFilter)
        # Ignore this for now, we'll cover it in the next task.
        self.UniverseSettings.Resolution = Resolution.Daily 

    def CoarseSelectionFilter(self, coarse):
        sortedByDollarVolume = sorted(coarse, key=lambda x: x.DollarVolume, reverse=True) 
        filteredByPrice = [x.Symbol for x in sortedByDollarVolume if x.Price > 10]
        return filteredByPrice[:8]
   
    def OnSecuritiesChanged(self, changes):
        self.changes = changes
        self.Log(f"OnSecuritiesChanged({self.UtcTime}):: {changes}")
        
        #1. Liquidate removed securities
        for security in changes.RemovedSecurities:
            if security.Invested:
                self.Liquidate(security.Symbol)
        
        #2. We want 10% allocation in each security in our universe
        for security in changes.AddedSecurities:
            self.SetHoldings(security.Symbol, 0.1)