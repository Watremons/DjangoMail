import socket


if __name__ == "__main__":
    client = socket.socket()
    pop3_ip_port = ('127.0.0.1', 8110)
    smtp_ip_port = ('127.0.0.1', 8025)
    

    while True:
        server = input("Input the test server (smtp or pop3):")
        if server.strip() == 'exit':
            client.shutdown(2)
            client.close()
            break
        elif server.strip() == 'smtp':
            client.connect(smtp_ip_port)
        else:
            client.connect(pop3_ip_port)
        while True:

            data = client.recv(1024)
            print(data.decode())

            msg_input = input("Input the message:") + "\r\n"
            dataStr = data.decode()
            if dataStr.find("354 End data with <CR><LF>.<CR><LF>") != -1:
                # print("arrive if")
                while msg_input[-5:] != "\r\n.\r\n":
                    # print("IN WHILE")
                    msg_input = msg_input + input("Input the message:") + "\r\n"

            if msg_input == '':
                continue
            if msg_input == 'exit':
                break
            client.send(msg_input.encode())
            

            client.send(msg_input.encode())
