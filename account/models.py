from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_player = models.BooleanField(default=True)
    is_organization = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)
    is_blog_writer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.first_name