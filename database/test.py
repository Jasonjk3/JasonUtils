# -*- ecoding: utf-8 -*-
# @ModuleName: test
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2021/5/6 11:40
# @Desc:

import pandas as pd

from database.MongoDB import MongoDBClient

if __name__ == '__main__':
    """连接"""
    # 常量定义
    uri = "mongodb://user:32SZnr518000@139.159.204.92:27017/"
    db = "spiderServer"
    collection = "weibo_comments2"
    mongodb = MongoDBClient(uri, db, collection)  # 连接数据库
    print(mongodb)  # 基本信息
    result = mongodb.find_all()
    print(result)

    df = pd.DataFrame(result)
    print(df.head())

    print(df['item_id'].value_counts())

    # MongoDBClient(uri,db)