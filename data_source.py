import json

import pymongo
import pandas as pd
from pandas import DataFrame


class DataSource:

    def __init__(self):
        self.type = "mongo"
        self.client = pymongo.MongoClient(host='47.107.60.105',
                                          port=27017,
                                          username="Abel",
                                          password="1qaz@WSX3edc")

    def insert_one(self, json, db: str, table: str):
        if json is None:
            raise Exception('插入数据不能为空')
        db = self.client[db]
        table = db[table]
        table.insert_one(json)

    def insert_many(self, doc: list[dict], db: str, table: str):
        if doc is None:
            raise Exception('插入数据不能为空')
        db = self.client[db]
        table = db[table]

        table.insert_many(doc)

    def select_list(self, db: str, table: str, *args, **kwargs) -> DataFrame:
        db = self.client[db]
        table = db[table]
        cursor = table.find(args, kwargs)
        result = []
        for data in cursor:
            result.append(data)
        return pd.DataFrame(result)


if __name__ == '__main__':
    aa = DataSource()
