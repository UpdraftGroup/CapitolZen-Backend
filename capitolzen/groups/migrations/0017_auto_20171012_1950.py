# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-12 23:50
from __future__ import unicode_literals

import capitolzen.groups.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0016_auto_20171011_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='logo',
        ),
        migrations.AddField(
            model_name='group',
            name='avatar',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=capitolzen.groups.models.avatar_directory_path),
        ),
    ]