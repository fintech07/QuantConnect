class BootCampTask(QCAlgorithm):

    def Initialize(self):
        
        self.SetStartDate(2018, 12, 1) 
        self.SetEndDate(2019, 4, 1) 
        self.SetCash(100000) 
        spy = self.AddEquity("SPY", Resolution.Daily)
        spy.SetDataNormalizationMode(DataNormalizationMode.Raw)
        self.lastOrderEvent = None
        
    def OnData(self, data):
    
        if not self.Portfolio.Invested:
            self.MarketOrder("SPY", 500)
            self.StopMarketOrder("SPY", -500, 0.9 * self.Securities["SPY"].Close)
        
    def OnOrderEvent(self, orderEvent):
        
        #1. Write code to only act on fills
            #2. Save the orderEvent to lastOrderEvent, use Debug to print the event OrderId
            
        if orderEvent.Status == OrderStatus.Filled:
            self.lastOrderEvent = orderEvent
            self.Debug(orderEvent.OrderId)