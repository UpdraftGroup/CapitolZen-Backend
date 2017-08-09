from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Organization
from .tasks import intercom_manage_organization
from organizations.signals import user_added, user_removed
from cacheops import invalidate_obj


@receiver(post_save, sender=Organization)
def intercom_update_organization(sender, **kwargs):
    """
    https://www.whatan00b.com/posts/celery-jobs-unable-to-access-objects-when-queued-by-post_save-signal-in-django/
    http://docs.celeryproject.org/en/latest/whatsnew-4.0.html#django-support
    https://docs.djangoproject.com/en/1.11/topics/db/transactions/#performing-actions-after-commit

    We delay the task execution 10 seconds because post_save
    isn't post database commit. Need to how to take
    advantage of transaction.on_commit while still using the receiver decorator.
    This isn't great, because technically it could take longer than 10
    seconds to do a db transaction.

    :param sender:
    :param kwargs:
    :return:
    """

    created = kwargs.get('created')
    organization = kwargs.get('instance')

    if created:
        intercom_manage_organization.apply_async(
            [str(organization.id), "create"], countdown=10)
    else:
        intercom_manage_organization.apply_async(
            [str(organization.id), "update"], countdown=10)


@receiver(post_delete, sender=Organization)
def intercom_delete_organization(sender, **kwargs):
    organization = kwargs.get('instance')
    intercom_manage_organization.apply_async(
        [str(organization.id), "delete"], countdown=10)


@receiver(user_removed)
@receiver(user_added)
def invalidate_organization_cache(sender, **kwargs):
    invalidate_obj(sender)
