# -*- ecoding: utf-8 -*-
# @ModuleName: MySQL
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2021/4/29 16:11
# @Desc:

import pymysql


class MySQLClient:

    def __init__(self, host="127.0.0.1", port=3306, user="root", password="123456",
                 database="spider"):  # 构造函数
        self.conn = pymysql.connect(host=host,user=user,password=password,db=database,charset='utf8', port=port)
        self.cursor = self.conn.cursor()


    # 返回执行execute()方法后影响的行数

    def execute(self, sql):
        self.cursor.execute(sql)
        rowcount = self.cursor.rowcount
        return rowcount

    # 删除并返回影响行数
    def delete(self, **kwargs):
        table = kwargs['table']

        where = kwargs['where']
        sql = 'DELETE FROM %s where %s' % (table, where)
        print(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 影响的行数
            rowcount = self.cursor.rowcount
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            raise e
        return rowcount

    # 新增并返回新增ID
    def insert(self, **kwargs):
        table = kwargs['table']
        del kwargs['table']
        sql = 'insert into %s(' % table
        fields = ""
        values = ""
        for k, v in kwargs.items():
            fields += "%s," % k
            values += "'%s'," % v
        fields = fields.rstrip(',')
        values = values.rstrip(',')
        sql = sql + fields + ")values(" + values + ")"
        print(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 获取自增id
            res = self.cursor.lastrowid
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            raise e
        return res

    # 修改数据并返回影响的行数

    def update(self, **kwargs):
        table = kwargs['table']
        # del kwargs['table']
        kwargs.pop('table')
        where = kwargs['where']
        kwargs.pop('where')
        sql = 'update %s set ' % table
        for k, v in kwargs.items():
            sql += "%s='%s'," % (k, v)
        sql = sql.rstrip(',')
        sql += ' where %s' % where
        print(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 影响的行数
            rowcount = self.cursor.rowcount
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            raise e
        return rowcount

    # 查-一条条数据
    def selectTopone(self, **kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s limit 1' % (field, table, where, order)
        print(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.cursor.fetchone()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            raise e
        return data

    # 查所有数据
    def selectAll(self, **kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s ' % (field, table, where, order)
        print(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.cursor.fetchall()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            raise e
        return data

    def __del__(self):
        self.conn.close()



if __name__ == '__main__':

    conn = MySQLClient('139.159.204.92', 3306, 'root', 'zh1132', 'spider')

    # insert测试
    # cs = conn.insert(table="T1", Name="Python测试2", Sex="男")
    # print(cs)

    # delete 测试
    # cs = conn.delete(table="T1", where="Id = 2")
    # print(cs)

    # update 测试
    # cs = conn.update(table="T1", Name="Python测试3", Sex="man", where="Id in(1,2)")
    # print(cs)

    # select 测试
    cs = conn.selectAll(table="test")
    print(cs)