# Generated by Django 5.0 on 2024-02-15 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_remove_payment_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='price',
            field=models.BigIntegerField(default=1, verbose_name='قیمیت'),
            preserve_default=False,
        ),
    ]
