import datetime

import akshare as ak

from data_source import DataSource


class StockTick:

    def __init__(self):
        self.column = ['成交时间', '成交价格', '价格变动', '成交量', '成交金额', '性质']
        self.convert_column = ['biz_time', 'biz_price', 'price_chg', 'volume', 'turnover', 'order_type']

        self.dict_map = dict(zip(self.column, self.convert_column))
        self.datasource = DataSource()

    def fetch_stock_tick(self, symbol):
        stock_zh_a_tick_tx_js_df = ak.stock_zh_a_tick_tx_js(symbol=symbol).rename(columns=self.dict_map)
        ak.stock_zh_a_tick_tx()
        stock_zh_a_tick_tx_js_df['symbol'] = symbol[2:]
        stock_zh_a_tick_tx_js_df['trade_date'] = datetime.datetime.now().strftime('%Y%m%d')
        stock_zh_a_tick_tx_js_df['order_type'] = stock_zh_a_tick_tx_js_df['order_type'].apply(convert_order_type)

        print('jjjj')
        self.datasource.insert_many(stock_zh_a_tick_tx_js_df.to_dict(orient="records"),
                                    'history', 'hs_stock_tick')

def convert_order_type(type) -> str:
    if type == '买盘':
        return 'buy'
    elif type =='卖盘':
        return 'sell'
    else:
        return 'mid'

if __name__ == '__main__':
    StockTick().fetch_stock_tick("sh601318")