# Generated by Django 4.1.7 on 2023-05-03 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlayAndWin', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lottodrop',
            name='result_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lottodrop',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]