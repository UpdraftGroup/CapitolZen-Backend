# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-12 23:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0011_auto_20171011_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='logo',
        ),
    ]
