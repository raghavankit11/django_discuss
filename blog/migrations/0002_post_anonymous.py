# Generated by Django 2.1 on 2020-05-01 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='anonymous',
            field=models.BooleanField(default=True, verbose_name='Post as Anonymous User'),
        ),
    ]
