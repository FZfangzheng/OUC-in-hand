# Generated by Django 2.1.3 on 2018-11-21 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MySession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=30)),
                ('wechat_session', models.CharField(max_length=50)),
            ],
        ),
    ]
