# Generated by Django 5.0 on 2024-01-23 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_remove_paymentmethod_bank_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='is_active',
        ),
    ]