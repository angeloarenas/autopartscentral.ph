# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-18 02:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopartscentral', '0011_auto_20170112_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(b'PL', b'PLACED'), (b'PR', b'PROCESSED'), (b'SH', b'SHIPPED'), (b'RE', b'RECEIVED'), (b'CA', b'CANCELLED')], default=b'PL', max_length=2),
        ),
    ]
