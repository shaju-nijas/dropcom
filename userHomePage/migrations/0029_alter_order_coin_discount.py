# Generated by Django 4.1.7 on 2023-04-15 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0028_alter_order_date_time_of_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='coin_discount',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]