from django.db import models

# Create your models here.


class Users(models.Model):
    openid = models.CharField(max_length=30)
    user = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50)


class Grade(models.Model):
    openid = models.CharField(max_length=30)
    class_name = models.CharField(max_length=50)
    class_credit = models.CharField(max_length=30)
    class_grade = models.CharField(max_length=30)


class Exam(models.Model):
    openid = models.CharField(max_length=30)
    class_name = models.CharField(max_length=50)
    class_credit = models.CharField(max_length=30)
    class_type = models.CharField(max_length=30)
    class_way = models.CharField(max_length=30)
    class_time = models.CharField(max_length=30)
    class_location = models.CharField(max_length=30)
    class_seat = models.CharField(max_length=30)