# Generated by Django 5.1.7 on 2025-06-13 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_nationality_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authorsubmission',
            name='nationality',
        ),
    ]
