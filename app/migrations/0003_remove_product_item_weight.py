# Generated by Django 4.2.5 on 2023-12-05 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='item_weight',
        ),
    ]
