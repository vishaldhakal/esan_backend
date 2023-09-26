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
    phone_number = models.CharField(max_length=20,blank=True)
    address = models.CharField(max_length=500,blank=True)
    nationality = models.CharField(max_length=100,default="Nepal")
    bio = models.TextField(blank=True)
    facebook_link = models.CharField(max_length=250,blank=True)
    instagram_link = models.CharField(max_length=250,blank=True)
    twitch_link = models.CharField(max_length=250,blank=True)
    discord_link = models.CharField(max_length=250,blank=True)
    reddit_link = models.CharField(max_length=250,blank=True)
    website_link = models.CharField(max_length=250,blank=True)
    youtube_link = models.CharField(max_length=250,blank=True)
    twitter_link = models.CharField(max_length=250,blank=True)
    linkedin_link = models.CharField(max_length=250,blank=True)

    def __str__(self) -> str:
        return self.username
    

class Player(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class BlogWriter(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    website = models.URLField(max_length=200,blank=True)
    position = models.CharField(max_length=500,blank=True)

    def __str__(self):
        return self.user.username

class Organizer(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    organizer_name = models.CharField(max_length=255,unique=True,blank=True)

    def __str__(self):
        return self.user.username

class Organization(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255,unique=True,blank=True)
    players = models.ManyToManyField(UserProfile,related_name="organization_players")

    def __str__(self):
        return self.organization_name

class PlayerRequest(models.Model):
    STARTED_BY_CHOICES = (
        ('Player','Player'),
        ('Organization','Organization'),
    )
    STATUS_CHOICES = (
        ('Requested','Requested'),
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
    )
    player = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="player_request")
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="organization_request")
    request_date = models.DateTimeField(auto_now_add=True)
    request_started_by = models.CharField(max_length=500,choices=STARTED_BY_CHOICES,default='Organization')
    request_status = models.CharField(max_length=500,choices=STATUS_CHOICES,default='Requested')
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.organization.organization_name

class OTP(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    otp = models.IntegerField()