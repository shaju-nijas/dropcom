# Generated by Django 4.1.7 on 2023-04-24 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfilePage', '0002_withdraws_withdraw_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdraws',
            name='withdrawed_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]