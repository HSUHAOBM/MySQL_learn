# 連接池測試
import sys
import threading
import pymysql
import time

from dbutils.pooled_db import PooledDB

connargs = {
     "host":"localhost",
      "user":"root",
      "passwd":"12345678",
      "db":"blogdb"}

def test(conn):
    try:
        cursor = conn.cursor()
        count = cursor.execute("select * from user")
        rows = cursor.fetchall()
        for r in rows: pass
    finally:
        conn.close()
# not pool
def not_pool(num):
    for i in range(10):
        conn = pymysql.connect(**connargs)
        test(conn)
        print('第',num+1 ,'個子執行緒的第',i+1,'次連線')
        time.sleep(1)
# use pool
def pool(num):
    pooled = PooledDB(pymysql, **connargs)
    for i in range(10):
        conn = pooled.connection()
        test(conn)
        print('第', num + 1 ,'個子執行緒的第', i + 1,'次連線')

def main():
    t = not_pool if len(sys.argv) == 1 else pool

    for i in range(10):
        threading.Thread(target = t,args = (i,)).start() # 子執行緒

if __name__ == "__main__":
    main()


# time python ./connect_time_test_threading.py
# python ./connect_time_test_threading.py  23.91s user 19.02s system 170% cpu 25.198 total
# time python ./connect_time_test_threading.py -l
# python ./connect_time_test_threading.py -l  15.97s user 9.13s system 154% cpu 16.269 total