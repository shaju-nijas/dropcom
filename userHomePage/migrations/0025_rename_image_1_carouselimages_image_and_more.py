# Generated by Django 4.1.7 on 2023-04-12 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userHomePage', '0024_carouselimages'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carouselimages',
            old_name='image_1',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='carouselimages',
            name='image_2',
        ),
        migrations.RemoveField(
            model_name='carouselimages',
            name='image_3',
        ),
    ]