# Generated by Django 5.0 on 2024-01-22 11:42

import django.db.models.deletion
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='اخرین بروزرسانی')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('is_active', models.BooleanField(default=True, verbose_name='وضعیت')),
                ('title', models.CharField(max_length=64, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='اخرین بروزرسانی')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('is_active', models.BooleanField(default=True, verbose_name='وضعیت')),
                ('title', models.CharField(max_length=62, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='اخرین بروزرسانی')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('is_active', models.BooleanField(default=True, verbose_name='وضعیت')),
                ('season_number', models.SmallIntegerField(db_index=True, verbose_name='فصل')),
            ],
            options={
                'verbose_name': 'season',
                'verbose_name_plural': 'seasons',
                'db_table': 'Season',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='اخرین بروزرسانی')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('is_active', models.BooleanField(default=True, verbose_name='وضعیت')),
                ('image', models.ImageField(upload_to='media/product/images/', verbose_name='عکس')),
                ('name', models.CharField(max_length=252, verbose_name='نام')),
                ('persian_name', models.CharField(max_length=252, verbose_name='نام فارسی')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='خلاصه')),
                ('average_time', models.SmallIntegerField(blank=True, null=True, verbose_name='مدت زمان')),
                ('product_of', models.CharField(blank=True, max_length=64, null=True, verbose_name='محصول')),
                ('quality', models.CharField(blank=True, choices=[('WEB-DL', 'WEB-DL'), ('HDTV', 'HDTV'), ('BluRay', 'BluRay')], max_length=64, null=True, verbose_name='کیفیت نمایش')),
                ('imdb_rate', models.PositiveSmallIntegerField(verbose_name='رتبه imdb')),
                ('age_limit', models.SmallIntegerField(default=13, verbose_name='محدوده سنی')),
                ('director', models.CharField(blank=True, max_length=64, null=True, verbose_name='کارگردان')),
                ('super_stars', models.CharField(blank=True, max_length=252, null=True, verbose_name='ستارگان')),
                ('is_ongoing', models.BooleanField(db_default=models.Value(False), verbose_name='وضعیت پخش')),
                ('ongoing_day', models.PositiveSmallIntegerField(choices=[('شنبه', 1), ('یکشنبه', 2), ('دوشنبه', 3), ('سه شنبه', 4), ('چهارشنبه', 5), ('پنجشنبه', 6), ('جمعه', 7)], db_default=models.Value(False), verbose_name='روز پخش')),
                ('release_at', models.DateField(blank=True, null=True, verbose_name='پخش از')),
                ('translation_team', models.CharField(blank=True, max_length=64, null=True, verbose_name='تیم ترجمه')),
                ('translator', models.CharField(blank=True, max_length=64, null=True, verbose_name='مترجم')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s', to='products.category', verbose_name='مجموعه')),
                ('genre', models.ManyToManyField(db_index=True, related_name='%(class)s', to='products.genre', verbose_name='ژانر')),
                ('season', models.ManyToManyField(related_name='%(class)s', to='products.season', verbose_name='فصل')),
            ],
            options={
                'verbose_name': 'movie',
                'verbose_name_plural': 'movies',
                'db_table': 'Movie',
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='اخرین بروزرسانی')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('is_active', models.BooleanField(default=True, verbose_name='وضعیت')),
                ('file', models.FileField(upload_to='media/product/files', verbose_name='فایل')),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='products.movie', verbose_name='فیلم')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='products.season', verbose_name='فصل')),
            ],
            options={
                'verbose_name': 'episode',
                'verbose_name_plural': 'episodes',
                'db_table': 'Episode',
            },
        ),
    ]
