# Generated by Django 4.1.7 on 2023-05-23 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0037_returnordersbankdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='returnordersrefund',
            name='return_amount_paid',
            field=models.BooleanField(default=False),
        ),
    ]