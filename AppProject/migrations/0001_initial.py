# Generated by Django 5.0.2 on 2024-03-02 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarBarnd',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cus_id', models.CharField(default='', max_length=13, primary_key=True, serialize=False)),
                ('email', models.CharField(default='', max_length=100)),
                ('name', models.CharField(default='', max_length=100)),
                ('tell', models.CharField(default='', max_length=10)),
                ('address', models.TextField(default='')),
                ('role', models.CharField(default='ลูกค้า', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DailyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('ren_count', models.IntegerField(default=0)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Employ',
            fields=[
                ('em_id', models.CharField(default='', max_length=13, primary_key=True, serialize=False)),
                ('email', models.CharField(default='', max_length=100)),
                ('name', models.CharField(default='', max_length=100)),
                ('tell', models.CharField(default='', max_length=10)),
                ('address', models.TextField(default='')),
                ('role', models.CharField(choices=[('พนักงาน', 'พนักงาน'), ('แอดมิน', 'แอดมิน')], default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('car_id', models.CharField(default='', max_length=5, primary_key=True, serialize=False)),
                ('model', models.CharField(default='', max_length=100)),
                ('type', models.CharField(choices=[('รถยนต์', 'รถยนต์'), ('มอเตอร์ไซค์', 'มอเตอร์ไซค์')], max_length=20)),
                ('price', models.FloatField(default=0.0)),
                ('rental_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('picture', models.ImageField(default='', upload_to='static/cars/')),
                ('brand', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='AppProject.carbarnd')),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ren_start', models.DateField()),
                ('ran_end', models.DateField(blank=True, null=True)),
                ('total', models.FloatField(default=0.0)),
                ('car_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='AppProject.car')),
                ('cus_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='AppProject.customer')),
            ],
        ),
    ]
