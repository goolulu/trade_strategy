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
        sma = pd.Series(sma_values, index=data['trade_date'])
        price = pd.Series(data=data['close'].values, index=data['trade_date'])
        figure = plt.figure()
        ax1 = figure.add_subplot()
        price.plot()
        plt.show()

    def RSI(self):
        pass


if __name__ == '__main__':
    data = DataSource().select_list('history','hs_stock_quotation')
    IndicatorGenerator().SMA(data,5)