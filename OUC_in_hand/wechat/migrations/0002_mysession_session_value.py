# Generated by Django 2.1.3 on 2018-11-21 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysession',
            name='session_value',
            field=models.CharField(default=0, max_length=50),
        ),
    ]