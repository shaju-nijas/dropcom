# Generated by Django 4.1.7 on 2023-05-01 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_affiliatecommission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='affiliatecommission',
            name='order_id',
        ),
    ]
