# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-17 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopartscentral', '0003_auto_20160816_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='line_2',
            field=models.CharField(blank=True, default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoryl1',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoryl2',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoryl3',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='part',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='middle_name',
            field=models.CharField(blank=True, default='', max_length=30),
            preserve_default=False,
        ),
    ]
