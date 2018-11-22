from django.test import TestCase
from django.test import Client
from wechat import wechat_session
# Create your tests here.
def test_check():
    csrf_client = Client(enforce_csrf_checks=True)
    response = csrf_client.get('/check?signature=1&timestamp=12&nonce=123&echostr=1234')
    print(response.content_params)
def test_session_change():
    wechat_session.change_session("ovqtx1pb5eSYAZz1A0ArBIbD_glQ", "binding", 2)

test_session_change()