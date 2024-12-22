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

    # 处理关闭
    def close(self):
        self.cursor.close()
        self.db.close()

    # 处理登录
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

    # 处理注册
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

    # 处理单词查询
    def query(self, word):
        sql = "select mean from words where word = %s"
        try:
            self.cursor.execute(sql, (word,))
            self.db.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    # 处理历史记录查询
    def history(self, name):
        # 注意分行之后每一行后面的空格，缺少这些空格会导致语句粘连在一起，导致报错
        sql = ('select word, mean, `time` from words w '
               'left join history h on w.id = h.id '
               'where h.users_id in '
               '(select u.id from users u where name = %s) '
               'order by h.time desc '
               'limit 10')
        try:
            self.cursor.execute(sql, (name,))
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False


    # 处理添加历史记录
    def add_history(self, name, word):
        try:
            sql = 'select id from users where name = %s'
            self.cursor.execute(sql, (name,))
            self.db.commit()
            user_id = self.cursor.fetchone()[0]

            sql = 'select id from words where word = %s'
            self.cursor.execute(sql, (word,))
            self.db.commit()
            word_id = self.cursor.fetchone()[0]

            sql = 'insert into history(users_id, words_id) values (%s, %s)'
            self.cursor.execute(sql, (user_id, word_id))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False


if __name__ == '__main__':
    sql = DictSQL()
    sql.close()
