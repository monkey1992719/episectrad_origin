# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-10 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tokenmetric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenmetric',
            name='price_usd',
            field=models.DecimalField(decimal_places=7, max_digits=12),
        ),
    ]
