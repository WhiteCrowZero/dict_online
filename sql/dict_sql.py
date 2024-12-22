"""
在线词典 SQL
包含
    DictSQL 负责与数据库交互处理
"""
import pymysql

class DictSQL:
    def __init__(self, host='localhost', port=3306, user='root', password='123456', database='dict_online',
                 charset='utf8mb4'):
        self.kwargs = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': charset
        }
        self.db = pymysql.connect(**self.kwargs)
        self.cursor = self.db.cursor()
        print('连接数据库成功')

    def close(self):
        self.cursor.close()
        self.db.close()

    def login(self, name, password):
        sql = "select 1 from users where name = BINARY %s and password = %s"
        try:
            self.cursor.execute(sql, (name, password))
            self.db.commit()
            if self.cursor.fetchone():
                return True
            else:
                return False
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def register(self, name, password):
        sql = "insert into users(name, password) values (BINARY %s, %s)"
        try:
            self.cursor.execute(sql, (name, password))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def query(self, word):
        pass

    def history(self, name, word):
        pass


if __name__ == '__main__':
    sql = DictSQL()
    sql.close()
