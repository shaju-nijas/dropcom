# Generated by Django 4.1.7 on 2023-05-23 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userHomePage', '0038_returnordersrefund_return_amount_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='returnordersbankdetails',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
