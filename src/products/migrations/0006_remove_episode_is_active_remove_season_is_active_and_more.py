# Generated by Django 5.0 on 2024-01-23 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_episode_options_alter_movie_is_ongoing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='season',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='serial',
            name='is_active',
        ),
    ]
