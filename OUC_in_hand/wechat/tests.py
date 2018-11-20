from django.test import TestCase
from django.test import Client
# Create your tests here.
def test_check():
    csrf_client = Client(enforce_csrf_checks=True)
    response = csrf_client.get('/check?signature=1&timestamp=12&nonce=123&echostr=1234')
    print(response.content_params)
test_check()