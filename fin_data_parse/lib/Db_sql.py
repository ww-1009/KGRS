#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
from pymysql.converters import escape_string
class Db:
    def __init__(self,db_name):
        self.connect = pymysql.connect(host='192.168.0.107',  # 本地数据库

                             user='root',  # 用户名

                             passwd='ww20011009',  # 数据库密码

                             db=db_name,  # 数据库名

                             charset='utf8')  # 数据库编码type_transitive_dbp_new
        self.cursor = self.connect.cursor()

    '''
        sql='insert ignore into relation (id_S, S, P, O, id_O) values (%s, %s, %s, %s, %s);'
        sql='insert ignore into entity (id, entity, imgUrl, relatedType, abstract) values (%s, %s, %s, %s, %s);'
        datas=[(...),(...)]
    '''
    def insert_ignore(self,sql,datas):
        try:
            self.cursor.executemany(sql, datas)
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()  # 发生错误时回滚
            print(e)

    def select(self,sql,*s):
        # SQL 查询语句
        if s!=():
            # s = escape_string(str(s))
            sql = sql % s
        try:
            # 执行SQL语句
            print(f"SQL语句为：{sql}")
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            print("数据查询成功")
            # 关闭数据库连接
            # self.connect.close()
            return results
        except:
            print("Error: unable to fetch data")


    # 关闭数据库连接
    def connect_close(self):
        self.connect.close()


if __name__ == '__main__':
    db=Db("FinancialDate")
    # print(db.select("SELECT *FROM relation WHERE id_O = '%s'",1546))
    # print(db.select("SELECT *FROM relation WHERE id_S = '%s'", 2))
    # print(db.select("SELECT entity FROM entity WHERE （imgUrl='',abstract = ''"))
    # db.cursor.execute("UPDATE entity SET abstract = '' WHERE abstract='\n'")

    results = db.select("SELECT id,entity FROM entity WHERE imgUrl='%s' and relatedType='%s' and abstract = '%s'",'','','')
