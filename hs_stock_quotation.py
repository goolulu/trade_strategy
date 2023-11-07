import datetime

import akshare as ak
from typing import Any, Type, Dict, List, Optional

from data_source import DataSource


def convert_date(trade_date: datetime) -> str:
    return trade_date.strftime('%Y%m%d')


class StockQuotation:

    def __init__(self):
        self.index: List = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额',
                            '换手率']

        self.convert_index: List = ['trade_date', 'open', 'close', 'high', 'low', 'volume', 'turnover', 'amplitude',
                                    'price_per_change', 'price_change', 'turnover_ratio']
        self.map: Dict = dict(zip(self.index, self.convert_index))

        self.datasource = DataSource()

    def fetch_hs_stock_quotation(self, symbol: str, period: str = None, start_date: str = None, end_date: str = None,
                                 adjust: str = None) -> None:
        if period is None:
            period = 'daily'
        if start_date is None:
            start_date = '20130101'
        if end_date is None:
            end_date = datetime.datetime.now().strftime('%Y%m%d')
        if adjust is None:
            adjust = ''

        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date,
                                                end_date=end_date, adjust=adjust).rename(columns=self.map)
        stock_zh_a_hist_df['symbol'] = symbol
        stock_zh_a_hist_df['trade_date'] = stock_zh_a_hist_df['trade_date'].apply(convert_date)
        self.datasource.insert_many(stock_zh_a_hist_df.to_dict(orient='records'), 'history', 'hs_stock_quotation')



if __name__ == '__main__':
    sq = StockQuotation()
    sq.fetch_hs_stock_quotation('601318')
