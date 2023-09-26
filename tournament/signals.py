from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import BannerImage
import os

@receiver(pre_delete, sender=BannerImage)
def delete_player_profile_picture(sender, instance, **kwargs):
    # Delete the profile picture file when a Player instance is deleted
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
