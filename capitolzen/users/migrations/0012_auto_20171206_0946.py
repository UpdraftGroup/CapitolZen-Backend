# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-06 14:46
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20171124_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='preferences',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='action',
            name='title',
            field=models.CharField(choices=[('bill:introduced', 'Bill Introduced'), ('wrapper:updated', 'Bill Updated'), ('organization:user-add', 'User Joined'), ('organization:user-invite', 'User Invited'), ('user:mention', 'Mentioned'), ('committee:meeting', 'Committee Meeting')], db_index=True, max_length=225),
        ),
    ]
