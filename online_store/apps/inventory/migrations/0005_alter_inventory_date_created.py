# Generated by Django 4.2.2 on 2023-07-20 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_delivery_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='date_created',
            field=models.DateField(),
        ),
    ]
