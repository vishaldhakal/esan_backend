from django.db import models

# Create your models here.

class OurTeam(models.Model):
    name = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    image = models.ImageField(blank=True)
    facebook_link = models.CharField(max_length=250,blank=True)
    instagram_link = models.CharField(max_length=250,blank=True)
    twitch_link = models.CharField(max_length=250,blank=True)
    discord_link = models.CharField(max_length=250,blank=True)
    twitter_link = models.CharField(max_length=250,blank=True)
    linkedin_link = models.CharField(max_length=250,blank=True)
    
    def __str__(self):
        return self.name