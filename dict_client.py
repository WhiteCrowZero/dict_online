"""
在线词典 客户端
包含
    ClientView
        View1 界面（登录、注册、退出）
        View2 界面（查询、历史、注销）
    Handle 逻辑处理，负责给服务端发送请求
"""
from socket import *

class Handle:
    ADDR = ('127.0.0.1', 8888)

    def __init__(self):
        self.sock = self._create_sock()

    def _create_sock(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(self.ADDR)
        return sock

    def main(self):
        self.sock.send(b'c test')
        msg = self.sock.recv(1024)
        print(msg.decode())

class ClientView:

    def __init__(self):
        self.__handle = Handle()

    def View1(self):
        while True:
            print(
                """
                
                """
            )

    def View2(self):
        pass

    def main(self):
        self.__handle.main()

if __name__ == '__main__':
    c = ClientView()
    c.main()