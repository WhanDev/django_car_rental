# Generated by Django 5.0.2 on 2024-03-05 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppProject', '0007_remove_rentalreture_car_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalpayment',
            name='bank',
        ),
    ]
