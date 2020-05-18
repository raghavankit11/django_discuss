from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Comment, Notification, Subscription
from django.db import transaction


@receiver(post_save, sender=Comment)
def on_comment_created(sender, instance, created, **kwargs):
    comment = instance
    subscriptions = Subscription.objects.filter(post__id__exact=comment.post.id)
    notification_type = 'created' if created else 'updated'

    notifications = list(map(lambda s: Notification(type=notification_type, comment=comment, subscription=s),
                             subscriptions))

    Notification.objects.bulk_create(notifications)


@receiver(post_save, sender=Comment)
def on_comment_saved(sender, instance, **kwargs):
    bulk_save_notifications(instance.notifications)


@transaction.atomic
def bulk_save_notifications(notifications):
    for n in notifications.all():
        n.save()
