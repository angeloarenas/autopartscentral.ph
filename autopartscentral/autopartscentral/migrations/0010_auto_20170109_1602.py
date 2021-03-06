# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autopartscentral', '0009_auto_20170109_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='autopartscentral.OrderDiscount'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_details', to='autopartscentral.PartDiscount'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='autopartscentral.Order'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_details', to='autopartscentral.Part'),
        ),
    ]
