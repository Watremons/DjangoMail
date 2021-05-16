import socket


if __name__ == "__main__":
    client = socket.socket()
    pop3_ip_port = ('127.0.0.1', 8110)
    smtp_ip_port = ('127.0.0.1', 8025)
    
    username = 'bossq'
    password = '123456'

    client.connect(pop3_ip_port)
    data = client.recv(1024)
    # print(data.decode())
    user_cmd = 'USER ' + username + '\r\n'
    client.send(user_cmd.encode())
    data = client.recv(1024)
    # print(data.decode())
    pass_cmd = 'PASS ' + password + '\r\n'
    client.send(pass_cmd.encode())
    data = client.recv(1024)
    # print(data.decode())
    list_cmd = 'LIST\r\n'
    client.send(list_cmd.encode())
    data = client.recv(1024).decode()
    print(type(data), data)
    mail_list = data.split('\r\n')[1:-2]
    print(mail_list)

    mail_json_list = []
    for mail in mail_list:
        
        retr_cmd = 'RETR ' + mail.split()[0] + '\r\n'
        client.send(retr_cmd.encode())
        mail_detail = client.recv(1024).decode()
        mail_item = mail_detail.split('\r\n')[1:-2]

        mail_dict = {}
        mail_dict['mailNo'] = int(mail.split()[0])
        mail_dict['sender'] = mail_item[1].split()[1]
        mail_dict['subject'] = mail_item[3].split()[1]
        mail_dict['isRead'] = 0
        mail_json_list.append(mail_dict)
    print(mail_json_list)


    