# Generated by Django 2.2.5 on 2019-09-08 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_auto_20190908_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='converted_imaged',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to='', width_field='width_field'),
        ),
    ]
