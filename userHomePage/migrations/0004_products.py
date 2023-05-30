# Generated by Django 4.1.7 on 2023-04-06 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mrp', models.FloatField(default=0.0)),
                ('price', models.FloatField(default=0.0)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='product')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userHomePage.categories')),
            ],
        ),
    ]