# Generated by Django 4.1.7 on 2023-05-24 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0044_rename_returned_order_refunde_requested_order_returned_order_refund_requested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_expected_delivery_date',
            field=models.DateTimeField(blank=True, max_length=200, null=True),
        ),
    ]
