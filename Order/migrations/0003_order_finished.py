# Generated by Django 5.0 on 2024-01-08 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0002_remove_order_products_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
