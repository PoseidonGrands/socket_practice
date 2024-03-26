import socket
import json

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

# 初始化线程池
t = ThreadPoolExecutor(5)

# 维护用户连接，数据格式为：{user:xxx, sock:xxx}
online_users = defaultdict(dict)
# 维护用户历史消息
user_msgs = defaultdict(list)


def sock_handle(_sock, _addr):
    # 连接建立后持续接受消息（不是一次性接收消息后就断开连接，而是持续的通信，所以发送消息给client后不需要关闭sock
    while True:
        # 接收的是json数据,接收的数据格式:{action:xx ,user:xx}
        json_data = _sock.recv(1024)
        data = json.loads(json_data.decode('utf-8'))
        action = data.get('action', '')
        user = data.get('user', '')
        # 根据用户请求进行操作
        if action == 'login':
            # 登录请求：保存连接
            online_users[user] = _sock
            _sock.send('login success...'.encode('utf-8'))
        elif action == 'list_user':
            users = [user for user, sock in online_users.items()]
            _sock.send(json.dumps(users).encode('utf-8'))
        elif action == 'history_msg':
            # 获取发起请求的用户的历史消息
            _sock.send(json.dumps(user_msgs.get(data['user'], '')).encode('utf-8'))
        elif action == 'send_msg':
            # 只能给在线用户发消息？
            # 拿到需发送对象的连接对象并把消息转发
            to_user = data.get('to')
            if to_user in online_users:
                online_users[to_user].send(json.dumps(data).encode('utf-8'))
            # 发送离线消息不需要对方在线
            user_msgs[to_user].append(data)
        elif action == 'exit':
            online_users.pop(data.get('user'), '')
            _sock.send('exit success...'.encode('utf-8'))


if __name__ == '__main__':
    server = socket.socket()

    server.bind(('0.0.0.0', 8000))
    server.listen()

    while True:
        # 等待客户端连接
        sock, addr = server.accept()
        t.submit(sock_handle, sock, addr)