import requests
def test():
    content = {'signature': 1, 'timestamp': 2, 'nonce': 3, 'echostr': 4}
    r = requests.get('http://127.0.0.1:8000/check/', params=content)
    print(r.content)
test()