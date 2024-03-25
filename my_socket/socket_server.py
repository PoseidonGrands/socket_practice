import socket

from concurrent.futures import ThreadPoolExecutor


t = ThreadPoolExecutor(5)

# 默认是tcp协议
server = socket.socket()
server.bind(('0.0.0.0', 8000))
server.listen()


# 对每个请求的处理
def handle_sock(_sock, addr):
    data = ""
    while True:
        tmp_data = _sock.recv(1024)

        # 发送一段信息给客户端
        server_msg = 'server is received...'.encode('utf-8')
        _sock.send(server_msg)

        if tmp_data:
            data += tmp_data.decode('utf-8')
            print(f'client send message:{tmp_data.decode("utf-8")}')
            if "#" in tmp_data.decode('utf-8'):
                break
        else:
            break
    print(data)


# 不断接受客户端请求，并新开线程处理
while True:
    # server负责接受连接请求，sock负责具体的数据传输，而addr则提供了客户端的地址信息（ip、端口
    # 阻塞方法，如果客户端close服务端会接收并取消阻塞
    sock, addr = server.accept()
    print('client is connected...')
    t.submit(handle_sock, sock, addr)


# sock.close()




