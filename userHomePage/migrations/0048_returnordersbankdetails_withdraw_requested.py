# Generated by Django 4.1.7 on 2023-05-25 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0047_remove_returnordersbankdetails_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='returnordersbankdetails',
            name='withdraw_requested',
            field=models.BooleanField(default=True),
        ),
    ]