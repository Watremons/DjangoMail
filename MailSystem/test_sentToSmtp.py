import socket


if __name__ == "__main__":
    client = socket.socket()
    pop3_ip_port = ('127.0.0.1', 8110)
    smtp_ip_port = ('127.0.0.1', 8025)
    
    username = 'bossq@test.com'
    password = '123456'
    subject = '你困吗'
    content = '你这个年龄段，你这个阶段睡得着觉？有点出息没有'
    recever = 'David@test.com'

    client.connect(smtp_ip_port)
    data = client.recv(1024)
    print(data.decode())

    ehlo_cmd = 'ehlo ' + username + '\r\n'
    client.send(ehlo_cmd.encode())
    data = client.recv(1024)
    print(data.decode())


    login_cmd = 'auth login\r\n'
    client.send(login_cmd.encode())
    data = client.recv(1024)
    login_cmd = username + '\r\n'
    client.send(login_cmd.encode())
    data = client.recv(1024)
    login_cmd = password + '\r\n'
    client.send(login_cmd.encode())
    data = client.recv(1024)
    print(data.decode())

    mailfrom_cmd = 'mail from:<' + username + '>\r\n'
    client.send(mailfrom_cmd.encode())
    data = client.recv(1024)
    print(data.decode())

    rcptto_cmd = 'rcpt to:<' + recever + '>\r\n'
    client.send(rcptto_cmd.encode())
    data = client.recv(1024)
    print(data.decode())

    data_cmd = 'data\r\n'
    client.send(data_cmd.encode())
    data = client.recv(1024)

    content = subject + '\r\n' + content + '\r\n\r\n.'
    content_list = content.split('\r\n')
    print(content_list)
    for line in content_list:
        line = line + '\r\n'
        client.send(line.encode())

    data = client.recv(1024).decode()
    print(data)




    