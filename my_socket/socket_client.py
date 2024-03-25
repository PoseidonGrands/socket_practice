import socket

client = socket.socket()
client.connect(('192.168.0.101', 8000))

while True:
    # 给服务端发消息
    input_data = input()
    client.send(input_data.encode('utf-8'))


    # 监听服务端发来的消息
    server_data = client.recv(1024)
    print(f'server_data is {server_data}')
# client.close()