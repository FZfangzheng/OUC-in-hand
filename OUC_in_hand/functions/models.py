from django.db import models

# Create your models here.


class Users(models.Model):
    openid = models.CharField(max_length=30)
    user = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50)


class Grade(models.Model):
    openid = models.CharField(max_length=30)
    class_name =models.CharField(max_length=30)
    class_credit = models.CharField(max_length=30)
    class_grade = models.CharField(max_length=30)