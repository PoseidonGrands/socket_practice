import json
import socket

from concurrent.futures import ThreadPoolExecutor

t = ThreadPoolExecutor(5)

user = 'monkey'
# 定义数据发送格式
login_command = {
    'action': 'login',
    'user': user
}

get_user_command = {
    'action': 'list_user'
}

offline_msg_command = {
    'action': 'history_msg',
    'user': user
}

send_data_command = {
    'action': 'send_msg',
    'from': user,
    'to': '',
    'data': ''
}

exit_command = {
    'action': 'exit',
    'user': user
}

is_exit = False


def handle_send():
    while True:
        op_type = input('请输入你的操作：1、发送消息 2、获取在线人数 3、退出')
        if op_type not in ('1', '2', '3'):
            continue
        else:
            if op_type == '1':
                to_user = input('请输入你要发送的用户：')
                data = input('请输入你的消息：')
                send_data_command['to'] = to_user
                send_data_command['data'] = data
                client.send(json.dumps(send_data_command).encode('utf-8'))
            elif op_type == '2':
                client.send(json.dumps(get_user_command).encode('utf-8'))
            elif op_type == '3':
                client.send(json.dumps(exit_command).encode('utf-8'))
                # 用户退出了客户端的连接也要关闭
                client.close()
                global is_exit
                is_exit = True
                break


def handle_recv():
    while True:
        if not is_exit:
            try:
                # 当客户端关闭连接后此方法会抛出异常
                res_json = client.recv(1024).decode('utf-8')
            except:
                break
            try:
                # 当解析的数据不是json数据（单纯的字符串）会抛出异常
                _res = json.loads(res_json)
                msg = _res['data']
                from_user = _res['from']
                print(f'\n收到了来自{from_user}的消息：{msg}')
            except:
                print(f'\n消息{res_json}')
        else:
            break


if __name__ == '__main__':
    client = socket.socket()
    client.connect(('127.0.0.1', 8000))

    # 这三步不会被阻塞是因为发送请求后确定服务端会马上回传消息
    # 1、登录
    client.send(json.dumps(login_command).encode('utf-8'))
    res = client.recv(1024).decode('utf-8')
    print(res)

    # 2、获取在线人数
    client.send(json.dumps(get_user_command).encode('utf-8'))
    res = client.recv(1024).decode('utf-8')
    print(f'在线人数：{res}')

    # 3、获取历史消息
    client.send(json.dumps(offline_msg_command).encode('utf-8'))
    res = client.recv(1024).decode('utf-8')
    print(f'历史消息：{res}')

    t.submit(handle_send)
    t.submit(handle_recv)

