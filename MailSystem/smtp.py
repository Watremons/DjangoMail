from mysql import sqlHandle
from socket import *
from time import *
import os
import sys
# import signal
import threading
import base64
import re
import datetime
import uuid

otherMailDomain = 'other.com'
otherIP = '127.0.0.1'
otherPort = 8026

class Smtp:
    STOPPED = 0
    RUNNING = 1
    LISTENING = False

    state = STOPPED
    server = None
    connection = None

    maxClient = 10
    log = None

    def __init__(self, domain = 'test.com', port=8025, logDir='/log/smtp', banIPs=[], banActs=[]):
        self.ip = '0.0.0.0'
        self.port = port
        self.domain = domain
        self.logDir = logDir
        self.banIPs = banIPs
        self.banActs = banActs
        # signal.signal(signal.SIGINT, self.signalHandler)

    def start(self):
        if self.state == self.RUNNING:
            print('start smtp server passed, smtp server is running')
            return True

        try:
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.server.bind((self.ip, self.port))
            self.server.listen(self.maxClient)
            
        except:
            self.state = self.STOPPED
            print('start smtp server failed, error')
            return False

        else:
            self.state = self.RUNNING
            self.LISTENING = True
            self.connection = None
            print('smtp server started.')
            print('smtp server is listening at port ' + str(self.port))
            t = threading.Thread(target = self.listen)
            t.start()

            try:
                now = datetime.datetime.now()
                now = now.strftime("%Y-%m-%d-%H:%M:%S")
                fileDir = os.path.abspath(os.path.dirname(__file__)) + self.logDir
                if not os.path.exists(fileDir):
                    os.makedirs(fileDir)
                os.chdir(fileDir)
                fileName = 'smtp-log-' + now + '.log'
                self.log = open(fileName, 'w')
            except:
                print('make log file failed')
                self.log = None
            else:
                self.log.write('smtp start at ' + now + '\n')
            
            return True

    def stop(self):
        if self.state == self.STOPPED:
            print('stop smtp server passed, smtp server is stopped')
            return True
        
        try:
            self.LISTENING = False
            sleep(1)
            if self.connection != None:
                self.connection.close()
                print('connection close!')
            self.server.close()

            if self.log != None:
                now = datetime.datetime.now()
                now = now.strftime("%Y-%m-%d-%H:%M:%S")
                self.log.write('smtp stop at ' + now + '\n')
                self.log.close()

        except:
            self.state = self.RUNNING
            print('stop smtp server failed, error')
            return False

        else:
            self.state = self.STOPPED
            print('smtp server stopped.')
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
    
    # def signalHandler(self, signal, frame):
    #     if self.LISTENING == False:
    #         sys.exit()

    #     self.LISTENING = False
    #     print('\nTerminated listen by keyboard.')
    #     self.stop()

    def authentication(self, username, password):
        try:
            username = str(base64.b64decode(username.encode('utf-8')), 'utf-8')
            password = str(base64.b64decode(password.encode('utf-8')), 'utf-8')
            results = sqlHandle('user', 'SELECT', 'userID, password', 'username = \'' + username + '\'')
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
        if self.LISTENING == True:
            t = threading.Thread(target = self.smtpServer, daemon = True)
            t.start()
        while True:
            if self.LISTENING == False:
                print('listen stop')
                break

    def smtpServer(self):
        while True:
            try:
                connection, address = self.server.accept()
                if address[0] in self.banIPs:
                    connection.close()
                    continue

                self.connection = connection

            except:
                print('can\'t connect for the connection is closed')
                break

            thread = threading.Thread(target = self.clientConn, args = (connection, address,), daemon = True)
            thread.start()

            if self.log != None:
                now = datetime.datetime.now()
                now = now.strftime("%Y-%m-%d-%H:%M:%S")
                self.log.write('connection from (' + address[0] + ',' + str(address[1]) + ') at ' + now + '\n')
            
        if self.connection != None:
            self.connection.close()

    def send(self, email, ip, port):
        client = socket(AF_INET, SOCK_STREAM)
        try:
            client.connect((ip, port))
        except:
            print('Can\'t connect the remote smtp server!')
        else:
            data = client.recv(1024)

            message = 'helo ' + self.domain + '\r\n'
            print(message)
            client.send(message.encode('utf-8'))
            data = client.recv(1024)
            print(data)

            message = 'mail from:<' + email[4] + '>\r\n'
            print(message)
            client.send(message.encode('utf-8'))
            data = client.recv(1024)
            print(data)

            message = 'rcpt to:<' + email[5] + '>\r\n'
            print(message)
            client.send(message.encode('utf-8'))
            data = client.recv(1024)
            print(data)

            message = 'data\r\n'
            print(message)
            client.send(message.encode('utf-8'))
            data = client.recv(1024)
            print(data)

            message = email[6]
            print(message)
            client.send(message.encode('utf-8'))
            # data = client.recv(1024)

            message = '\r\n'
            client.send(message.encode('utf-8'))
            message = '.\r\n'
            client.send(message.encode('utf-8'))
            data = client.recv(1024)
            print(data)

            message = 'quit\r\n'
            print(message)
            client.send(message.encode('utf-8'))
            print('?')
            data = client.recv(1024)
            print(data)

        client.close()

    def save(self, email):
        if email[1] == -1:
            print('don\'t have this user')
            return
            
        sqlHandle('sendmail', 'INSERT', '\'' + email[0] + '\'', str(email[1]),
                 '\'' + email[2] + '\'', '\'' + email[3] + '\'',
                 '\'' + email[4] + '\'', '\'' + email[5] + '\'', 
                 '\'' + email[6] + '\'', '\'' + email[7] + '\'')
    
    def recieve(self, email):
        results = sqlHandle('user', 'SELECT', 'userID', 'username = \'' + email[5] + '\'')
        if results != (): 
            sqlHandle('recvmail', 'INSERT', '\'' + email[0] + '\'', '\'' + str(results[0][0]) + '\'',
                    '\'' + email[2] + '\'', '\'' + email[3] + '\'',
                 '\'' + email[4] + '\'', '\'' + email[5] + '\'', 
                 '\'' + email[6] + '\'', '\'' + email[7] + '\'')

    def sendMail(self, email):
        domain = email[5][re.search('@', email[5]).span()[0]+1:]
        if domain == self.domain:
            self.recieve(email)
        elif domain == otherMailDomain:
            send = threading.Thread(target = self.send, args = (email, otherIP, otherPort))
            send.start()
            send.join()
        else:
            print('email domain do not support yet!')

        self.save(email)

    def clientConn(self, connection, address):
        userID = -1
        auth = False

        message = '220 localhost Example Mail System (EMS(20200501))\r\n'
        connection.send(message.encode('utf-8'))
        state = 'WAITING'
        while True:
            try:
                message = connection.recv(1024)
            except:
                print('the connection is closed')
                break
            else:
                try:
                    data = message.decode('utf-8')[0:-2]
                    
                    if self.log != None:
                        now = datetime.datetime.now()
                        now = now.strftime("%Y-%m-%d-%H:%M:%S")
                        self.log.write('smtp get \'' + data  + '\' at ' + now + ' from (' + address[0] + ', ' + str(address[1]) + ')\n')

                    if data[0:4].lower() == 'noop':
                        message = '250 OK\r\n'
                        connection.send(message.encode('utf-8'))
                        continue

                    if state == 'WAITING':
                        if re.match('[hH][eE][lL][oO]', data):
                            valid = re.search('\S+', data[4:])
                            if valid != None:
                                heloFrom = valid.group()
                                state = 'AUTH_AFTER'
                                auth = False
                                message = '250 OK\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif re.match('[eE][hH][lL][oO]', data):
                            valid = re.search('\S+', data[4:])
                            if valid != None:
                                heloFrom = valid.group()
                                state = 'AUTH_BEFORE'
                                message = '250 OK\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif data[0:4].lower() == 'quit':
                            message = '221 Bye\r\n'
                            connection.send(message.encode('utf-8'))
                            break

                        elif data[0:10].lower() == 'auth login' or data[0:10].lower() == 'mail from:' or data[0:8].lower() == 'rcpt to:' or data[0:4].lower() == 'data':
                            message = '503 Error: send EHLO first\r\n'

                        else:
                            message = '502 Error: command not implemented\r\n'

                        connection.send(message.encode('utf-8'))

                    elif state == 'AUTH_BEFORE':
                        if data[0:10].lower() == 'auth login':
                            state = 'AUTH_LOGIN'
                            message = '334 dXNlcm5hbWU6\r\n'

                        elif data[0:4].lower() == 'quit':
                            message = '221 Bye\r\n'
                            connection.send(message.encode('utf-8'))
                            break
                        
                        elif re.match('[hH][eE][lL][oO]', data):
                            valid = re.search('\S+', data[4:])
                            if valid != None:
                                heloFrom = valid.group()
                                state = 'AUTH_AFTER'
                                message = '250 OK\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif re.match('[eE][hH][lL][oO]', data):
                            valid = re.search('\S+', data[4:])
                            if valid != None:
                                heloFrom = valid.group()
                                state = 'AUTH_BEFORE'
                                message = '250 OK\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif data[0:10].lower() == 'mail from:' or data[0:8].lower() == 'rcpt to:' or data[0:4].lower() == 'data':
                            message = '553 authentication is required\r\n'
                            
                        else:
                            message = '502 Error: command not implemented\r\n'

                        connection.send(message.encode('utf-8'))
                    
                    elif state == 'AUTH_LOGIN':
                        username = data
                        state = 'AUTH_USER'
                        message = '334 UGFzc3dvcmQ6\r\n'
                        
                        connection.send(message.encode('utf-8'))

                    elif state == 'AUTH_USER':
                        password = data
                        state = 'AUTH_PWD'
                        
                        if state == 'AUTH_PWD':
                            auth, userID = self.authentication(username, password)

                            if auth == True:
                                state = 'AUTH_AFTER'
                                message = '235 Authentication successful\r\n'
                            
                            else:
                                state = 'AUTH_BEFORE'
                                message = '535 Error: authentication failed\r\n'
                            
                            connection.send(message.encode('utf-8'))                            

                    elif state == 'AUTH_AFTER':
                        mailFrom = ''
                        
                        if data[0:10].lower() == 'mail from:':
                            mailAdd = ''
                            valid = re.search('<(\w|@|_|-|\.)*>', data[10:])
                            if valid != None:
                                mailAdd = valid.group()[1:-1]
                                if re.match('(\w|-)+(\.(\w|-)+)*@(\w|-)+(\.(\w|-)+)+', mailAdd) != None:
                                    domain = mailAdd[re.search('@', mailAdd).span()[0]+1:]
                                    if domain == self.domain or domain == otherMailDomain:
                                        if mailAdd in self.banActs:
                                            message = '550 Error: The accounts has been banned\r\n'
                                        else:
                                            mailFrom = mailAdd
                                            state = 'MAILFROM'
                                            message = '250 Mail OK\r\n'
                                    else:
                                        message = '550 Error: The domain not support yet\r\n'
                                else:
                                    message = '550 Error: Invalid User\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif data[0:4].lower() == 'quit':
                            message = '221 Bye\r\n'
                            connection.send(message.encode('utf-8'))
                            break

                        elif re.match('(([hH][eE])|([eE][hH]))[lL][oO]', data):
                            valid = re.search('\S+', data[4:])
                            if valid != None:
                                heloFrom = valid.group()
                                state = 'AUTH_AFTER'
                                message = '250 OK\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif data[0:10].lower() == 'auth login':
                            state = 'AUTH_LOGIN'
                            message = '334 dXNlcm5hbWU6\r\n'

                        elif data[0:8].lower() == 'rcpt to:' or data[0:4].lower() == 'data':
                            message = '503 bad sequence of commands\r\n'

                        else:
                            message = '502 Error: command not implemented\r\n'

                        connection.send(message.encode('utf-8'))

                    elif state == 'MAILFROM':
                        rcptTos = []

                        if data[0:8].lower() == 'rcpt to:':
                            mailAdd = ''
                            valid = re.search('<(\w|@|_|-|\.)*>', data[8:])
                            if valid != None:
                                mailAdd = valid.group()[1:-1]
                                if re.match('(\w|-)+(\.(\w|-)+)*@(\w|-)+(\.(\w|-)+)+', mailAdd) != None:
                                    domain = mailAdd[re.search('@', mailAdd).span()[0]+1:]
                                    if domain == self.domain or domain == otherMailDomain:
                                        if mailAdd in self.banActs:
                                            message = '550 Error: The accounts has been banned\r\n'
                                        else:
                                            rcptTos.append(mailAdd)
                                            state = 'RCPTTO'
                                            message = '250 Mail OK\r\n'
                                    else:
                                        message = '550 domain not support yet\r\n'
                                else:
                                    message = '550 Invalid User\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif data[0:4].lower() == 'quit':
                            message = '221 Bye\r\n'
                            connection.send(message.encode('utf-8'))
                            break

                        elif data[0:10].lower() == 'mail from:':
                            mailAdd = ''
                            valid = re.search('<(\w|@|_|-|\.)*>', data[10:])
                            if valid != None:
                                mailAdd = valid.group()[1:-1]
                                if re.match('(\w|-)+(\.(\w|-)+)*@(\w|-)+(\.(\w|-)+)+', mailAdd) != None:
                                    domain = mailAdd[re.search('@', mailAdd).span()[0]+1:]
                                    if domain == self.domain or domain == otherMailDomain:
                                        if mailAdd in self.banActs:
                                            message = '550 Error: The accounts has been banned\r\n'
                                        else:
                                            mailFrom = mailAdd
                                            state = 'MAILFROM'
                                            message = '250 Mail OK\r\n'
                                    else: 
                                        message = '550 domain not support yet\r\n'
                                else:
                                    message = '550 Invalid User\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif re.match('(([hH][eE])|([eE][hH]))[lL][oO]', data):
                            valid = re.search('\S+', data[4:])
                            if valid != None:
                                heloFrom = valid.group()
                                state = 'MAILFROM'
                                message = '250 OK\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif data[0:10].lower() == 'auth login' or data[0:4].lower() == 'data':
                            message = '503 bad sequence of commands\r\n'

                        else:
                            message = '502 Error: command not implemented\r\n'

                        connection.send(message.encode('utf-8'))

                    elif state == 'RCPTTO':
                        if data[0:8].lower() == 'data':
                            state = 'DATA'
                            mail = ''
                            message = '354 End data with <CR><LF>.<CR><LF>\r\n'
                            # data
                            pass

                        elif data[0:4].lower() == 'quit':
                            message = '221 Good bye\r\n'
                            connection.send(message.encode('utf-8'))
                            break

                        elif data[0:8].lower() == 'rcpt to:':
                            mailAdd = ''
                            valid = re.search('<(\w|@|_|-|\.)*>', data[8:])
                            if valid != None:
                                mailAdd = valid.group()[1:-1]
                                if re.match('(\w|-)+(\.(\w|-)+)*@(\w|-)+(\.(\w|-)+)+', mailAdd) != None:
                                    domain = mailAdd[re.search('@', mailAdd).span()[0]+1:]
                                    if domain == self.domain or domain == otherMailDomain:
                                        if mailAdd in self.banActs:
                                            message = '550 Error: The accounts has been banned\r\n'
                                        else:
                                            rcptTos.append(mailAdd)
                                            state = 'RCPTTO'
                                            message = '250 Mail OK\r\n'
                                    else:
                                        message = '550 domain not support yet\r\n'
                                else:
                                    message = '550 Invalid User\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif re.match('(([hH][eE])|([eE][hH]))[lL][oO]', data):
                            valid = re.search('\S+', data[4:])
                            if valid != None:
                                heloFrom = valid.group()
                                state = 'RCPTTO'
                                message = '250 OK\r\n'
                            else:
                                message = '500 Error: bad syntax\r\n'

                        elif data[0:10].lower() == 'auth login' or data[0:8].lower() == 'mail from:':
                            message = '503 bad sequence of commands\r\n'

                        else:
                            message = '502 Error: command not implemented\r\n'

                        connection.send(message.encode('utf-8'))
                    
                    elif state == 'DATA':
                        mail = mail + data + '\r\n'
                        if mail[-7:] == '\r\n\r\n.\r\n':
                            mail = mail[:-5]
                            state = 'QUEUED'
                            message = '250 Mail OK queued\r\n'
                            connection.send(message.encode('utf-8'))
                            if state ==  'QUEUED':
                                for rcptTo in rcptTos:
                                    now = datetime.datetime.now()
                                    now = now.strftime("%Y-%m-%d %H:%M:%S")
                                    time_ = str(now)
                                    mailID = str(uuid.uuid4())
                                    ip = address[0]
                                    email = [mailID, userID, heloFrom, ip, mailFrom, rcptTo, mail, time_]
                                    send = threading.Thread(target = self.sendMail, args = (email,))
                                    send.start()

                                state = 'AUTH_AFTER'
                    else:
                        print(state + 'error')
                        break

                except:
                    print('connection lost by accident')
                    break
        try:
            connection.close()
            if self.log != None:
                    now = datetime.datetime.now()
                    now = now.strftime("%Y-%m-%d-%H:%M:%S")
                    self.log.write('disconnection from (' + address[0] + ',' + str(address[1]) + ') at ' + now + '\n')
        except:
            print('connection lost by accident')

if __name__ == "__main__":
    smtp = Smtp()
    while True:
        cmd = input().lower()
        if cmd == 'start':
            smtp.start()
        elif cmd == 'stop':
            smtp.stop()
        elif cmd == 'restart':
            smtp.restart()
        elif cmd == 'quit':
            smtp.stop()
            print('bye')
            break
        else:
            print('?')
