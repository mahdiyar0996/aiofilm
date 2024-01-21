# Generated by Django 5.0 on 2024-01-21 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(error_messages={'invalid': 'رمز کاربری باید ۸ کاراکتر یا بیشتر باشد و یک حرف بزرگ  و یک عدد داشته باشد'}, max_length=254, verbose_name='رمز عبور'),
        ),
    ]