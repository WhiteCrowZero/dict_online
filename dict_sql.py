"""
在线词典 SQL
包含
    DictSQL 负责与数据库交互处理
"""
import pymysql


class DictSQL:
    def __init__(self, host='localhost', port=3306, user='root', password='123456', database='dbtest',
                 charset='utf8mb4'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                  database=self.database, charset=self.charset)
        self.cursor = self.db.cursor()
        print('连接数据库成功')

    def close(self):
        self.cursor.close()
        self.db.close()
