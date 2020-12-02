class LiquidUniverseSelection(QCAlgorithm):
    
    filteredByPrice = None
    coarse = None
    
    def Initialize(self):
        self.SetStartDate(2019, 1, 11)  
        self.SetEndDate(2019, 7, 1) 
        self.SetCash(100000)  
        
        #3. Add a Universe model using Coarse Fundamental Data and set the filter function 
        self.AddUniverse(self.CoarseSelectionFilter)
        
    #1. Add an empty filter function
    def CoarseSelectionFilter(self, coarse):
        #2. Save coarse as self.coarse and return an Unchanged Universe
        self.coarse = coarse
        return Universe.Unchanged