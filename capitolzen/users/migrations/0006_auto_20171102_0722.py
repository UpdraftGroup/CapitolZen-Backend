# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-02 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_merge_20171017_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='modified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='modified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]
