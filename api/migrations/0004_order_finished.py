# Generated by Django 5.0 on 2024-01-18 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_order_table_number_alter_order_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
