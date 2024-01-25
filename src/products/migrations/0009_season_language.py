# Generated by Django 5.0 on 2024-01-25 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_genre_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='language',
            field=models.CharField(choices=[('دوبله فارسی', 'دوبله فارسی'), ('هارد ساب', 'هارد ساب'), ('زبان اصلی', 'زبان اصلی')], default=None, max_length=62, verbose_name='زبان (زیرنویس) (دوبله)'),
            preserve_default=False,
        ),
    ]