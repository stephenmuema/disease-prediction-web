# Generated by Django 3.1.1 on 2020-09-30 16:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0021_auto_20200929_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='alternative_phone_number',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='mobile_money_phone_number',
        ),
    ]
