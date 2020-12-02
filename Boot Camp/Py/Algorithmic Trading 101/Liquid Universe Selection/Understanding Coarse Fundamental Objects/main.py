class LiquidUniverseSelection(QCAlgorithm):
    
    filteredByPrice = None

    def Initialize(self):
        self.SetStartDate(2019, 1, 11)  
        self.SetEndDate(2019, 7, 1) 
        self.SetCash(100000)  
        self.AddUniverse(self.CoarseSelectionFilter)
        
    def CoarseSelectionFilter(self, coarse):
        
        #1. Sort descending by daily dollar volume
        sortedByDollarVolume = sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)  
        
        #2. Select only Symbols with a price of more than $10 per share
        self.filteredByPrice = [x.Symbol for x in sortedByDollarVolume if x.Price > 10]
        
        #3. Return the 8 most liquid Symbols from the filteredByPrice list
        self.filteredByPrice = self.filteredByPrice[:8]
        return self.filteredByPrice