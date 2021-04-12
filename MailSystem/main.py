import os
import sys
import json
import uuid
import getopt
import datetime
import threading
from socket import *
from user import *
from server import *
from MailSystem.mysql import sqlHandle
from MailSystem.user import User, UserManager
type = 0
connection = None
state = 0
error = False


def input__():
    global connection
    global error
    if connection is None:
        return input()
    else:
        try:
            data = connection.recv(1024).decode('utf-8')[:-2]
        except:
            error = True
            if connection is not None:
                connection.close()
            return '?'
        print(data)
        return data


def input_(string):
    global connection
    print_(string)
    if connection is None:
        return input()
    else:
        try:
            data = connection.recv(1024).decode('utf-8')[:-2]
        except:
            error = True
            if connection is not None:
                connection.close()
        print(data)
        return data


def print_(string):
    global connection
    global error
    print(string)
    if connection is not None:
        try:
            connection.send((string + '\r\n').encode('utf-8'))
        except:
            error = True
            print('send failed')
            if connection is not None:
                connection.close()


def helpInfo():
    print_('type "quit" to quit')
    print_('type "help" for these messages')
    print_('type "auth" to login')


def helpInfo_():
    print_('type "quit" to quit')
    print_('type "help" for these messages')
    print_('type "logout" to logout')
    print_('type "user show" to show all user')
    print_('type "user new" to add a new user')
    print_('type "user type" to change the type of a user')
    print_('type "user usable" to change the usable of a user')
    print_('type "user delete" to delete a user')
    print_('type "change password" to change the password')
    print_('type "send to" to send a message to many user')
    print_('---------these below can only do on local------------')
    print_('type "server start" to start smtp and pop3 server')
    print_('type "server stop" to stop smtp and pop3 server')
    print_('type "server restart" to restart smtp and pop3 server')
    print_('type "config show" to show the config')
    print_('type "config set" to set the config')
    print_('type "config default" to return the config to default')
    print_('type "config save" to save the config as a file')
    print_('type "smtp start" to start smtp server')
    print_('type "smtp stop" to stop smtp server')
    print_('type "smtp restart" to restart smtp server')
    print_('type "pop3 start" to start pop3 server')
    print_('type "pop3 stop" to stop pop3 server')
    print_('type "pop3 restart" to restart pop3 server')
    print_('type "logs show" to show the all logs')
    print_('type "logs check" to check a log')
    print_('type "logs delete" to delete a log')


def sendToMany(sender, allUser, users, data):
    if allUser is True:
        users = []
        results = sqlHandle('Users', 'SELECT', 'userName')
        for result in results:
            users.append(result[0])

    if users == []:
        print_('no user shoule be sent')
        return

    for user in users:
        results = sqlHandle('Users', 'SELECT', 'userNo', 'userName = \'' + user + '\'')
        if len(results) == 0:
            print_('send error, no such user, pass')
            continue

        isRead = 0
        isServed = 1
        ip = 'system message'
        mailFrom = sender
        rcptTo = user
        content = data
        time_ = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if sqlHandle(
                'Mails', 'INSERT', '\'' + rcptTo + '\'', '\'' + mailFrom + '\'',
                '\'' + ip + '\'',
                '\'' + isRead + '\'', '\'' + isServed + '\'',
                '\'' + content + '\'', '\'' + time_ + '\''
                ) is False:

            print_('send to ' + user + 'failed')
        else:
            print_('send successfully')


def main(argv):
    config = None
    configFile = None

    try:
        opts, args = getopt.getopt(argv, "hic:", [])
    except:
        flag = False
        print('parameter error')
        print('try to run main.py with -h -i -c [the config json file]')
    else:
        for opt in opts:
            if opt[0] == '-h':
                print('try to run main.py with -h -i -c [the config json file]')
            elif opt[0] == '-i':
                global type
                type = 1
                print('turn to online mode, you can only use with tcp socket')
            elif opt[0] == '-c':
                configFile = opt[1]

    fileDir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(fileDir)
    if configFile is not None:
        if not os.path.exists(configFile):
            print('no such json file, please check')
            return
        try:
            config = json.load(open(configFile, 'r')) 
        except:
            print('config file parameter error, please check')
            return
        else:
            print('set as \'' + configFile + '\'')
    else:
        print('didn\'t set config file, run as default config')

    server = Server(config)

    if type == 1:
        tcpServer = socket(AF_INET, SOCK_STREAM)
        tcpServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        tcpServer.bind(('0.0.0.0', 8000))
        tcpServer.listen(1)

        t = threading.Thread(target=remote, args=(tcpServer, server, config), daemon=True)
        t.start()

    while True:
        c = input('press any key to control\r\n')
        global state
        if state == 0:
            state = 1
            global connection
            connection = None
            run(server, config)
            state = 0
        else:
            print('admin is using at remote, please wait')


