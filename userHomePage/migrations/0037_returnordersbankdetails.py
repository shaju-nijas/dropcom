# Generated by Django 4.1.7 on 2023-05-22 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0036_order_order_returned_returnordersrefund'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnOrdersBankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acc_holder_name', models.CharField(max_length=255)),
                ('acc_num', models.CharField(max_length=255)),
                ('IFSC_code', models.CharField(max_length=255)),
                ('bank', models.CharField(max_length=255)),
                ('bank_branch', models.CharField(max_length=255)),
            ],
        ),
    ]