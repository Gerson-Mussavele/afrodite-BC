# Generated by Django 5.0 on 2023-12-28 17:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetodoPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendas.metodopagamento')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Order.order')),
            ],
        ),
    ]
