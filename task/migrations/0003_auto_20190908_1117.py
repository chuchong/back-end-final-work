# Generated by Django 2.2.5 on 2019-09-08 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20190908_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.CharField(max_length=64, verbose_name='用户'),
        ),
    ]
