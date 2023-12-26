from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Like(models.Model):
    """
    Like model related to 'user' and 'post'.

    unique_together is used to ensure that a user cannot like the same post
    more than once.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']
        unique_together = ['user', 'post']

def __str__(self):
        return f'{self.user} likes {self.post}'