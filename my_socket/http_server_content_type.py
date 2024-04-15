import socket

from concurrent.futures import ThreadPoolExecutor


t = ThreadPoolExecutor(5)

# 默认是tcp协议
server = socket.socket()
server.bind(('0.0.0.0', 8003))
server.listen()


# 对每个请求的处理
def handle_sock(_sock, addr):
    data = ""
    while True:
        tmp_data_json = _sock.recv(1024)
        tmp_data = tmp_data_json.decode('utf-8')
        print(tmp_data)
        # 解析出请求方式和路径
        method = tmp_data.split(' ')[0]
        path = tmp_data.split(' ')[1]
        if method == 'GET':
            # http响应
            response_template = '''HTTP/1.1 200 OK
Set-Cookie: name=sewellhe
Set-Cookie: course_id=213
Set-Cookie: session_id=12312312312

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
</head>
<body>
    <h2>Login Form</h2>
    <form action="/" method="GET">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br><br>
        
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br><br>
        
        <input type="submit" value="Login">
    </form>
</body>
</html>

'''
            # 本身是字符串，无需json.dumps转字符串
            _sock.send(response_template.encode('utf-8'))
            _sock.close()
        elif method == 'POST':
            response_template = '''HTTP/1.1 200 OK

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login Form</title>
</head>
<body>
<h2>Login Form</h2>
<form action="/" method="POST" enctype="multipart/form-data">
    <input type="text" id="username" name="username"><br><br>
    <input type="password" id="password" name="password"><br><br>
    <input type="submit" value="Login">
</form>
</body>
</html>

'''
            # 本身是字符串，无需json.dumps转字符串
            _sock.send(response_template.encode('utf-8'))
            _sock.close()


# 不断接受客户端请求，并新开线程处理
while True:
    # server负责接受连接请求，sock负责具体的数据传输，而addr则提供了客户端的地址信息（ip、端口
    # 阻塞方法，如果客户端close服务端会接收并取消阻塞
    sock, addr = server.accept()
    print('client is connected...')
    t.submit(handle_sock, sock, addr)


# sock.close()




