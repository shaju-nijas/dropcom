# Generated by Django 4.1.7 on 2023-04-05 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='username',
        ),
    ]