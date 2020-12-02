from datetime import timedelta, datetime

class SMAPairsTrading(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 7, 1)   
        self.SetEndDate(2019, 3, 31)
        self.SetCash(100000)
        
        symbols = [Symbol.Create("PEP", SecurityType.Equity, Market.USA), Symbol.Create("KO", SecurityType.Equity, Market.USA)]
        self.AddUniverseSelection(ManualUniverseSelectionModel(symbols))
        self.UniverseSettings.Resolution = Resolution.Hour
        
        #1. Create an instance of the PairsTradingAlphamodel()
        self.AddAlpha(PairsTradingAlphaModel())
        
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        self.SetExecution(ImmediateExecutionModel())
         
class PairsTradingAlphaModel(AlphaModel): 

    def __init__(self):
        #2. Initialize an empty list self.pair = [ ]
        self.pair = []

    def Update(self, algorithm, data): 
        
        #3. Set the price difference calculation to spread.
        spread = self.pair[1].Price - self.pair[0].Price
        return []
    
    def OnSecuritiesChanged(self, algorithm, changes):
        
        #4. Set self.pair to the changes.AddedSecurities changes
        self.pair = [x for x in changes.AddedSecurities]