# Generated by Django 4.0.3 on 2022-03-16 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mealbrotherhood', '0002_rename_restaurants_restaurant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='title',
            new_name='restaurant_name',
        ),
    ]
