# Generated by Django 4.1.7 on 2023-04-08 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0009_orderitem_order_checkoutaddress'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]