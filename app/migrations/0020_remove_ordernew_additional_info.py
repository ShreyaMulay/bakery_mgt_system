# Generated by Django 3.2.7 on 2024-03-23 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20240323_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordernew',
            name='additional_info',
        ),
    ]
