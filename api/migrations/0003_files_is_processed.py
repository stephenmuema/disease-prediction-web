# Generated by Django 3.1.1 on 2020-09-30 18:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0002_files_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
    ]
