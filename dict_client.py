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

    # 处理登录和注册的统一函数
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

    # 处理登录
    def login(self, name, password):
        return self.__login_and_register(name, password, 'login')

    # 处理注册
    def register(self, name, password):
        return self.__login_and_register(name, password, 'register')

    # 处理单词查询
    def query(self, word):
        request_flag = self.flag_dict['query']
        request_data = self.name + ' ' + word
        request = request_flag + '\t' + request_data
        self.sock.send(request.encode())

        msg = self.sock.recv(1024).decode()
        if msg == 'F':
            return False
        else:
            mean = msg.split('\t')[1]
            return mean

    # 处理历史记录查询
    def history(self):
        request_flag = self.flag_dict['history']
        request_data = self.name
        request = request_flag + '\t' + request_data
        self.sock.send(request.encode())

        msg = self.sock.recv(1024).decode()
        if msg == 'F':
            return False
        else:
            history_info = msg.split('\t',1)[1].strip()
            return history_info

    # 处理客户端退出
    def close(self):
        request_flag = self.flag_dict['exit'].encode()
        self.sock.send(request_flag)
        self.sock.close()
        print("Client close")

    # 处理密码加密
    def __sha256_encrypt(self, password):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password.encode('utf-8'))
        return sha256_hash.hexdigest()


class ClientView:

    def __init__(self):
        self.__handle = Handle()

    # 视图1，未登录前
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

    # 视图2，已登录后
    def __View2(self):
        while True:
            print("""
            ============= Query ===========
             1. 查单词   2. 历史记录   3.注销
            ================================
                """)
            choice = input("请输入选项：")

            if choice == '1':
                while True:
                    word = input('请输入要查询的单词（输入 ## 退出）：')
                    if word == '##':
                        break
                    mean = self.__handle.query(word)
                    if mean:
                        print('单词解释：', mean)
                    else:
                        print('查询失败！')

            elif choice == '2':
                history_info = self.__handle.history()
                if history_info:
                    print('历史记录：')
                    print(history_info)
                else:
                    print('查询失败！')

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
