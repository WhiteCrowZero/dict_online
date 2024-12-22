"""
在线词典 服务端
包含
    WebServer 处理客户端的请求，并发送响应
    Handle 负责实现具体的处理逻辑，与SQL交互
"""
from socket import *
from month2_code.dict_online.sql.dict_sql import DictSQL
from multiprocessing import Process


class Handle(Process):
    # 自己拟订的通信协议的标识符
    flag_dict = {
        'login': 'L',
        'register': 'R',
        'query': 'Q',
        'history': 'H',
        'exit': 'E'
    }

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.db = None

    def run(self):
        self.db = DictSQL()

        while True:
            msg = self.conn.recv(1024).decode().strip()
            if msg == self.flag_dict['exit']:
                self.conn.close()
                self.db.close()
                break

            request_flag, request_data = msg.split('\t', 1)
            if request_flag == self.flag_dict['login']:
                name, pwd = request_data.split(' ')
                self.login(name, pwd)
            elif request_flag == self.flag_dict['register']:
                name, pwd = request_data.split(' ')
                self.register(name, pwd)
            elif request_flag == self.flag_dict['query']:
                name, word = request_data.split(' ')
                self.query(name, word)
            elif request_flag == self.flag_dict['history']:
                name = request_data
                self.history(name)


    def login(self, name, pwd):
        res = self.db.login(name, pwd)
        if res:
            self.conn.send(b'T')
        else:
            self.conn.send(b'F')

    def register(self, name, pwd):
        res = self.db.register(name, pwd)
        if res:
            self.conn.send(b'T')
        else:
            self.conn.send(b'F')


class WebServer(Process):
    def __init__(self, host='', port=0):
        super().__init__()
        self.HOST = host
        self.PORT = port
        self.ADDR = (host, port)
        self.sock = self._create_socket()

    def _create_socket(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(self.ADDR)
        return sock

    def serve_forever(self):
        self.sock.listen(5)
        print(f'Server start on {self.ADDR}\nWait for connect...')

        while True:
            try:
                conn, addr = self.sock.accept()
                print('Connect from', addr)
            except KeyboardInterrupt:
                print('Server exit...')
                break
            except Exception as e:
                print(e)
                continue
            # 创建一个线程单独处理一个客户端
            handle = Handle(conn)
            handle.daemon = True
            handle.start()


if __name__ == '__main__':
    s = WebServer('127.0.0.1', 8888)
    s.serve_forever()
