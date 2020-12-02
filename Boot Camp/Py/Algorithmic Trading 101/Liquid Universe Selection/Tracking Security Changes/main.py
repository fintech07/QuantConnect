class LiquidUniverseSelection(QCAlgorithm):
    
    filteredByPrice = None
    changes = None
    
    def Initialize(self):
        self.SetStartDate(2019, 1, 11)  
        self.SetEndDate(2019, 7, 1) 
        self.SetCash(100000)  
        self.AddUniverse(self.CoarseSelectionFilter)
        
    def CoarseSelectionFilter(self, coarse):
    
        sortedByDollarVolume = sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)  
        
        filteredByPrice = [x.Symbol for x in sortedByDollarVolume if x.Price > 10]
       
        return filteredByPrice[:8]
    
    #1. Create a function OnSecuritiesChanged
    def OnSecuritiesChanged(self, changes):
        #2. Save securities changed as self.changes 
        self.changes = changes
        #3. Log the changes in the function 
        self.Log(f"OnSecuritiesChanged({self.Time}):: {changes}")