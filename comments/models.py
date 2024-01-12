from django.db import models
from django.contrib.auth.models import User
from notifications.models import Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post


class Comment(models.Model):
    """
    Comment model related to User and Post

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.comment_content


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """
    Signal which creates a notification when a new comment is made
    on the user's own post
    """
    if created:
        comment_message = (
            f"{instance.user.username} commented on "
            f"'{instance.post.title}'"
        )
        Notification.objects.create(
            user=instance.post.user,
            message=comment_message,
        )
