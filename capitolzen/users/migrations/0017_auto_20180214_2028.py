# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-15 01:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

def forwards(apps, schema_editor):
    Action = apps.get_model('users', 'Action')

    for action in Action.objects.all().iterator():
        fk = action.object_id
        content = str(action.content_type)

        if content == 'bill':
            action.bill_id = fk
        elif content == 'wrapper':
            action.wrapper_id = fk
        elif content == 'event':
            action.event_id = fk
        else:
            raise Exception
        action.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20180212_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='bill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proposals.Bill'),
        ),
        migrations.AlterField(
            model_name='action',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proposals.Event'),
        ),
        migrations.AlterField(
            model_name='action',
            name='wrapper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proposals.Wrapper'),
        ),
        migrations.RunPython(forwards),
    ]
