# Generated by Django 3.2.4 on 2021-12-21 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collage',
            name='creators',
            field=models.ManyToManyField(related_name='creators', to='foodie.User'),
        ),
    ]
