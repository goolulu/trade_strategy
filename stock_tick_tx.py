import datetime

import akshare as ak
import pandas as pd

from data_source import DataSource
from pandas import DataFrame


class StockTick:

    def __init__(self):
        self.column = ['成交时间', '成交价格', '价格变动', '成交量', '成交金额', '性质']
        self.convert_column = ['biz_time', 'biz_price', 'price_chg', 'volume', 'turnover', 'order_type']

        self.dict_map = dict(zip(self.column, self.convert_column))
        self.datasource = DataSource()

        self.db = 'history'
        self.table = 'hs_stock_tick'

    def fetch_stock_tick(self, symbol: str, trade_date: str = None):

        reuslt: DataFrame

        if trade_date is None:
            stock_zh_a_tick_tx_js_df = ak.stock_zh_a_tick_tx_js(symbol=symbol).rename(columns=self.dict_map)
            stock_zh_a_tick_tx_js_df['symbol'] = symbol[2:]
            stock_zh_a_tick_tx_js_df['inner_symbol'] = symbol
            stock_zh_a_tick_tx_js_df['trade_date'] = datetime.datetime.now().strftime('%Y%m%d')
            stock_zh_a_tick_tx_js_df['order_type'] = stock_zh_a_tick_tx_js_df['order_type'].apply(convert_order_type)
            reuslt = stock_zh_a_tick_tx_js_df
        else:
            stock_zh_a_tick_tx_df = ak.stock_zh_a_tick_tx(symbol=symbol, trade_date=trade_date).rename(
                columns=self.dict_map)
            if stock_zh_a_tick_tx_df.values.size == 0:
                print("交易日%s 暂时无数据" % trade_date)
                return
            stock_zh_a_tick_tx_df['inner_symbol'] = symbol
            stock_zh_a_tick_tx_df['symbol'] = symbol[2:]
            stock_zh_a_tick_tx_df['trade_date'] = datetime.datetime.now().strftime('%Y%m%d')
            stock_zh_a_tick_tx_df['order_type'] = stock_zh_a_tick_tx_df['order_type'].apply(convert_order_type)
            reuslt = stock_zh_a_tick_tx_df

        self.datasource.insert_many(reuslt.to_dict(orient="records"),
                                    self.db, self.table)

    def select_list(self, symbol=None) -> DataFrame:
        return self.datasource.select_list(self.db, self.table)


def convert_order_type(type) -> str:
    if type == '买盘':
        return 'buy'
    elif type == '卖盘':
        return 'sell'
    else:
        return 'mid'


if __name__ == '__main__':
    # StockTick().fetch_stock_tick("sh601318")
    # 小于20w 散户, 20w到100w牛户，100w以上机构
    smail_power = 200000
    middle_power = 1000000

    tick_list = StockTick().select_list()
    sell_orders = tick_list[tick_list['order_type'] == 'sell']
    buy_orders = tick_list[tick_list['order_type'] == 'buy']
    retail_investor_buy = buy_orders[buy_orders['turnover'] < smail_power]
    retail_investor_sell = sell_orders[sell_orders['turnover'] < smail_power]

    retail_investor_sell = sell_orders[
        (buy_orders['turnover'] >= smail_power) and (buy_orders['turnover'] < middle_power)]
