class FadingTheGap(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2017, 11, 1)  
        self.SetEndDate(2018, 7, 1)  
        self.SetCash(100000)  
        self.AddEquity("TSLA", Resolution.Minute)
        
        #1. Create a scheduled event to run every day at "0 minutes" before 
        # TSLA market close that calls the method ClosingBar
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.BeforeMarketClose("TSLA", 0), self.ClosingBar) 
        
        #2. Create a scheduled event to run every day at 1 minute after 
        # TSLA market open that calls the method OpeningBar
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TSLA", 1), self.OpeningBar)
        
        #3. Create a scheduled event to run every day at 45 minutes after 
        # TSLA market open that calls the method ClosePositions
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TSLA", 45), self.ClosePositions)
    
    #1. Create an empty method ClosingBar
    def ClosingBar(self):
        pass
    
    #2. Create an empty method OpeningBar
    def OpeningBar(self):
        pass
    
    #3. Create a method ClosePositions
        # Liquidate our position to limit our exposure and keep our holding period short 
    def ClosePositions(self):
        self.Liquidate()