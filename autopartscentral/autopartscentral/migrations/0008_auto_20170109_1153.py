# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 11:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('autopartscentral', '0007_auto_20170107_1553'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='availability',
            new_name='is_available',
        ),
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='discount',
        ),
        migrations.AddField(
            model_name='order',
            name='discount_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='order',
            name='net_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_city',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_contact_no',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_country',
            field=models.CharField(choices=[(b'PH', b'Philippines')], default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_first_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_last_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_line_1',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_line_2',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_province',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='staff_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='discount_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='discount_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='net_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='part_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='part_number',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdiscount',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='partdiscount',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orderdetails', to='autopartscentral.Part'),
        ),
        migrations.AlterField(
            model_name='part',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parts', to='autopartscentral.Brand'),
        ),
        migrations.AlterField(
            model_name='part',
            name='category_l1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='parts', to='autopartscentral.CategoryL1'),
        ),
        migrations.AlterField(
            model_name='part',
            name='category_l2',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field=b'category_l1', chained_model_field=b'category', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parts', to='autopartscentral.CategoryL2'),
        ),
        migrations.AlterField(
            model_name='part',
            name='category_l3',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field=b'category_l2', chained_model_field=b'category', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parts', to='autopartscentral.CategoryL3'),
        ),
        migrations.AlterField(
            model_name='partfeatured',
            name='part',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='part_featured', to='autopartscentral.Part'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='default_shipping_address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userprofile', to='autopartscentral.Address'),
        ),
    ]
