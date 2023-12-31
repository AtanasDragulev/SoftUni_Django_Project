# Generated by Django 4.2.2 on 2023-07-18 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
                ('tax_id', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('comments', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('in_stock', models.BooleanField(default=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_created', models.DateTimeField()),
                ('products', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='core.product')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_number', models.IntegerField(unique=True)),
                ('invoice_number', models.IntegerField(unique=True)),
                ('delivery_date', models.DateTimeField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('items', models.ManyToManyField(to='inventory.inventory')),
            ],
        ),
    ]
