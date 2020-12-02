class CopulaPairTradingTest(QCAlgorithm):

    def Initialize(self):
        pass

    def OnData(self, data):
        '''Main event handler. Implement trading logic.'''

        self.SetSignal(slice)     # only executed at first day of each month

        # Daily rebalance
        if self.Time.day == self.day:
            return
        
        long, short = self.pair[0], self.pair[1]

        # Update current price to trading pair's historical price series
        for kvp in self.Securities:
            symbol = kvp.Key
            if symbol in self.pair:
                price = kvp.Value.Price
                self.window[symbol].append(price)

        if len(self.window[long]) < 2 or len(self.window[short]) < 2:
            return
        
        # Compute the mispricing indices for u and v by using estimated copula
        MI_u_v, MI_v_u = self._misprice_index()

        # Placing orders: if long is relatively underpriced, buy the pair
        if MI_u_v < self.floor_CL and MI_v_u > self.cap_CL:
            
            self.SetHoldings(short, -self.weight_v, False, f'Coef: {self.coef}')
            self.SetHoldings(long, self.weight_v * self.coef * self.Portfolio[long].Price / self.Portfolio[short].Price)

        # Placing orders: if short is relatively underpriced, sell the pair
        elif MI_u_v > self.cap_CL and MI_v_u < self.floor_CL:

            self.SetHoldings(short, self.weight_v, False, f'Coef: {self.coef}')
            self.SetHoldings(long, -self.weight_v * self.coef * self.Portfolio[long].Price / self.Portfolio[short].Price)
        
        self.day = self.Time.day

    def PairSelection(self, date):
        '''Selects the pair of stocks with the maximum Kendall tau value.
        It's called on first day of each month'''

        if date.month == self.month:
            return Universe.Unchanged

        symbols = [Symbol.Create(x, SecurityType.Equity, Market.USA)
                for x in [
                    "QQQ", "XLK",
                    "XME", "EWG",
                    "TNA", "TLT",
                    "FAS", "FAZ",
                    "XLF", "XLU",
                    "EWC", "EWA",
                    "QLD", "QID"
                ]]

        logreturns = self._get_historical_returns(symbols, self.lookbackdays)

        tau = 0
        for i in range(0, len(symbols), 2):

            x = logreturns[str(symbols[i])]
            y = logreturns[str(symbols[i+1])]

            # Estimate Kendall rank correlation for each pair
            tau_ = kendalltau(x, y)[0]

            if tau > tau_:
                continue

            tau = tau_
            self.pair = symbols[i:i+2]

        return [x.Value for x in self.pair]


        def _parameter(self, family, tau):
            ''' Estimate the parameters for three kinds of Archimedean copulas
            according to association between Archimedean copulas and the Kendall rank correlation measure
            '''
            
            if  family == 'clayton':
                return 2 * tau / (1 - tau)
            
            elif family == 'frank':
                
                '''
                debye = quad(integrand, sys.float_info.epsilon, theta)[0]/theta  is first order Debye function
                frank_fun is the squared difference
                Minimize the frank_fun would give the parameter theta for the frank copula 
                ''' 
                
                integrand = lambda t: t / (np.exp(t) - 1)  # generate the integrand
                frank_fun = lambda theta: ((tau - 1) / 4.0  - (quad(integrand, sys.float_info.epsilon, theta)[0] / theta - 1) / theta) ** 2
                
                return minimize(frank_fun, 4, method='BFGS', tol=1e-5).x 
            
            elif family == 'gumbel':
                return 1 / (1 - tau)

        def _lpdf_copula(self, family, theta, u, v):
            '''Estimate the log probability density function of three kinds of Archimedean copulas
            '''
            
            if  family == 'clayton':
                pdf = (theta + 1) * ((u ** (-theta) + v ** (-theta) - 1) ** (-2 - 1 / theta)) * (u ** (-theta - 1) * v ** (-theta - 1))
                
            elif family == 'frank':
                num = -theta * (np.exp(-theta) - 1) * (np.exp(-theta * (u + v)))
                denom = ((np.exp(-theta * u) - 1) * (np.exp(-theta * v) - 1) + (np.exp(-theta) - 1)) ** 2
                pdf = num / denom
                
            elif family == 'gumbel':
                A = (-np.log(u)) ** theta + (-np.log(v)) ** theta
                c = np.exp(-A ** (1 / theta))
                pdf = c * (u * v) ** (-1) * (A ** (-2 + 2 / theta)) * ((np.log(u) * np.log(v)) ** (theta - 1)) * (1 + (theta - 1) * A ** (-1 / theta))
                
            return np.log(pdf)

        
        def SetSignal(self, slice):
            '''Computes the mispricing indices to generate the trading signals.
            It's called on first day of each month'''

            if self.Time.month == self.month:
                return
            
            ## Compute the best copula
            
            # Pull historical log returns used to determine copula
            logreturns = self._get_historical_returns(self.pair, self.numdays)
            x, y = logreturns[str(self.pair[0])], logreturns[str(self.pair[1])]

            # Convert the two returns series to two uniform values u and v using the empirical distribution functions
            ecdf_x, ecdf_y  = ECDF(x), ECDF(y)
            u, v = [ecdf_x(a) for a in x], [ecdf_y(a) for a in y]
            
            # Compute the Akaike Information Criterion (AIC) for different copulas and choose copula with minimum AIC
            tau = kendalltau(x, y)[0]  # estimate Kendall'rank correlation
            AIC ={}  # generate a dict with key being the copula family, value = [theta, AIC]
            
            for i in ['clayton', 'frank', 'gumbel']:
                param = self._parameter(i, tau)
                lpdf = [self._lpdf_copula(i, param, x, y) for (x, y) in zip(u, v)]
                # Replace nan with zero and inf with finite numbers in lpdf list
                lpdf = np.nan_to_num(lpdf) 
                loglikelihood = sum(lpdf)
                AIC[i] = [param, -2 * loglikelihood + 2]
                
            # Choose the copula with the minimum AIC
            self.copula = min(AIC.items(), key = lambda x: x[1][1])[0]
            
            ## Compute the signals
            
            # Generate the log return series of the selected trading pair
            logreturns = logreturns.tail(self.lookbackdays)
            x, y = logreturns[str(self.pair[0])], logreturns[str(self.pair[1])]
            
            # Estimate Kendall'rank correlation
            tau = kendalltau(x, y)[0] 
            
            # Estimate the copula parameter: theta
            self.theta = self._parameter(self.copula, tau)
            
            # Simulate the empirical distribution function for returns of selected trading pair
            self.ecdf_x, self.ecdf_y  = ECDF(x), ECDF(y) 
            
            # Run linear regression over the two history return series and return the desired trading size ratio
            self.coef = stats.linregress(x,y).slope
            
            self.month = self.Time.month