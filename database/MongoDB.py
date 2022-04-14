# -*- ecoding: utf-8 -*-
# @ModuleName: MongoDB
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2021/5/6 11:30
# @Desc:

import pymongo


class MongoDBClient:
    def __init__(self, uri='mongodb://localhost:27017/', db='test', collection=None):
        """初始化MongoDB数据库和表的信息并连接数据库

        :param uri: 连接名
        :param db: 数据库名
        :param collection: 表名
        """
        self.uri = uri
        self.client = pymongo.MongoClient(uri)

        self.db_name = db_name
        self.collection_name = collection_name

        if db_name is not None and self.db_name not in self.client.list_database_names():
            print("数据库不存在！")
        if collection_name is not None and self.collection_name not in self.client[db_name].list_collection_names():
            print("表不存在！")

    def __str__(self):
        """数据库基本信息"""
        db = self.client[self.db_name]._Database__name
        collection = self.client[self.db_name][self.collection_name]._Collection__name
        num = len(self)
        return "数据库[{}] 表[{}] 共{}条数据".format(db, collection, num)

    def __len__(self):
        """表的数据条数"""
        return self.client[self.db_name][self.collection_name].count_documents(filter={})

    def change_db(self, db_name, collection_name=None):
        if db_name is not None:
            self.db_name = db_name
        if collection_name is not None:
            self.collection_name = collection_name

    def insert(self, *args, **kwargs):
        """插入多条数据

        :param args: 多条数据，可以是dict、dict的list或dict的tuple
        :param kwargs: 单条数据，如name=XerCis, gender=male
        :return: 添加的数据在库中的_id
        """
        documents = []
        for i in args:
            if isinstance(i, dict):
                documents.append(i)
            else:
                documents += [x for x in i]
        documents.append(kwargs)
        return self.client[self.db_name][self.collection_name].insert_many(documents)

    def delete(self, *args, **kwargs):
        """删除一批数据

        :param args: 字典类型，如{"gender": "male"}
        :param kwargs: 直接指定，如gender="male"
        :return: 已删除条数
        """
        list(map(kwargs.update, args))
        result = self.client[self.db_name][self.collection_name].delete_many(kwargs)
        return result.deleted_count

    def update(self, *args, **kwargs):
        """更新一批数据

        :param args: dict类型的固定查询条件如{"author":"XerCis"}，循环查询条件一般为_id列表如[{'_id': ObjectId('1')}, {'_id': ObjectId('2')}]
        :param kwargs: 要修改的值，如country="China", age=22
        :return: 修改成功的条数
        """
        value = {"$set": kwargs}
        query = {}
        n = 0
        list(map(query.update, list(filter(lambda x: isinstance(x, dict), args))))  # 固定查询条件
        for i in args:
            if not isinstance(i, dict):
                for id in i:
                    query.update(id)
                    result = self.client[self.db_name][self.collection_name].update_one(query, value)
                    n += result.modified_count
        result = self.client[self.db_name][self.collection_name].update_many(query, value)
        return n + result.modified_count

    def find(self, *args, **kwargs):
        """保留原接口"""
        return self.client[self.db_name][self.collection_name].find(*args, **kwargs)



if __name__ == '__main__':
    """连接"""
    # 常量定义
    uri = "mongodb://user:32SZnr518000@139.159.204.92:27017/"
    db = "spiderServer"
    collection = "weibo_comments2"
    mongodb = MongoDBClient(uri, db, collection)  # 连接数据库
    print(mongodb)  # 基本信息

    # """增"""
    # mongodb.insert(author="XerCis", gender="male")  # 插入一条数据
    # mongodb.insert({"country": "China"})  # 插入一条数据，dict
    # mongodb.insert([{"country": "Japan"}, {"country": "Korea"}])  # 插入一批数据，dict的list
    # result = mongodb.insert(({"country": "American"}, {"country": "Australia"}))  # 插入一批数据，dict的tuple
    # # mongodb.insert({"country": "China"}, [{"country": "Japan"}, {"country": "Korea"}], country="American")# 多类型传参
    # print(result.inserted_ids)  # 添加的数据在库中的_id
    # print(len(mongodb))  # 表的数据条数
    # print(mongodb.find_all())  # 所有查询结果
    #
    # """删"""
    # print(mongodb.delete(country="Japan"))  # 删除国家为日本的所有记录
    # print(mongodb.delete(country={"$regex": "^A"}))  # 删除国家开头为A的所有记录
    # # print(mongodb.delete({"country": {"$regex": "^A"}}))#效果同上
    #
    # """改"""
    # id = mongodb.find_col("_id")  # 查询所有_id
    # print(id)
    # print(mongodb.update(id, {"author": "XerCis"}, country="China", age=22, height=178))
    # print(mongodb.find_col(author="XerCis"))


