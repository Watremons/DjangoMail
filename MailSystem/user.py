from mysql import sqlHandle

class User:
    username = ''
    type = ''
    state = False
    manager = None

    def __init__(self):
        pass
    
    def login(self, username_, password_):
        if self.state == True:
            print('login pass, already login')
            return True
        
        results = sqlHandle('user', 'SELECT', 'password, type, usable', 'username = \'' + username_ + '\'')

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
        if self.state == False:
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

        if self.state == False:
            print('change password error, did not login')
            return False
        
        results = sqlHandle('user', 'SELECT', 'userID, password', 'username = \'' + self.username + '\'')
        
        userID = str(results[0][0])
        password = results[0][1]
        
        if oldPass == password:
            print('change password successfully, please login again')
            self.logout()
            return sqlHandle('user', 'UPDATE', 'password = \'' + newPass + '\'', 'userID = ' + userID)
        else:
            self.state = False
            print('change password error, password wrong')
            return False

    def initManager(self):
        if self.state == False:
            print('user manager init error, did not login')
            return False

        if self.type == '0':
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
        results = sqlHandle('user', 'SELECT', '*')
        for result in results:
            user = (result[1], result[3], result[4])
            users.append(user)
        return users

    def addNewUser(self, username, password, type, usable):
        if (type != '0' and type != '1') or (usable != '0' and usable != '1'):
            print('add new user error, parameter wrong')
            return False

        results = sqlHandle('user', 'SELECT', 'userID', 'username = \'' + username + '\'')

        if len(results) != 0:
            print('add new user error, already has this user')
            return False

        return sqlHandle('user', 'INSERT', 'null', '\'' + username + '\'', '\'' + password + '\'', type, usable)

    def changeUserType(self, username, type):
        if type != '0' and type != '1':
            print('change user type, parameter error')
            return False
        
        results = sqlHandle('user', 'SELECT', 'userID', 'username = \'' + username + '\'')

        if len(results) == 0:
            print('change user type error, no such user')
            return False
        
        userID = str(results[0][0])

        return sqlHandle('user', 'UPDATE', 'type = \'' + type + '\'', 'userID = ' + userID)

    def changeUserUsable(self, username, usable):
        if usable != '0' and usable != '1':
            print('change user usable error, parameter wrong')
            return False
        
        results = sqlHandle('user', 'SELECT', 'userID', 'username = \'' + username + '\'')

        if len(results) == 0:
            print('change user usable error, no such user')
            return False
        
        userID = str(results[0][0])

        return sqlHandle('user', 'UPDATE', 'usable = \'' + usable + '\'', 'userID = ' + userID)

    def deleteUser(self, username):
        results = sqlHandle('user', 'SELECT', 'userID', 'username = \'' + username + '\'')

        if len(results) == 0:
            print('delete user errpr, no such user')
            return False
        
        userID = str(results[0][0])

        sqlHandle('recvmail', 'DELETE', 'userID = ' + userID)
        sqlHandle('sendmail', 'DELETE', 'userID = ' + userID)
        return sqlHandle('user', 'DELETE', 'userID = ' + userID)


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