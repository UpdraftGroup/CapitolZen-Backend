# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-03 23:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0018_merge_20171017_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='modified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='group',
            name='modified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='report',
            name='modified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]
