from django.db import models
from django.contrib.auth.models import User

class Follower(models.Model):
    """
    Follower model related to user and followed_user.

    user is a person that is following another person

    followed_user is a person that is being followed by the user

    unique_together constraint ensures that a user cannot follow the same
    followed_user twice
    """

    user = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )

    followed_user = models.ForeignKey(
        User, related_name='followed_user', on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']
        unique_together = ['user', 'followed_user']

    def __str__(self):
        return f'{self.user} is following {self.followed_user}'






