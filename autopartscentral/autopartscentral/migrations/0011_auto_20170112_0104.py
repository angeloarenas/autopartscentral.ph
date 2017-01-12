# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 01:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopartscentral', '0010_auto_20170109_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='placed_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(b'PL', b'PLACED'), (b'PR', b'PROCESSED'), (b'SH', b'SHIPPED'), (b'RE', b'RECEIVED')], default=b'PL', max_length=2),
        ),
    ]
