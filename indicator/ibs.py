"""
基于微观市场结构的择时策略
基于知情交易者行为模式的择时策略
"""

from data_source import DataSource as ds
def init(context):
   context.stock_pool = []

