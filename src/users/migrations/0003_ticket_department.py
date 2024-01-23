# Generated by Django 5.0 on 2024-01-22 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='department',
            field=models.CharField(choices=[('پشتیبانی', 'پشتیبانی'), ('مشکلات فنی', 'مشکلات فنی'), ('پیشنهادات و انتقادات', 'پیشنهادات و انتقادات'), ('اپلیکیشن', 'اپلیکیشن'), ('مشکلات ترجمه', 'مشکلات ترجمه')], db_index=True, default=None, max_length=64, verbose_name='دپارتمان'),
            preserve_default=False,
        ),
    ]