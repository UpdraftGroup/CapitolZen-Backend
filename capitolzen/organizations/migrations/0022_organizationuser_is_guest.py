# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-05 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0021_auto_20180118_0605'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationuser',
            name='is_guest',
            field=models.BooleanField(default=False),
        ),
    ]
