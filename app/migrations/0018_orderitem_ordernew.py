# Generated by Django 3.2.7 on 2024-03-23 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0017_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=1000)),
                ('lastname', models.CharField(max_length=1000)),
                ('country', models.CharField(max_length=1000)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=1000)),
                ('state', models.CharField(max_length=1000)),
                ('postcode', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('email', models.EmailField(max_length=10)),
                ('additional_info', models.TextField()),
                ('amount', models.CharField(max_length=10000)),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=1000)),
                ('image', models.ImageField(upload_to='bakery/ordernew/image')),
                ('quantity', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=50)),
                ('total', models.CharField(max_length=10000)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ordernew')),
            ],
        ),
    ]
