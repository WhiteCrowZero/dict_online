import pymysql
import re

# 连接数据库
setting = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'dict_online',
    'charset': 'utf8'
}
db = pymysql.connect(**setting)
cursor = db.cursor()
print('连接数据库成功')

# 插入语句
sql = 'insert into words(word,mean) values (%s,%s)'

# 读取文件并插入
with open('data/dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        data = re.findall(r'(\w+)\s+(.*)', line)[0]
        word, mean = data
        try:
            cursor.execute(sql, (word, mean))
            db.commit()
            print(f'插入{word}成功')
        except Exception as e:
            print(f'插入{word}失败')
            db.rollback()
print('插入数据完成')
