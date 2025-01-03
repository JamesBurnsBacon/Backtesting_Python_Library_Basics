import datetime
#import pandas_ta as ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover

import talib

#print(GOOG)

#Simple crossover strategy
def SMA(values, n):
        return pd.Series(values).rolling(n).mean() #helper function

class SmaCross(Strategy):
    #MA lags as class variables
    lag1 = 10
    lag2 = 20

    def init(self):
        #precompute the two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.lag1)
        self.sma2 = self.I(SMA, self.data.Close, self.lag2)

    def next(self):
        if crossover(self.sma1, self.sma2): #bullish reversal
            self.position.close()
            self.buy()
        elif crossover(self.sma2, self.sma1): #bearish reversal
            self.position.close()
            self.sell()

#no order size assumes maximum possible position
bt = Backtest(GOOG, SmaCross, cash = 10_000, commission=.002) #0.2% commission
stats = bt.run()
print(stats)
bt.plot()