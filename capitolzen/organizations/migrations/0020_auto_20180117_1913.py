# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-18 00:13
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings
from capitolzen.organizations.services import StripeOrganizationSync
from capitolzen.organizations.utils import get_stripe_client


def forwards(apps, schema_editor):
    stripe = get_stripe_client()

    Organization = apps.get_model('organizations', 'Organization')

    for organization in Organization.objects.all().iterator():
        if organization.stripe_subscription_id:
            subscription = stripe.Subscription.retrieve(organization.stripe_subscription_id)
            subscription.delete()
            organization.stripe_subscription_id = None
            organization.plan_name = None

        StripeOrganizationSync().execute(organization, "create_or_update")

        subscription = stripe.Subscription.create(
            customer=organization.stripe_customer_id,
            items=[
                {
                    "plan": settings.STRIPE_DEFAULT_PLAN_ID,
                },
            ]
        )
        organization.plan_name = settings.STRIPE_DEFAULT_PLAN_ID
        organization.stripe_subscription_id = subscription.get('id')
        organization.save()


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0019_auto_20180103_2002'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
