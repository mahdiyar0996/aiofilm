# Generated by Django 5.0 on 2024-02-17 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_user_sex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='is_active',
        ),
        migrations.AddField(
            model_name='ticket',
            name='admin_closed',
            field=models.BooleanField(default=False, verbose_name='بسته شده توسط ادمین'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user_close',
            field=models.BooleanField(default=False, verbose_name='بسته شده توسط کاربر'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='users/default.jpg', upload_to='users/', verbose_name='آواتار'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(error_messages={'invalid': 'رمز کاربری باید ۸ کاراکتر یا بیشتر باشد و یک حرف بزرگ  و یک عدد داشته باشد'}, max_length=254, verbose_name='رمز عبور'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='جنسیت'),
        ),
    ]
