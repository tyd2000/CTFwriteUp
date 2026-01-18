import re
import json
import base64
import random
import requests
from bs4 import BeautifulSoup

url='http://96b4e347-a838-44f6-84e6-4eecf3efa8fc.challenge.ctf.show/'
s=requests.session()
username=str(random.randint(1,100000))
print(username)
r=s.get(url+'?username='+username)
responses=[]

for i in range(10):
        r=s.get(url+'find_dragonball')
        responses.append(json.loads(r.text))

for item in responses:
        data=json.dumps({'player_id':item['player_id'],'dragonball':item['dragonball'],'round_no':item['round_no'],'time':item['time']})
        miwen=base64.b64decode(item['address'])
        round_no=item['round_no']
        if round_no in [str(i) for i in range(1,8)]:
                fake_address=miwen[:64]+miwen[80:]
                fake_address=base64.b64encode(fake_address).decode()
                r=s.get(url+'get_dragonball',params={"address":fake_address})

r=s.get(url+'flag')
soup = BeautifulSoup(r.text, 'html.parser')
# print(soup)
flags = re.findall(r'ctfshow\{[a-zA-Z0-9\-_]+\}', soup.get_text())
print(flags[0])
# ctfshow{adc5e683-70fd-47b9-92b2-77c9ec2fd1bb}