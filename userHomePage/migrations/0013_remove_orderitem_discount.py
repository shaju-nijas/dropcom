# Generated by Django 4.1.7 on 2023-04-08 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0012_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='discount',
        ),
    ]