def remote(tcpServer, server, config):
    while True:
        global state
        global connection
        co, address = tcpServer.accept()
        print('connection accepted', address)
        if state == 0:
            state = 2
            connection = co
            
            run(server, config)

            connection.close()
            state = 0
        else:
            connection = None
            co.send('admin is using at local, please wait\r\n'.encode('utf-8'))
            co.close()
    print('connection closed')


def run(server, config):
    global connection
    global state
    global error
    error = False
    user = User()
    print_('welcome, type "help" for more, type "auth" to login, type "quit" to quit')
    while True:
        if error is True:
            break
        cmd = input__().lower()
        if user.state is False:
            if cmd == 'auth':
                username = input_('username:')
                password = input_('password:')
                user.login(username, password)
                if user.state is False:
                    print_('Login failed, retry please.')
                elif user.type == '1':
                    print_('permission denied.')
                    user.logout()
                else:
                    user.initManager()
                    if connection is not None:
                        connection.send('login successfully!\r\n'.encode('utf-8'))
                    print_('type "help" for more usages')
            elif cmd == 'quit':
                print_('bye')
                return
            elif cmd == 'help':
                helpInfo()
            else:
                print_('please type "auth" to login')
        else:
            if connection is not None:
                if cmd == 'auth':
                    print_('you has already logined')
                elif cmd == 'logout':
                    user.logout()
                elif cmd == 'user show':
                    users = user.manager.showUser()
                    for user_ in users:
                        print_(user_[0] + '    ' + user_[1] + '    ' + user_[2])
                elif cmd == 'user new':
                    username = input_('username:')
                    password = input_('password:')
                    type_ = input_('type(0 for admin, 1 for normal)')
                    usable = '1'
                    if user.manager.addNewUser(username, password, type_, usable) is True:
                        print_('add new user successfully')
                elif cmd == 'user type':
                    username = input_('username:')
                    type_ = input_('type(0 for admin, 1 for normal):')
                    if user.manager.changeUserType(username, type_) is True:
                        print_('change user type successfully')
                elif cmd == 'user usable':
                    username = input_('username:')
                    usable = input_('usable:(0 for disable, 1 for enable):')
                    if user.manager.changeUserUsable(username, usable) is True:
                        print_('change user usable successfully')
                elif cmd == 'user delete':
                    username = input_('username:')
                    if username == user.username:
                        print_('you cannot delete yourself')
                        continue

                    print_('Are you sure to delete? Press return to continued')
                    re = input_('[return]')
                    if re == '\n' or re == '\r\n' or re == '':
                        if user.manager.deleteUser(username) is True:
                            print_('delete succussfully')
                elif cmd == 'change password':
                    old = input_('old password:')
                    new = input_('new password:')
                    new_ = input_('confirm new password:')
                    if new != new_:
                        print_('new and confirme password are not same, error')
                        continue
                    user.changePassword(old, new)
                elif cmd == 'send to':
                    print_('type "all" to send to all\ntype "user" to add a user\ntype "data" to enter the content\ntype "quit" to quit')
                    state_ = 'user'
                    allUser = False
                    users = []
                    mail = ''
                    while True:
                        if state_ == 'user':
                            cmd = input__().lower()
                            if cmd == 'all':
                                state_ = 'data'
                                allUser = True
                                print_('send to all')
                                print_('write data, end data with <CR><LF>.<CR><LF>')
                            elif cmd == 'user':
                                recvs = input_('add a user:')
                                users.append(recvs)
                            elif cmd == 'data':
                                state_ = 'data'
                                print_('write data, end data with <CR><LF>.<CR><LF>')
                            elif cmd == 'quit':
                                print_('cancle to send')
                                break
                            else:
                                print_('error')
                        elif state_ == 'data':
                            data = input__()
                            mail = mail + data + '\r\n'
                            if mail[-7:] == '\r\n\r\n.\r\n':
                                mail = mail[:-5]
                                break
                        else:
                            print_('error')

                    send = threading.Thread(
                        target=sendToMany,
                        args=(user.username, allUser, users, "System Admin Message", mail)
                        )
                    send.start()
                    send.join()
                elif cmd == 'quit':
                    print_('bye')
                    return
                elif cmd == 'help':
                    helpInfo_()
                else:
                    print_('unknown command or remote control don\'t support')

            else:
                if cmd == 'server start':
                    server.server_run()
                elif cmd == 'server stop':
                    server.server_shutdown()
                elif cmd == 'server restart':
                    server.server_restart()
                elif cmd == 'config show':
                    server.config_show
                elif cmd == 'config set':
                    service = input_('service:')
                    newConfig = input_('config:')
                    value = input_('value:')
                    server.config_update(service, newConfig, value)
                elif cmd == 'config default':
                    server.config_default
                elif cmd == 'config save':
                    filename = input_('filename')
                    server.config_save(filename)
                elif cmd == 'smtp start':
                    server.smtp.start()
                elif cmd == 'pop3 start':
                    server.pop3.start()
                elif cmd == 'smtp stop':
                    server.smtp.stop()
                elif cmd == 'pop3 stop':
                    server.pop3.stop()
                elif cmd == 'stmp restart':
                    server.smtp.restart()
                elif cmd == 'pop3 restart':
                    server.pop3.restart()
                elif cmd == 'logs show':
                    t = int(input_('type(0 for smtp, 1 for pop3)'))
                    server.showAllLogFile(t)
                elif cmd == 'logs check':
                    t = int(input_('type(0 for smtp, 1 for pop3)'))
                    n = int(input_('the number of file'))
                    server.checkLogFile(t, n)
                elif cmd == 'logs delete':
                    t = int(input_('type(0 for smtp, 1 for pop3)'))
                    n = int(input_('the number of file'))
                    server.checkLogFile(t, n)

                elif cmd == 'auth':
                    print_('you has already logined')
                elif cmd == 'logout':
                    user.logout()
                elif cmd == 'user show':
                    users = user.manager.showUser()
                    for user_ in users:
                        print_(user_[0] + '    ' + user_[1] + '    ' + user_[2])
                elif cmd == 'user new':
                    username = input_('username:')
                    password = input_('password:')
                    type_ = input_('type(0 for admin, 1 for normal)')
                    usable = '1'
                    if user.manager.addNewUser(username, password, type_, usable) is True:
                        print_('add new user successfully')
                elif cmd == 'user type':
                    username = input_('username:')
                    type_ = input_('type(0 for admin, 1 for normal):')
                    if user.manager.changeUserType(username, type_) is True:
                        print_('change user type successfully')
                elif cmd == 'user usable':
                    username = input_('username:')
                    usable = input_('usable:(0 for disable, 1 for enable):')
                    if user.manager.changeUserUsable(username, usable) is True:
                        print_('change user usable successfully')
                elif cmd == 'user delete':
                    username = input_('username:')
                    if username == user.username:
                        print_('you cannot delete yourself')
                        continue

                    print_('Are you sure to delete? Press return to continued')
                    re = input_('[return]')
                    if re == '\n' or re == '\r\n' or re == '':
                        if user.manager.deleteUser(username) is True:
                            print_('delete succussfully')
                elif cmd == 'change password':
                    old = input_('old password:')
                    new = input_('new password:')
                    new_ = input_('confirm new password:')
                    if new != new_:
                        print_('new and confirme password are not same, error')
                        continue
                    user.changePassword(old, new)
                elif cmd == 'send to':
                    print_('type "all" to send to all\ntype "user" to add a user\ntype "data" to enter the content\ntype "quit" to quit')
                    state_ = 'user'
                    allUser = False
                    users = []
                    mail = ''
                    while True:
                        if state_ == 'user':
                            cmd = input__().lower()
                            if cmd == 'all':
                                state_ = 'data'
                                allUser = True
                                print_('send to all')
                                print_('write data, end data with <CR><LF>.<CR><LF>')
                            elif cmd == 'user':
                                recvs = input_('add a user:')
                                users.append(recvs)
                            elif cmd == 'data':
                                state_ = 'data'
                                print_('write data, end data with <CR><LF>.<CR><LF>')
                            elif cmd == 'quit':
                                print_('cancle to send')
                                break
                            else:
                                print_('error')
                        elif state_ == 'data':
                            data = input__()
                            mail = mail + data + '\r\n'
                            if mail[-7:] == '\r\n\r\n.\r\n':
                                mail = mail[:-5]
                                break
                        else:
                            print_('error')

                    send = threading.Thread(
                        target=sendToMany,
                        args=(user.username, allUser, users, "System Admin Message", mail)
                        )
                    send.start()
                    send.join()
                elif cmd == 'quit':
                    print_('bye')
                    return
                elif cmd == 'help':
                    helpInfo_()
                else:
                    print_('unknown command, error')


if __name__ == '__main__':
    main(sys.argv[1:])
