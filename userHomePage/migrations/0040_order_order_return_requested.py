# Generated by Django 4.1.7 on 2023-05-24 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0039_returnordersbankdetails_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_return_requested',
            field=models.BooleanField(default=False),
        ),
    ]
