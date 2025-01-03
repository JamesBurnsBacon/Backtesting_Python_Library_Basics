import datetime
import talib
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover, resample_apply
from backtesting.test import GOOG

# Ensure the data has a DatetimeIndex
if not isinstance(GOOG.index, pd.DatetimeIndex):
    GOOG['Date'] = pd.to_datetime(GOOG['Date'])
    GOOG.set_index('Date', inplace=True)

class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14 #same for daily and weekly currently

    # All initial calculations
    def init(self):
        self.daily_rsi = self.I(talib.RSI
                                , pd.Series(self.data.Close), self.rsi_window)
        
        # does all the resampling 
        self.weekly_rsi = resample_apply(
            'W-FRI', talib.RSI, pd.Series(self.data.Close), self.rsi_window)
        #Weekly, Friday being close


    def next(self):

        if (crossover(self.daily_rsi, self.upper_bound) and
                self.weekly_rsi[-1] > self.upper_bound):
            self.position.close()

        elif (crossover(self.lower_bound, self.daily_rsi) and
                self.lower_bound > self.weekly_rsi[-1]):
            self.buy()


bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)
stats = bt.run()
bt.plot()