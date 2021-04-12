import pymysql
import traceback


def sqlHandle(tableName, handle, *data):
    usableTables = ['Mails', 'Users', 'Contacts', 'Attachments']
    # ip = '123.56.118.225'
    ip = '81.70.104.60'
    sqluser = 'root'
    sqlpass = '123456cc'
    database = 'djangomail'

    if tableName not in usableTables:
        print('no such table')
        return False

    try:
        db = pymysql.connect(host=ip, user=sqluser, password=sqlpass, database=database, port=3306)
    except:
        print('can\'t connect to the database!')
        return False

    cursor = db.cursor()
    sql = ''

    if handle == 'SELECT':
        if len(data) == 1:
            sql = 'SELECT ' + data[0] + ' FROM ' + tableName + ';'
        elif len(data) == 2:
            sql = 'SELECT ' + data[0] + ' FROM ' + tableName + ' WHERE ' + data[1] + ';'
        else:
            print('select handle, parameter error')
            db.close()
            return False

    elif handle == 'INSERT':
        if len(data) == 0:
            print('insert handle, parameter error')
            db.close()
            return False
        elif data[0] == "paralist":
            sql = 'INSERT INTO ' + tableName + ' ('

            sep = (len(data)-1)//2+1
            sql = sql + data[1]
            if (len(data) > 2):
                for di in data[2:sep]:
                    sql = sql + ',' + di
            sql = sql + ')'

            sql = sql + ' VALUES (' + data[sep]

            if len(data) > 3:
                for di in data[sep+1:]:
                    sql = sql + ', ' + di

            sql = sql + ');'
            print(sql)
        else:
            sql = 'INSERT INTO ' + tableName + ' VALUES (' + data[0]

            if len(data) > 1:
                for di in data[1:]:
                    sql = sql + ', ' + di

            sql = sql + ');'

    elif handle == 'DELETE':
        if len(data) == 1:
            sql = 'DELETE FROM ' + tableName + ' WHERE ' + data[0] + ';'
        else:
            print('delete handle, parameter error')
            db.close()
            return False

    elif handle == 'UPDATE':
        if len(data) == 2:
            sql = 'UPDATE ' + tableName + ' SET ' + data[0] + ' WHERE ' + data[1] + ';'
        else:
            print('update handle, parameter error')
            db.close()
            return False
    else:
        print('error, unknown handle')
        return False

    results = True
    try:
        # print(sql)
        cursor.execute(sql)

        if handle == 'SELECT':
            results = cursor.fetchall()

        db.commit()

    except Exception as e:
        traceback.print_exc()
        print("sql handle error, rollback")
        db.rollback()

    cursor.close()
    db.close()
    return results


if __name__ == "__main__":
    print('mysql.py')
    pass

# result = sqlHandle('test', 'INSERT', '1', '2')
# print(result)
# sqlHandle('test', 'SELECT', '*')
# sqlHandle('test', 'DELETE', 'a = \'a\'')
# sqlHandle('test', 'SELECT', '*')
# sqlHandle('test', 'UPDATE', 'a = \'a\'', 'a = \'1\'')
# sqlHandle('test', 'SELECT', '*')
# result = sqlHandle('test', 'DELETE', 'a = \'1\'')
# print(result)
# result = sqlHandle('test', 'SELECT', '*')
# print(result)

# results = sqlHandle('user', 'INSERT', 'null', '\'One_Random\'', '\'admin\'', '0', '1')
# newUser('test', '1', '0', '1')