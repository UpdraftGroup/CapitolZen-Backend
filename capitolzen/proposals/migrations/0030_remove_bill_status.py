# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-02 11:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0029_auto_20171102_0722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='status',
        ),
    ]
