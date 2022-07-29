# -*- coding: UTF-8 -*-
# MySQL 物件化
import json
import pymysql
import datetime
from dbutils.pooled_db import PooledDB
import pymysql


class MysqlClient(object):
    __pool = None

    def __init__(self,
        mincached=10,
        maxcached=20,
        maxshared=10,
        maxconnections=200,
        blocking=True,
        maxusage=100,
        setsession=None,
        reset=True,
        host='127.0.0.1', port=3306, db='blogdb',
        user='root', passwd='12345678', charset='utf8mb4'):

        """
        :param mincached:空閒初始
        :param maxcached:空閒連接的最大数量
        :param maxshared:共享連接的最大数量
        :param maxconnections:創建連接池的最大数量
        :param blocking:超過最大連接數時，True等待連接數下降，为false直接報錯誤
        :param maxusage:單個連接的最大重複使用次數
        :param setsession:optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        :param reset:how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        :param host: ip
        :param port: 端口
        :param db: 資料庫
        :param user: 用户名
        :param passwd: 密码
        :param charset: 編碼
        """

        if not self.__pool:
            self.__class__.__pool = PooledDB(pymysql,
                                             mincached, maxcached,
                                             maxshared, maxconnections, blocking,
                                             maxusage, setsession, reset,
                                             host=host, port=port, db=db,
                                             user=user, passwd=passwd,
                                             charset=charset,
                                             cursorclass=pymysql.cursors.DictCursor
                                             )
        self._conn = None
        self._cursor = None
        self.__get_conn()

    def __get_conn(self):
        self._conn = self.__pool.connection();
        self._cursor = self._conn.cursor();

    def close(self):
        try:
            self._cursor.close()
            self._conn.close()
        except Exception as e:
            print (e)

    def __execute(self, sql, param=()):
        count = self._cursor.execute(sql, param)
        print (count)
        return count

    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        """ 字典 datatime -> str """
        if result_dict:
            result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime.datetime)}
            result_dict.update(result_replace)
        return result_dict

    def select_one(self, sql, param=()):
        """ 單結果 """
        count = self.__execute(sql, param)
        result = self._cursor.fetchone()
        """:type result:dict"""
        result = self.__dict_datetime_obj_to_str(result)
        return count, result

    def select_many(self, sql, param=()):
        """
        多節我
        param: sql参数
        """
        count = self.__execute(sql, param)
        result = self._cursor.fetchall()
        """:type result:list"""
        [self.__dict_datetime_obj_to_str(row_dict) for row_dict in result]
        return count, result

    def execute(self, sql, param=()):
        count = self.__execute(sql, param)
        return count

    def begin(self):
        self._conn.autocommit(0)

    def end(self, option='commit'):
        if option == 'commit':
            self._conn.autocommit()
        else:
            self._conn.rollback()


if __name__ == "__main__":
    mc = MysqlClient()
    sql1 = 'SELECT * FROM user  WHERE  id = 1'
    result1 = mc.select_one(sql1)
    print (json.dumps(result1[1], ensure_ascii=False))

    # sql2 = 'SELECT * FROM user  WHERE  id IN (%s,%s,%s)'
    # param = (2, 3, 4)
    # print (json.dumps(mc.select_many(sql2, param)[1], ensure_ascii=False))