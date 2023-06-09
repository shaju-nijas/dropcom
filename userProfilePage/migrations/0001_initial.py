# Generated by Django 4.1.7 on 2023-04-24 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdraws',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdraw_requested_amount', models.CharField(max_length=100)),
                ('withdraw_requested', models.BooleanField(default=False)),
                ('withdraw_completed', models.BooleanField(default=False)),
                ('date_time_of_withdraw_requested', models.DateTimeField(auto_now_add=True)),
                ('date_time_of_withdraw_completed', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
