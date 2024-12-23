import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover
import matplotlib.pyplot as plt
import seaborn as sns

import talib

#print(GOOG)

#Simple crossover strategy
#Long only
#Max position size at every entry/exit

def optim_func(series):

    if series["# Trades"] < 10:
        return -1 # filtering out every result with fewer than 10 trades
    
    return series["Equity Final [$]"] / series["Exposure Time [%]"] #Max returns for lowest time in market

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
stats, heatmap = bt.optimize(
    upper_bound = range(55, 85, 5),
    lower_bound = range(10, 45, 5),
    rsi_window = 14, #range(10, 30, 2),
    maximize = optim_func, #""
    constraint = lambda param: param.upper_bound > param.lower_bound,
    #max_tries = 100 #Randomized grid search using these variables, helps with overfitting
    return_heatmap = True,
)

#print(heatmap)
#print(stats)

hm = heatmap.groupby(["upper_bound", "lower_bound"]).mean().unstack()
sns.heatmap(hm)
plt.show()

#print(hm)

lower_bound_result = stats["_strategy"].lower_bound
upper_bound_result = stats["_strategy"].upper_bound

bt.plot(filename=f'Backtest_HTML_Graphs/RSI_Plot-{lower_bound_result}-{upper_bound_result}.html')
