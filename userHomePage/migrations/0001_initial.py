# Generated by Django 4.1.7 on 2023-04-04 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='pro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_name', models.CharField(max_length=100)),
                ('dep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userHomePage.dep')),
            ],
        ),
    ]