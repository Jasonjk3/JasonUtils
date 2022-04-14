# -*- ecoding: utf-8 -*-
# @ModuleName: pandas_database.py
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2022/4/12
# @Desc:封装为pandas服务的mysql，mongodb常用操作
import pymongo
import sqlalchemy
import pandas as pd
import numpy as np




class PdMysql:
    """
        pandas专用的mysql封装
    """

    def __init__(self, host, port, user, password, dbname=None):

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        if dbname is None:
            self.engines = {}
        else:
            self.add_database(dbname)

    def add_database(self, dbname):
        """
            添加数据库
            :param dbname: 数据库名
            :return: None
        """
        self.engines[dbname] = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{dbname}")

    def read_sql(self, sql: str, database: str, ):
        """
        使用 pd.read_sql 读取数据库
        :param sql: SELECT语句
        :param database: 数据库表名
        :return:
        """
        try:
            if database not in self.engines:
                self.add_database(database)
            df = pd.read_sql(sql, self.engines[database])  # 读表
            print(f"读取成功.")
            return df
        except Exception as e:
            print(f"读取失败!!!!!!")
            raise e

    def create_table(self, df, table_name, db_name, char_set="utf8mb4", collate='utf8mb4_0900_ai_ci', primary_key=None,
                     sql_index=None):
        """
        创建表结构
        :param df: dataframe
        :param table_name: 表名
        :param db_name: 库名
        :param char_set: char_set字符集
        :param collate: collate排序
        :param primary_key: 主键
        :param sql_index: 索引，需传入列表
        :return: None  (执行成功会打印成功信息)
        """
        if df is None or isinstance(df, pd.DataFrame) is False:
            raise Exception('dataframe为None 或不是dataframe类型')
        if self.check_table(table_name, db_name):
            raise Exception(f'{table_name}表已存在')

        # 主键
        if primary_key:
            pk_sql = f', PRIMARY KEY (`{primary_key}`)'
        else:
            pk_sql = ''

        # 字段
        cols = self.__get_df_column_type(df)
        sql_list = []
        for field, field_type in cols:
            if primary_key and primary_key == field:
                sql_list.append(f"`{field}` {field_type} NOT NULL")
            else:
                sql_list.append(f"`{field}` {field_type} DEFAULT NULL")

        field_sql = ','.join(sql_list)

        # 索引
        if sql_index:
            sql_list = [f'KEY `idx_{field}` (`{field}`) USING BTREE' for field in sql_index]
            index_sql = ',' + ','.join(sql_list)
        else:
            index_sql = ''

        # 最终sql
        sql = f"""
        CREATE TABLE `{table_name}` (
          {field_sql}
          {pk_sql}
          {index_sql}
        ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET={char_set} COLLATE={collate}
        """.strip()
        try:
            self.engines[db_name].execute(sql)
        except Exception as e:
            print(f'创建{table_name}失败')
            raise e
        print(f'创建{table_name}成功')

    def to_sql(self, df, table_name, db_name, if_exists='append', chunksize=None, index=False, char_set="utf8mb4",
               collate='utf8mb4_0900_ai_ci', primary_key=None,
               sql_index=None):
        """
        插入数据
        :param df: 要插入数据的df
        :param table_name: 表名
        :param db_name: 库名
        :param if_exists: df.to_sql的if_exists，replace操作需要删除原表后重建表，否则会使得字段格式不合规范
        :param index: df索引，默认为false
        :param chunksize: int类型 ,分块
        :param char_set: char_set字符集
        :param collate: collate排序
        :param primary_key: 主键
        :param sql_index: 索引，需传入列表
        :return: None (成功会打印成功信息)
        """
        if db_name not in self.engines:
            self.add_database(db_name)

        if self.check_table(table_name, db_name) is False:
            self.create_table(df, table_name, db_name, char_set=char_set, collate=collate, primary_key=primary_key,
                              sql_index=sql_index)
        self.__update_col_type(df, table_name, db_name)
        df.to_sql(name=table_name, con=self.engines[db_name], chunksize=chunksize, if_exists=if_exists, index=index)
        if if_exists != 'append':
            self.__update_col_type(df, table_name, db_name)
        print('插入成功')

    def check_table(self, table_name, db_name):
        """
        检测表是否存在
        :param table_name: 表名
        :param table_name: 库名
        :return: bool ，true为存在,false为不存在
        """
        res = self.engines[db_name].execute(
            f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{db_name}' AND TABLE_NAME='{table_name}' ;").fetchall()
        if len(res) > 0:
            return True
        else:
            return False

    def get_db_column_type(self, table_name, db_name, col_name=None):
        """
        获取数据库里对应表的字段类型
        :param table_name:表名
        :param col_name:字段名
        :return: (字段类型,字段类型的值)
        """
        if col_name is None:
            sql = f"select data_type,character_maximum_length from information_schema.`columns` where table_schema = '{db_name}' and table_name = '{table_name}' "
        else:
            sql = f"select data_type,character_maximum_length from information_schema.`columns` where table_schema = '{db_name}' and table_name = '{table_name}' and COLUMN_name = '{col_name}'"

        res = self.engines[db_name].execute(sql).fetchall()
        if len(res) > 0:
            return res[0]
        else:
            raise Exception(f'获取数据库里对应表的字段类型失败,sql:{sql}')

    def __get_df_column_type(self, df):
        """
        根据df各列dtype和最大长度，判断创建表时的各字符长度
        :param df: dataframe
        :return: field,field_type  字段名和字段类型
        """
        res_list = []
        df.fillna('', inplace=True)
        for col, col_type in zip(df.columns, df.dtypes):
            if col_type == np.int64:
                res_list.append((col, 'int'))
            elif col_type == np.int32:
                res_list.append((col, 'int'))
            elif col_type == np.float32:
                res_list.append((col, 'float'))
            elif col_type == np.float64:
                res_list.append((col, 'float'))
            else:
                if df[col].str.len().max() <= 8:
                    res_list.append((col, 'varchar(8)'))
                elif df[col].str.len().max() <= 32:
                    res_list.append((col, 'varchar(32)'))
                elif df[col].str.len().max() <= 128:
                    res_list.append((col, 'varchar(128)'))
                elif df[col].str.len().max() <= 512:
                    res_list.append((col, 'varchar(512)'))
                elif df[col].str.len().max() <= 1024:
                    res_list.append((col, 'varchar(1024)'))
                elif df[col].str.len().max() <= 65535:
                    res_list.append((col, 'text'))
                else:
                    res_list.append((col, 'longtext'))
        return res_list

    def __check_col_type_issame(self, dtype, db_type):
        """
        检测df字段类型与db字段类型是否一致，一致返回true，否则返回false
        :param dtype:
        :param db_type:
        :return:
        """
        if dtype is np.dtype('O'):  # numpy object的表示
            if db_type in ['varchar', 'text', 'longtext']:
                return True
            else:
                return False
        elif dtype == np.int64:
            if db_type in ['int']:
                return True
            else:
                return False
        elif dtype == np.int32:
            if db_type in ['int']:
                return True
            else:
                return False
        elif dtype == np.float64:
            if db_type in ['float']:
                return True
            else:
                return False
        elif dtype == np.float32:
            if db_type in ['float']:
                return True
            else:
                return False
        else:
            print(dtype, '未知映射')
            return False

    def __update_col_type(self, df, table_name, db_name):
        """
        更新字段类型，如果df的字符串类型的字段最大长度超过数据库的字段长度，则动态更新
        :param df: dataframe
        :param table_name: 表名
        :return:
        """
        df.fillna('', inplace=True)  # dataframe的nan为float类型，所以得先fillna为字符串
        for col in df.columns:
            col_type, col_type_value = self.get_db_column_type(table_name, db_name, col)
            if self.__check_col_type_issame(df[col].dtype, col_type) is False:
                raise Exception(f'df字段类型与数据库中的字段类型不一致,column:{col},df:{df[col].dtype},db:{col_type}')
            if col_type == 'varchar':
                str_len = df[col].str.len().max()
                if col_type_value < str_len < 32:
                    new_type_value = 32
                    new_type = col_type
                elif col_type_value < str_len < 128:
                    new_type_value = 128
                    new_type = col_type
                elif col_type_value < str_len < 512:
                    new_type_value = 512
                    new_type = col_type
                elif col_type_value < str_len < 1024:
                    new_type_value = 1024
                    new_type = col_type
                elif col_type_value < str_len < 65535:
                    new_type_value = None
                    new_type = 'text'
                elif str_len > 65535:
                    new_type = 'longtext'
                    new_type_value = None
                else:  # 无更新
                    continue
                if new_type == 'varchar':
                    sql = f"alter  table `{table_name}` modify  column `{col}`  {new_type}({new_type_value})"
                else:
                    sql = f"alter  table `{table_name}` modify  column `{col}`  {new_type}"
                try:
                    self.engines[db_name].execute(sql)
                except Exception as e:
                    raise Exception(f'修改字段类型失败 -> {e}')
                print('修改成功', col, col_type, col_type_value, '->', new_type, new_type_value)


class PdMongoDB:
    """
    pandas专用的mongo封装
    """
    def __init__(self, uri='mongodb://localhost:27017/', db_name=None, collection_name=None):
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

    def insert(self, df):
        """插入多条数据

        :param df: dataframe
        :return: 添加的数据在库中的_id
        """


        documents = df.to_dict(orient='record')
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
        return pd.DataFrame(list(self.client[self.db_name][self.collection_name]))

    def find_batch_byList(self, field_list, field, db, batch_size=100):
        """
        分批在mongodb中提取field in field_list
        :param field_list: 字段范围列表
        :param field: 字段
        :param db: MongoDB的集合
        :param batch_size: 分批的大小
        :return: 
        """""
        list_length = len(field_list)
        iter_size = batch_size
        current = 0
        df = []
        while current < list_length:
            end = current + iter_size
            field_segment = field_list[current: end]
            result_cursor = db.find({field: {"$in": field_segment}})
            df.append(pd.DataFrame(list(result_cursor)))
            current = current + iter_size
        return pd.concat(df).reset_index(drop=True)


if __name__ == '__main__':
    # mongo
    db = PdMongoDB('xxx', 'aws_verifi',
                   'amz_special_vehicle')
    print(db)
    df = db.find({})
    print(df.head())

    # mysql
    mysql_db = PdMysql(host='xxx', port=3306, user='jason',
                       password='xxx')
    df2 = mysql_db.read_sql(sql='select * from amz_product_tree', database='清洗_亚马逊数据')
    print(df2)
