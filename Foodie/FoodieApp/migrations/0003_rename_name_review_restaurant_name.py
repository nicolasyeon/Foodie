# Generated by Django 3.2.4 on 2021-06-20 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FoodieApp', '0002_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='name',
            new_name='restaurant_name',
        ),
    ]
