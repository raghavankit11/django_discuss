from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Comment, Notification, Subscription


@receiver(post_save, sender=Comment)
def create_notifications(sender, instance, created, **kwargs):
    if created:
        comment = instance
        subscriptions = Subscription.objects.filter(post__id__exact=comment.post.id)
        for s in subscriptions:
            Notification.objects.create(comment=comment, subscription=s)


@receiver(post_save, sender=Comment)
def save_notifications(sender, instance, **kwargs):
    for n in instance.notifications.all():
        n.save()
