from django.db import models

# Create your models here.
class MySession(models.Model):
    openid = models.CharField(max_length=30)
    wechat_session = models.CharField(max_length=50)
    session_value = models.CharField(max_length=50, default=0)