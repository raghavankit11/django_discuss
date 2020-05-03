from django.db import models
from django.template.defaultfilters import register
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    anonymous = models.BooleanField("Post as Anonymous User", editable=True, default=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @register.simple_tag
    def subscribed_to_users(self, user):
        users = self.subscriptions.filter(user__exact=user)
        return users


class Comment(models.Model):
    content = models.TextField()
    anonymous = models.BooleanField("Comment as Anonymous User", editable=True, default=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.author.username + ' (' + self.date_posted.strftime("%d %B, %Y %I:%M %p") + ') - ' + self.content

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})


class Subscription(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='subscriptions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')


class Notification(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='notifications')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='notifications')
