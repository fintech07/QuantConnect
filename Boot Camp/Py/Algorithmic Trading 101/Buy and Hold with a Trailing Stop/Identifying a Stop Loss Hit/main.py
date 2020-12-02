class BootCampTask(QCAlgorithm):
    
    # Order ticket for our stop order, Datetime when stop order was last hit
    stopMarketTicket = None
    stopMarketFillTime = datetime.min
    
    def Initialize(self):
        self.SetStartDate(2018, 12, 1)
        self.SetEndDate(2019, 4, 1)
        self.SetCash(100000)
        spy = self.AddEquity("SPY", Resolution.Daily)
        spy.SetDataNormalizationMode(DataNormalizationMode.Raw)
        
    def OnData(self, data):
        
        #4. Check that at least 15 days (~2 weeks) have passed since we last hit our stop order
        if (self.Time - self.stopMarketFillTime).days < 15:
            return;
        
        if not self.Portfolio.Invested:
            self.MarketOrder("SPY", 500)
            
            #1. Create stop loss through a stop market order
            self.stopMarketTicket = self.StopMarketOrder("SPY", -500, 0.9 * self.Securities["SPY"].Close)
        
    def OnOrderEvent(self, orderEvent):
        
        if orderEvent.Status != OrderStatus.Filled:
            return
        
        # Printing the security fill prices.
        self.Debug(self.Securities["SPY"].Close)
        
        #2. Check if we hit our stop loss (Compare the orderEvent.Id with the stopMarketTicket.OrderId)
        #   It's important to first check if the ticket isn't null (i.e. making sure it has been submitted)
        if self.stopMarketTicket is not None and orderEvent.OrderId == self.stopMarketTicket.OrderId:
            #3. Store datetime
            self.stopMarketFillTime = self.Time