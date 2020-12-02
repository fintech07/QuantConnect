class EMAMomentumUniverse(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2019, 1, 7)
        self.SetEndDate(2019, 4, 1)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)
    
    def CoarseSelectionFunction(self, coarse):
        sortedByDollarVolume = sorted(coarse, key=lambda c: c.DollarVolume, reverse=True) 
        selected = [c.Symbol for c in sortedByDollarVolume if c.Price > 10][:10]
        return selected
        
    def OnSecuritiesChanged(self, changes):  
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol) 
        for security in changes.AddedSecurities:
            self.SetHoldings(security.Symbol, 0.10)

#1. Create a class SelectionData
    #2. Create a constructor that takes self 
    def __init__(self):
        #2. Save the fast and slow ExponentialMovingAverage
        self.slow = ...
        self.fast = ...
    
    #3. Check if our indicators are ready
    
    #4. Use the "indicator.Update" method to update the time and price of both indicators