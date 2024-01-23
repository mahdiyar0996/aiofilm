# Generated by Django 5.0 on 2024-01-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_episode_is_active_remove_season_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=64, null=True, verbose_name='اسلاگ'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='file',
            field=models.FileField(upload_to='media/products/files', verbose_name='فایل'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.ImageField(upload_to='media/products/images/', verbose_name='عکس'),
        ),
    ]
