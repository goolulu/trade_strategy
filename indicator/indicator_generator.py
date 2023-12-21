import datetime

import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats

from data_source import DataSource


class IndicatorGenerator:

    def SMA(self, data: pd.DataFrame, N: int) -> pd.Series:


        ret = data['close'].rolling(window=N).mean()
        ret.index = data['trade_date'].apply(lambda x: datetime.datetime.strptime(x, '%Y%M%d'))
        return ret

    def RSI(self):

        data['close'].rolling

        pass


if __name__ == '__main__':
    data = DataSource().select_list('history', 'hs_stock_quotation')
    print(IndicatorGenerator().SMA(data, 5))
