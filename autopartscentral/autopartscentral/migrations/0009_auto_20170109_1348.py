# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopartscentral', '0008_auto_20170109_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
