from django.db import models
from django.contrib.auth.models import User
from notifications.models import Notification
from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    post_content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title


@receiver(post_save, sender=Post)
def create_post_notification(sender, instance, created, **kwargs):
    """
    Signal which creates a notification for followers of a user
    when the user posts a new content.
    """
    if created:
        # Find all followers of the user who created the post
        followers = instance.user.followed_user.all()
        for follower in followers:
            Notification.objects.create(
                user=follower.user,
                message=f"{instance.user.username} has created a new post: {instance.title}"
            )