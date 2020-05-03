from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Comment, Notification, Subscription


@receiver(post_save, sender=Comment)
def on_comment_created(sender, instance, created, **kwargs):
    comment = instance
    subscriptions = Subscription.objects.filter(post__id__exact=comment.post.id)
    notification_type = 'created' if created else 'updated'
    for s in subscriptions:
        Notification.objects.create(type=notification_type, comment=comment, subscription=s)


@receiver(post_save, sender=Comment)
def on_comment_saved(sender, instance, **kwargs):
    for n in instance.notifications.all():
        n.save()

