# Generated by Django 2.1.3 on 2018-12-22 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='class_name',
            field=models.CharField(max_length=50),
        ),
    ]