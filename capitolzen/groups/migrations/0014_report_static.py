# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-24 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0013_auto_20170813_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='static',
            field=models.BooleanField(default=False),
        ),
    ]