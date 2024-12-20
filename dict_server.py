"""
在线词典 服务端
包含
    WebServer 处理客户端的请求，并发送响应
    Handle 负责实现具体的处理逻辑，与SQL交互
"""
from socket import *
from dict_sql import *
from multiprocessing import Process


class Handle:
    def __init__(self):
        self.db = DictSQL()


class WebServer(Process):
    def __init__(self, host='', port=0):
        super().__init__()
        self.HOST = host
        self.PORT = port
        self.ADDR = (host, port)
        self.sock = self._create_socket()
        self.__handle = Handle()

    def _create_socket(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(self.ADDR)
        sock.listen(5)
        return sock

    def run(self):
        conn, addr = self.sock.accept()
        while True:
            msg = conn.recv(1024)
            print(msg.decode())
            conn.send(b'test')


if __name__ == '__main__':
    s = WebServer('127.0.0.1', 8888)
    s.run()
