from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class UserProfile(AbstractUser):
    role_choices = (
        ('Player', 'Player'),
        ('Organization', 'Organization'),
        ('Organizer', 'Organizer'),
        ('Blog Writer', 'Blog Writer'),
        ('Admin', 'Admin'),
    )
    
    status_choices = (
        ('Active', 'Active'),
        ('Banned', 'Banned'),
    )
    
    role = models.CharField(max_length=15, choices=role_choices)
    avatar = models.ImageField(blank=True)
    status = models.CharField(max_length=15, choices=status_choices,default="Active")
    is_verified = models.BooleanField(default=False)
    password_reset_token = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.username
    
class Player(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/images/player_profile_pictures/',blank=True)
    country = models.CharField(max_length=100,blank=True)
    phone_number = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.user.username

class BlogWriter(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,blank=True)
    profile_picture = models.ImageField(upload_to='media/images/blog_profile_pictures/',blank=True)
    website = models.URLField(max_length=200,blank=True)

    def __str__(self):
        return self.user.username

class Organizer(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='media/images/organizer_logos/',blank=True)
    description = models.TextField(max_length=500,blank=True)
    website = models.URLField(max_length=200,blank=True)

    def __str__(self):
        return self.user.username

class Organization(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255,unique=True)
    logo = models.ImageField(upload_to='media/images/organization_logos/',blank=True)
    description = models.TextField(max_length=500,blank=True)
    website = models.URLField(max_length=200,blank=True)
    address = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.organization_name
    
class Game(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='meddia/images/game_by_admin')

    def __str__(self):
        return self.name


