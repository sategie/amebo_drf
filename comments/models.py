from django.db import models
from django.contrib.auth.models import User
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