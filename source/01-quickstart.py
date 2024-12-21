import datetime
#import pandas_ta as ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover

import talib

#print(GOOG)

#Simple crossover strategy

class RsiOscillator(Strategy):

    upper_bound = 70
    lower_bound = 30 #traditional RSI crossover vals
    rsi_window = 14

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window) #pass closing price, num periods

    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()

bt = Backtest(GOOG, RsiOscillator, cash = 10_000)
stats = bt.run()
print(stats)
bt.plot()
