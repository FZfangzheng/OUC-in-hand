import requests
from wechat import wechat_session
def testGET():
    content = {'signature': 1, 'timestamp': 2, 'nonce': 3, 'echostr': 4}
    r = requests.get('http://127.0.0.1:8000/check/', params=content)
    print(r.content)


def testGET():
    content = {'signature': 1, 'timestamp': 2, 'nonce': 3, 'echostr': 4}
    r = requests.post('http://127.0.0.1:8000/check/', params=content)
    print(r.content)

def test_session_change():
    wechat_session.change_session("ovqtx1pb5eSYAZz1A0ArBIbD_glQ", "binding", 2)

test_session_change()