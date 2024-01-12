from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
     upload_to='images/',
     default='images/blank-profile-picture-973460_1280_skkwoi_n5jmh4'
    )

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.user.username} Profile'


def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver which creates a new profile automatically each time
    a new user instance is created
    """
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_profile, sender=User)
