# Generated by Django 4.0.3 on 2022-03-15 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('mealbrotherhood', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Restaurants',
            new_name='Restaurant',
        ),
    ]