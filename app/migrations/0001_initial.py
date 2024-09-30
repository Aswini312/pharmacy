# Generated by Django 4.2.5 on 2023-11-25 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('expiry_date', models.DateField()),
                ('mg', models.IntegerField()),
                ('net_quantity', models.PositiveIntegerField()),
                ('batch_no', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=100)),
                ('item_weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item_form', models.CharField(max_length=50)),
                ('age_range', models.CharField(max_length=20)),
                ('item_dimension', models.CharField(max_length=50)),
                ('availability_status', models.CharField(max_length=20)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
    ]
