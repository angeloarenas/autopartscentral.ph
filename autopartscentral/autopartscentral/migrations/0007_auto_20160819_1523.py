# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-19 15:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autopartscentral', '0006_auto_20160819_0336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryl1',
            options={'verbose_name_plural': 'Category Level 1'},
        ),
        migrations.AlterModelOptions(
            name='categoryl2',
            options={'verbose_name_plural': 'Category Level 2'},
        ),
        migrations.AlterModelOptions(
            name='categoryl3',
            options={'verbose_name_plural': 'Category Level 3'},
        ),
        migrations.AlterModelOptions(
            name='vehicleengine',
            options={'verbose_name_plural': '4. Vehicle Engines'},
        ),
        migrations.AlterModelOptions(
            name='vehiclemake',
            options={'verbose_name_plural': '1. Vehicle Makes'},
        ),
        migrations.AlterModelOptions(
            name='vehiclemodel',
            options={'verbose_name_plural': '2. Vehicle Models'},
        ),
        migrations.AlterModelOptions(
            name='vehicletrim',
            options={'verbose_name_plural': '5. Vehicle Trims'},
        ),
        migrations.AlterModelOptions(
            name='vehicleyear',
            options={'verbose_name_plural': '3. Vehicle Years'},
        ),
    ]
