# MySQL 增加連接池
from dbutils.pooled_db import PooledDB
import pymysql

# 資料庫設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "blogdb",
    "charset": "utf8"
}
try:
    pool = PooledDB(
        pymysql,
        mincached=10,
        maxcached=20,
        maxshared=10,
        maxconnections=200,
        blocking=True,
        maxusage=100,
        setsession=None,
        reset=True,
        host='localhost',
        port=3306,
        user='root',
        passwd='12345678',
        db='blogdb',
        )

    # 建立Connection物件
    conn = pool.connection()
    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 查詢資料SQL語法
        command = "SELECT * FROM user"
        # 執行指令
        cursor.execute(command)
        # 取得所有資料
        result = cursor.fetchall()
        print(result)
except Exception as ex:
    print(ex)