# Generated by Django 4.2.3 on 2023-07-23 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sell_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
