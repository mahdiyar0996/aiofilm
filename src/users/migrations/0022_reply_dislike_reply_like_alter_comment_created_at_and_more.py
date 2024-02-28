# Generated by Django 5.0 on 2024-02-28 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_ticketadminreply_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='dislike',
            field=models.BooleanField(default=False, verbose_name='دیس لایک'),
        ),
        migrations.AddField(
            model_name='reply',
            name='like',
            field=models.BooleanField(default=False, verbose_name='لایک'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='اخرین بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='ticketadminreply',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت'),
        ),
        migrations.AlterField(
            model_name='ticketadminreply',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='اخرین بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='ticketdetails',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت'),
        ),
        migrations.AlterField(
            model_name='ticketdetails',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='اخرین بروزرسانی'),
        ),
    ]
