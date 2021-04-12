from mysql import sqlHandle
import socket
import time
import os
# import signal
import threading
import re
import datetime

selfMailDomain = 'test.com'
otherMailDomain = 'other.com'
otherIP = '127.0.0.1'
otherPort = 8111


class Pop3:
    STOPPED = 0
    RUNNING = 1
    LISTENING = False

    state = STOPPED
    server = None
    connection = None

    maxClient = 10

    def __init__(self, port=8110, logDir='/log/pop3', banIPs=[], banActs=[], maxSize=65545):
        self.ip = '0.0.0.0'
        self.port = port
        self.logDir = logDir
        self.banIPs = banIPs
        self.banActs = banActs
        self.maxSize = maxSize
        # signal.signal(signal.SIGINT, self.signalHandler)

    def start(self):
        if self.state == self.RUNNING:
            print('start pop3 server passed, pop3 server is running')
            return True

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.ip, self.port))
            self.server.listen(self.maxClient)

        except:
            self.state = self.STOPPED
            print('start pop3 server failed, error')
            return False
        else:
            self.state = self.RUNNING
            self.LISTENING = True
            self.connection = None
            print('pop3 server started.')
            print('pop3 server is listening at port ' + str(self.port))
            t = threading.Thread(target=self.listen)
            t.start()

            try:
                now = datetime.datetime.now()
                now = now.strftime("%Y-%m-%d-%H:%M:%S").replace(":", "_")
                fileDir = os.path.abspath(os.path.dirname(__file__)) + self.logDir
                if not os.path.exists(fileDir):
                    os.makedirs(fileDir)
                os.chdir(fileDir)
                fileName = 'pop3-log-' + now + '.log'
                self.log = open(fileName, 'w')
            except:
                print('make log file failed')
                self.log = None
            else:
                self.log.write('pop3 start at ' + now + '\n')

            return True

    def stop(self):
        if self.state == self.STOPPED:
            print('stop pop3 server passed, pop3 server is stopped')
            return True

        try:
            self.LISTENING = False
            time.sleep(1)
            if self.connection is not None:
                self.connection.close()
                print('connection close!')
            self.server.close()

            if self.log is not None:
                now = datetime.datetime.now()
                now = now.strftime("%Y-%m-%d-%H:%M:%S")
                self.log.write('pop3 stop at ' + now + '\n')
                self.log.close()

        except:
            self.state = self.RUNNING
            print('stop pop3 server failed, error')
            return False
        else:
            self.state = self.STOPPED
            print('pop3 server stopped.')
            return True

    def restart(self):
        self.stop()
        self.start()

    def helpInfo(self):
        print('here is help info')
        pass

    def setMaxClient(self, maxClient_):
        self.maxClient = maxClient_
        print('max client number set successfully, the server is restarting...')
        self.restart()

    def authentication(self, username, password):
        try:
            results = sqlHandle(
                'Users', 'SELECT',
                'userNo, userPassword',
                'userName = \'' + username + '\''
                )
        except:
            return False, -1
        else:
            if len(results) == 0:
                return False, -1

            if password == results[0][1]:
                return True, results[0][0]
            else:
                return False, -1

    def listen(self):
        if self.LISTENING is True:
            t = threading.Thread(target=self.pop3Server, daemon=True)
            t.start()

        while True:
            if self.LISTENING is False:
                print('listen stop')
                break

    def pop3Server(self):
        while True:
            try:
                connection, address = self.server.accept()
                if address[0] in self.banIPs:
                    connection.close()
                    continue

                self.connection = connection
            except:
                print('the connection is closed')
                break

            thread = threading.Thread(target=self.clientConn, args=(connection, address), daemon=True)
            thread.start()

            if self.log is not None:
                now = datetime.datetime.now()
                now = now.strftime("%Y-%m-%d-%H:%M:%S")
                self.log.write('connection from (' + address[0] + ',' + str(address[1]) + ') at ' + now + '\n')

        if self.connection is not None:
            self.connection.close()

    def getEmail(self, username):
        allMails = sqlHandle(
            'Mails', 'SELECT',
            '*',
            'userName = \'' + str(username) + '\'' +
            'ORDER BY time DESC'
            )
        mailsSize = []
        mailSize = 0
        mails = []
        overSize = False
        deleMails = []
        print(allMails)

        if allMails:
            for mail in allMails:
                print('?')
                if mail[5] == 0 and mail[6] == 1:

                    if overSize is True:
                        deleMails.append(mail)
                        continue

                    if mailSize + len(mail[5].encode('utf-8')) > self.maxSize:
                        overSize = True
                        deleMails.append(mail)

                    else:
                        if mail[4] not in self.banActs and mail[0] not in self.banActs:
                            mailSize = mailSize + len(mail[6].encode('utf-8'))
                            mailsSize.append(len(mail[6].encode('utf-8')))
                            mails.append(mail)

        t = threading.Thread(target=self.delEmail, args=(deleMails, range(len(deleMails))))
        t.start()

        return len(mails), mails, mailSize, mailsSize

    def delEmail(self, mails, deles):
        if deles and mails:
            for dele in deles:
                sqlHandle(
                    'recvmail', 'UPDATE',
                    'isRead = \'' + '1' + '\'',
                    'mailNo = \'' + str(mails[dele][0]) + '\'')

    def clientConn(self, connection, address):
        mailsNum = 0
        mails = ()
        mailSize = 0
        mailsSize = []
        deles = []
        message = '+OK Welcome to localhost Example Mail System Pop3 Server (EMS(20210420))\r\n'
        connection.send(message.encode('utf-8'))

        state = 'AUTH_LOGIN'
        while True:
            try:
                message = connection.recv(1024)
            except:
                print('the connection is closed')
                break
            else:
                try:
                    data = message.decode('utf-8')[0:-2]

                    if self.log is not None:
                        now = datetime.datetime.now()
                        now = now.strftime("%Y-%m-%d-%H:%M:%S")
                        self.log.write(
                            'smtp get \'' + data +
                            '\' at ' + now +
                            ' from (' + address[0] + ', ' + str(address[1]) + ')\n'
                            )

                    if data[0:4].lower() == 'noop':
                        message = '+OK example mail\r\n'
                        connection.send(message.encode('utf-8'))
                        continue

                    if state == 'AUTH_LOGIN':
                        if re.match(r'[uU][sS][eE][rR]\s+\S+', data):
                            valid = re.search(r'\S+', data[4:])
                            if valid is not None:
                                username = valid.group()
                                state = 'AUTH_USER'
                                message = '+OK example mail\r\n'

                        elif data[0:4].lower() == 'quit':
                            message = '+OK example mail\r\n'
                            connection.send(message.encode('utf-8'))
                            state = 'HANDLE'
                            break

                        elif re.match(r'pass\s\S+', data) is not None:
                            message = '-ERR Command not valid in this state\r\n'

                        else:
                            message = '-ERR Unknown command ' + data + '\r\n'

                        connection.send(message.encode('utf-8'))

                    elif state == 'AUTH_USER':
                        if re.match(r'[pP][aA][sS][sS]\s+\S+', data):
                            valid = re.search(r'\S+', data[4:])
                            if valid is not None:
                                password = valid.group()
                                auth, userNo = self.authentication(username, password)
                                if auth is True:
                                    state = 'AUTH_AFTER'
                                    mailsNum, mails, mailSize, mailsSize = self.getEmail(username)
                                    message = '+OK ' + str(mailsNum) + ' message(s) [' + str(mailSize) + ' byte(s)]\r\n'
                                else:
                                    message = '-ERR Unable to log on\r\n'

                        elif data[0:4].lower() == 'quit':
                            message = '+OK example mail\r\n'
                            connection.send(message.encode('utf-8'))
                            state = 'HANDLE'
                            break

                        elif re.match(r'[uU][sS][eE][rR]\s+\S+', data):
                            valid = re.search(r'\S+', data[4:])
                            if valid is not None:
                                username = valid.group()
                                message = '+OK example mail\r\n'

                        else:
                            message = '-ERR Unknown command ' + data + '\r\n'

                        connection.send(message.encode('utf-8'))

                    elif state == 'AUTH_AFTER':
                        if re.match(r'[sS][tT][aA][tT]\s*', data):
                            message = '+OK ' + str(mailsNum) + ' ' + str(mailSize) + '\r\n'

                        elif re.match(r'[lL][iI][sS][tT]\s*\d*', data):
                            valid = re.search(r'\d+', data[4:])
                            if valid is None:
                                message = '+OK ' + str(mailsNum) + ' ' + str(mailSize) + '\r\n'
                                for i in range(mailsNum):
                                    message = message + str(i + 1) + ' ' + str(mailsSize[i]) + '\r\n'
                                message = message + '.\r\n'
                            else:
                                number = int(valid.group())
                                if (number > mailsNum):
                                    message = '-Error Unknown message\r\n'
                                else:
                                    message = str(number) + ' ' + str(mailsSize[number - 1]) + '\r\n'

                        elif re.match(r'[rR][eE][tT][rR]\s*\d*', data):
                            valid = re.search(r'\d+', data[4:])
                            if valid is None:
                                message = '-Error Unknown message\r\n'
                            else:
                                number = int(valid.group())
                                if (number > mailsNum):
                                    message = '-Error Unknown message\r\n'
                                else:
                                    mail = mails[number - 1]
                                    print(mail)
                                    message = '+OK ' + str(number) + ' ' + str(mailsSize[number - 1]) + ' octets\r\n'
                                    message = message + 'Received: from ' + mail[2] + '(' + mail[3] + ')\r\n'
                                    message = message + '        ' + str(mail[7]) + '\r\n'
                                    message = message + 'From:<' + mail[4] + '>\r\n'
                                    message = message + 'To:<' + mail[5] + '>\r\n'
                                    message = message + 'Date:' + str(mail[7]) + '\r\n'
                                    message = message + mail[6]
                                    message = message + '\r\n.\r\n'
                                    print(message)

                        elif re.match(r'[uU][iI][dD][lL]\s*\d*', data):
                            valid = re.search(r'\d+', data[4:])
                            if valid is None:
                                message = '-Error Unknown message\r\n'
                            else:
                                number = int(valid.group())
                                if (number > mailsNum):
                                    message = '-Error Unknown message\r\n'
                                else:
                                    mailID = mails[number - 1][0]
                                    print(mailID)
                                    message = '+OK ' + mailID + '\r\n'
                                    print(message)

                        elif re.match(r'[dD][eE][lL][eE]\s*\d*', data):
                            valid = re.search(r'\d+', data[4:])
                            if valid is None:
                                message = '-Error Unknown message\r\n'
                            else:
                                number = int(valid.group())
                                if number > mailsNum or number <= 0:
                                    message = '-Error Unknown message\r\n'
                                else:
                                    if number not in deles:
                                        deles.append(number)
                                    message = '+OK ' + str(number) + ' delete\r\n'
                                    print(message)

                        elif data[0:4].lower() == 'rest':
                            deles.clear()
                            message = '+OK delete mails cancled\r\n'

                        elif re.match(r'[rR][eE][sS][tt]\s*', data):
                            valid = re.search(r'\d+', data[4:])
                            if valid is None:
                                message = '-Error Unknown message\r\n'
                            else:
                                deles.clear()
                                message = '+OK delete cancelld\r\n'

                        elif data[0:4].lower() == 'quit':
                            message = '+OK example mail\r\n'
                            state = 'HANDLE'
                            break

                        connection.send(message.encode('utf-8'))

                except:
                    print('connection lost by accident')
                    break

        if state == 'HANDLE':
            t = threading.Thread(target=self.delEmail, args=(mails, deles))
            t.start()

        try:
            connection.close()
            if self.log is not None:
                now = datetime.datetime.now()
                now = now.strftime("%Y-%m-%d-%H:%M:%S")
                self.log.write('disconnection from (' + address[0] + ',' + str(address[1]) + ') at ' + now + '\n')
        except:
            print('connection lost by accident')


if __name__ == "__main__":
    pop3 = Pop3()

    while True:
        cmd = input().lower()
        if cmd == 'start':
            pop3.start()
        elif cmd == 'stop':
            pop3.stop()
        elif cmd == 'restart':
            pop3.restart()
        elif cmd == 'quit':
            pop3.stop()
            print('bye')
            break
        else:
            print('?')
