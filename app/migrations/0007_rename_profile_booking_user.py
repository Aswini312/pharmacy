# Generated by Django 5.0.4 on 2024-09-22 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_booking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='profile',
            new_name='user',
        ),
    ]
