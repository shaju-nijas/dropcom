# Generated by Django 4.1.7 on 2023-04-17 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_affiliatecommission'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliatecommission',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
