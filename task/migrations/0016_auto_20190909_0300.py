# Generated by Django 2.2.5 on 2019-09-08 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0015_auto_20190908_2237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='converted_image',
            new_name='converted_image1',
        ),
        migrations.AddField(
            model_name='task',
            name='converted_image2',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to='', width_field='width_field'),
        ),
    ]
