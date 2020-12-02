from datetime import timedelta, datetime

class SMAPairsTrading(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 7, 1)   
        self.SetEndDate(2019, 3, 31)
        self.SetCash(100000)
        
        symbols = [Symbol.Create("PEP", SecurityType.Equity, Market.USA), Symbol.Create("KO", SecurityType.Equity, Market.USA)]
        self.UniverseSettings.Resolution = Resolution.Hour
        self.UniverseSettings.DataNormalizationMode = DataNormalizationMode.Raw
        self.AddUniverseSelection(ManualUniverseSelectionModel(symbols))
        self.AddAlpha(PairsTradingAlphaModel())
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        self.SetExecution(ImmediateExecutionModel())
        
    #3. Use OnEndOfDay() to Log() your positions at the close of each trading day.
    def OnEndOfDay(self, symbol):
        self.Log("Taking a position of " + str(self.Portfolio[symbol].Quantity) + "units of symbol " + str(symbol))
        
    
class PairsTradingAlphaModel(AlphaModel):

    def __init__(self):
        self.pair = [ ]
        self.spreadMean = SimpleMovingAverage(500)
        self.spreadStd = StandardDeviation(500)
        #1. Set self.period to a 2 hour timedelta 
        self.period = timedelta(hours=2)
        
    def Update(self, algorithm, data):

        spread = self.pair[1].Price - self.pair[0].Price
        self.spreadMean.Update(algorithm.Time, spread)
        self.spreadStd.Update(algorithm.Time, spread)
        
        upperthreshold = self.spreadMean.Current.Value + self.spreadStd.Current.Value
        lowerthreshold = self.spreadMean.Current.Value - self.spreadStd.Current.Value
        
        #2. Emit an Insight.Group() if the spread is greater than the upperthreshold 
        if spread > upperthreshold:
            return Insight.Group(
                [
                    Insight.Price(self.pair[0].Symbol, self.period, InsightDirection.Up),
                    Insight.Price(self.pair[1].Symbol, self.period, InsightDirection.Down)
                ])
        
        #2. Emit an Insight.Group() if the spread is less than the lowerthreshold
        if spread < lowerthreshold:
            return Insight.Group(
                [
                    Insight.Price(self.pair[0].Symbol, self.period, InsightDirection.Down),
                    Insight.Price(self.pair[1].Symbol, self.period, InsightDirection.Up)
                ])
        
        # If the spread is not greater than the upper or lower threshold, do not return Insights
        return []
    
    def OnSecuritiesChanged(self, algorithm, changes):
        self.pair = [x for x in changes.AddedSecurities]