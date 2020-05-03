# Generated by Django 2.1 on 2020-05-03 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200502_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='blog.Comment')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='blog.Subscription')),
            ],
        ),
    ]
