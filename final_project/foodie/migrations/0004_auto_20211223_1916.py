# Generated by Django 3.2.4 on 2021-12-23 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0003_remove_collage_creators'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collage',
            name='creator',
        ),
        migrations.AddField(
            model_name='collage',
            name='creators',
            field=models.ManyToManyField(related_name='creators', to='foodie.User'),
        ),
    ]
