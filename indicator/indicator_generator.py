import datetime

import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats

from data_source import DataSource


class IndicatorGenerator:

    def SMA(self, data: pd.DataFrame, N: int) -> pd.DataFrame:
        history = []
        sma_values = []
        for close in data['close']:
            history.append(close)
            if (len(history) > N):
                del (history[0])
            sma_values.append(stats.mean(history))

        figure = plt.figure()
        ax = figure.subplots()
        date = data['trade_date'].apply(lambda x: datetime.datetime.strptime(x,'%Y%m%d'))
        ax.plot(date.values, sma_values, label='sma')
        ax.plot(date.values, data['close'].values, label='close')
        ax.set_xlabel("time [day]")
        ax.set_ylabel("price")
        ax.legend()
        ax.plot()
        figure.show()

    def RSI(self):
        pass


if __name__ == '__main__':
    data = DataSource().select_list('history', 'hs_stock_quotation')
    IndicatorGenerator().SMA(data, 5)
