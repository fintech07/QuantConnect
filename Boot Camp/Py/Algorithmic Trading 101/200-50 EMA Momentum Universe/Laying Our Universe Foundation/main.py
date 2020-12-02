class EMAMomentumUniverse(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2019, 1, 7)
        self.SetEndDate(2019, 4, 1)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)
        self.selected = None
    
    def CoarseSelectionFunction(self, coarse):
        #1. Sort coarse by dollar volume
        self.sortedByDollarVolume = sorted(coarse, key=lambda c: c.DollarVolume, reverse=True)
        
        #2. Filter out the stocks less than $10 and return selected
        self.selected = [c.Symbol for c in self.sortedByDollarVolume if c.Price > 5][:10]
        return self.selected

    def OnSecuritiesChanged(self, changes): 
        #3. Liquidate securities leaving the universe
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol)
        #4. Allocate 10% holdings to each asset added to the universe
        for security in changes.AddedSecurities:
            self.SetHoldings(security.Symbol, 0.10)