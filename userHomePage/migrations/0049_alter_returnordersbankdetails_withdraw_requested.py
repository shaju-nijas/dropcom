# Generated by Django 4.1.7 on 2023-05-25 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0048_returnordersbankdetails_withdraw_requested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returnordersbankdetails',
            name='withdraw_requested',
            field=models.BooleanField(default=False),
        ),
    ]
