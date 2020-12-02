class FrameworkAlgorithm(QCAlgorithm):
    
    def Initialize(self):
        
        self.SetStartDate(2013, 10, 1)   
        self.SetEndDate(2013, 12, 1)    
        self.SetCash(100000)

        #1. Set the NullUniverseSelectionModel()
        
        #2. Set the NullAlphaModel()

        #3. Set the NullPortfolioConstructionSelectionModel()

        #4. Set the NullRiskManagementModel()

        #5. Set the NullExecutionModel()