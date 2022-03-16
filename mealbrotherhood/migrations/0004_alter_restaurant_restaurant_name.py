# Generated by Django 4.0.3 on 2022-03-16 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealbrotherhood', '0003_rename_title_restaurant_restaurant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='restaurant_name',
            field=models.CharField(choices=[('None', 'None'), ('KFC', 'ქეიეფსი'), ('MCDONALDS', 'მაკდონალდსი'), ('SHAWARMA', 'შაურმა')], default='None', max_length=150, unique=True),
        ),
    ]
