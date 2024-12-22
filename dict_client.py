"""
在线词典 客户端
包含
    ClientView
        View1 界面（登录、注册、退出）
        View2 界面（查询、历史、注销）
    Handle 逻辑处理，负责给服务端发送请求
"""
import hashlib
import sys
from socket import *


class Handle:
    ADDR = ('127.0.0.1', 8888)
    # 自己拟订的通信协议的标识符
    flag_dict = {
        'login': 'L',
        'register': 'R',
        'query': 'Q',
        'history': 'H',
        'exit': 'E'
    }

    def __init__(self):
        self.sock = self._create_sock()
        self.name = ''

    def _create_sock(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(self.ADDR)
        print("Client is OK")
        return sock

    def __login_and_register(self, name, password, mode):
        self.name = name

        request_flag = self.flag_dict[mode]
        password = self.__sha256_encrypt(password)
        request_data = name + ' ' + password
        request = request_flag + '\t' + request_data
        self.sock.send(request.encode())

        msg = self.sock.recv(128).decode()
        if msg == 'T':
            return True
        else:
            return False

    def login(self, name, password):
        return self.__login_and_register(name, password, 'login')

    def register(self, name, password):
        return self.__login_and_register(name, password, 'register')

    def query(self, word):
        pass

    def history(self):
        pass

    def close(self):
        self.sock.send(b'E')
        self.sock.close()
        print("Client close")

    def __sha256_encrypt(self, password):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password.encode('utf-8'))
        return sha256_hash.hexdigest()


class ClientView:

    def __init__(self):
        self.__handle = Handle()

    def __View1(self):
        while True:
            print("""
            ========== Welcome =========
             1. 登录   2. 注册   3.退出
            ============================
                """)
            choice = input("请输入选项：")

            if choice == '1':
                name = input('请输入昵称：')
                password = input('请输入密码：')
                if self.__handle.login(name, password):
                    print('登录成功！')
                    self.__View2()
                else:
                    print('登录失败！')

            elif choice == '2':
                name = input('请输入昵称：')
                password = input('请输入密码：')
                if self.__handle.register(name, password):
                    print('注册成功！')
                    self.__View2()
                else:
                    print('注册失败！')

            elif choice == '3':
                sys.exit('感谢使用')
            else:
                print('输入有误，请重新输入！')

    def __View2(self):
        while True:
            print("""
            ============= Query ===========
             1. 查单词   2. 历史记录   3.注销
            ================================
                """)
            choice = input("请输入选项：")
            if choice == '1':
                word = input('请输入要查询的单词：')
                self.__handle.query(word)
            elif choice == '2':
                self.__handle.history()
            elif choice == '3':
                self.__handle.close()
                break
            else:
                print('输入有误，请重新输入！')

    def main(self):
        self.__View1()


if __name__ == '__main__':
    c = ClientView()
    c.main()

