# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 15:43
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def forwards(apps, schema_editor):
    Bill = apps.get_model('proposals', 'Bill')
    Committee = apps.get_model('proposals', 'Committee')

    for bill in Bill.objects.all().iterator():
        for action in bill.history:
            committee = None
            chamber = None
            if action.type == 'committee:referred':
                action_parts = action.action.lower().split('referred to committee ')
                committee = action_parts[0]
                chamber = action.actor
            if action.type == 'committee:passed':
                committee = None
                chamber = None

            if committee and chamber:
                bill.current_committee = Committee.objects.filter(name__icontains=committee, chamber=chamber).first()
                bill.save()


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0032_wrapper_files'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
