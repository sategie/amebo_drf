from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
  user = models.ForeignKey(
      User, related_name='notifications', on_delete=models.CASCADE
  )
  message = models.CharField(max_length=255)
  created_date = models.DateTimeField(auto_now_add=True)
  seen = models.BooleanField(default=False)

  class Meta:
    ordering = ['-created_date']
  
  def __str__(self):
      return f'Notification for {self.user.username}: {self.message}'