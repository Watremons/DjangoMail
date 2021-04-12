from mysql import sqlHandle
import datetime


class User:
    username = ''
    type = ''
    state = False
    manager = None

    def __init__(self):
        pass

    def login(self, username_, password_):
        if self.state is True:
            print('login pass, already login')
            return True

        results = sqlHandle(
            'Users', 'SELECT', 'userPassword, authorityValue, userState',
            'userName = \'' + username_ + '\''
            )

        if len(results) == 0:
            print('login error, no such user')
            return False

        password = results[0][0]
        type_ = results[0][1]
        usable_ = results[0][2]

        if password == password_:
            if usable_ == '0':
                print('login error, user disable')
            else:
                self.username = username_
                self.type = type_
                self.state = True
                self.manager = None

                print('login successfully, %s!' % (self.username))
                return True
        else:
            self.state = False
            print('login error, password wrong')
            return False

    def logout(self):
        if self.state is False:
            print('logout pass, did not login')
            return True

        self.username = ''
        self.type = ''
        self.state = False
        self.manager = None

        print('logout successfully!')
        return True

    def changePassword(self, oldPass, newPass):
        if oldPass == newPass:
            print('change password error, two passwords are same')
            return False

        if self.state is False:
            print('change password error, did not login')
            return False

        results = sqlHandle(
            'Users', 'SELECT', 'userNo, userPassword', 'userName = \'' +
            self.username + '\''
            )

        userNo = str(results[0][0])
        password = results[0][1]

        if oldPass == password:
            print('change password successfully, please login again')
            self.logout()
            return sqlHandle('Users', 'UPDATE', 'userPassword = \'' + newPass + '\'', 'userNo = ' + userNo)
        else:
            self.state = False
            print('change password error, password wrong')
            return False

    def initManager(self):
        if self.state is False:
            print('user manager init error, did not login')
            return False

        if self.type == 1 or self.type == 2:
            self.manager = UserManager()
            print('user manager init successfully!')
            return True
        else:
            self.manager = None
            print('user manager init error, permission denied')
            return False


class UserManager:
    def showUser(self):
        users = []
        results = sqlHandle('Users', 'SELECT', '*')
        for result in results:
            user = (result[1], result[3], result[4])
            users.append(user)
        return users

    def addNewUser(self, username, password, type, usable):
        if (usable != '0' and usable != '1'):
            print('add new user error, parameter wrong')
            return False

        if (type != '0' and type != '1'):
            print("User of level" + str(type) + "is not allowed to create")
            return False

        results = sqlHandle('Users', 'SELECT', 'userNo', 'userName = \'' + username + '\'')

        if len(results) != 0:
            print('add new user error, already has this user')
            return False

        timenow = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return sqlHandle(
            'Users', 'INSERT',
            'paralist',
            'userName', 'createDate', 'authorityValue', 'userState', 'userPassword',
            '\'' + username + '\'',
            '\'' + timenow + '\'',
            type,
            usable,
            '\'' + password + '\''
            )

    def changeUserType(self, username, type):
        if type != '0' and type != '1':
            print('change user type, parameter error')
            return False

        results = sqlHandle('Users', 'SELECT', 'userNo', 'userName = \'' + username + '\'')

        if len(results) == 0:
            print('change user type error, no such user')
            return False

        userID = str(results[0][0])

        return sqlHandle('Users', 'UPDATE', 'authorityValue = ' + type, 'userNo = ' + userID)

    def changeUserUsable(self, username, usable):
        if usable != '0' and usable != '1':
            print('change user usable error, parameter wrong')
            return False

        results = sqlHandle('Users', 'SELECT', 'userNo', 'userName = \'' + username + '\'')

        if len(results) == 0:
            print('change user usable error, no such user')
            return False

        userID = str(results[0][0])

        return sqlHandle('Users', 'UPDATE', 'userState = ' + usable, 'userNo = ' + userID)

    def deleteUser(self, username):
        results = sqlHandle('Users', 'SELECT', 'userName', 'userName = \'' + username + '\'')

        if len(results) == 0:
            print('delete user errpr, no such user')
            return False

        userName = str(results[0][0])

        sqlHandle('Mails', 'DELETE', 'sender = \'' + userName + '\'')
        sqlHandle('Mails', 'DELETE', 'receiver = \'' + userName + '\'')
        return sqlHandle('Users', 'DELETE', 'userName = \'' + userName + '\'')


if __name__ == "__main__":
    user = User()
    user.login('One_Random', 'admin')
    if user.initManager():
        user.manager.showUser()
    user.logout()

    user.login('user1', '1')
    if user.initManager():
        user.manager.showUser()
    user.logout()

    # user.changePassword('123', 'One_Random')
    # um = UserManager()
    # results = user.addNewUser('One_Random', 'x', '0', '0')
    # results = user.deleteUser('One_Random')
    # print(results)
    pass
