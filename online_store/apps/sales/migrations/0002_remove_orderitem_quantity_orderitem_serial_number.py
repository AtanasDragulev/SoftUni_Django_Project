# Generated by Django 4.2.2 on 2023-08-01 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='serial_number',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]