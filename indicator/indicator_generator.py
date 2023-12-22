import datetime

import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats
import talib
from data_source import DataSource


class IndicatorGenerator:

    def SMA(self, data: pd.Series, N: int) -> pd.Series:
        ret = data.rolling(window=N).mean()
        return ret

    def TA_SMA(self, data: pd.Series, N: int) -> pd.Series:
        return talib.SMA(data, timeperiod=N)

    def RSI(self, data: pd.Series, N: int):
        up = data.where(data > 0, 0)
        down = -data.where(data < 0, 0)
        up_ma = self.SMA(up, N)
        down_ma = self.SMA(down, N)
        rs = up_ma / down_ma
        rsi = rs * 100
        return rsi

    def ta_RSI(self, data: pd.Series, N: int):
        return talib.RSI(data, timeperiod=N)


if __name__ == '__main__':
    data = DataSource().select_list('history', 'hs_stock_quotation').tail(300)
    sma = IndicatorGenerator().SMA(data['close'], 6)
    ta_sma = IndicatorGenerator().TA_SMA(data['close'], 6)
    ta_rsi = IndicatorGenerator().ta_RSI(data['close'], 12)
    print(ta_rsi)
    print('fjkla')
    print(ta_sma)
