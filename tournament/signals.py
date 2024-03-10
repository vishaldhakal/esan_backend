from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import BannerImage
import os

from .models import EliminationMode

def create_initial_admin(sender, **kwargs):
    if not EliminationMode.objects.exists():
        EliminationMode.objects.create(elimination_mode="Single Elimination")
        EliminationMode.objects.create(elimination_mode="Double Elimination")
        EliminationMode.objects.create(elimination_mode="Round Robin")
        EliminationMode.objects.create(elimination_mode="Battle Royale")

@receiver(pre_delete, sender=BannerImage)
def delete_player_profile_picture(sender, instance, **kwargs):
    # Delete the profile picture file when a Player instance is deleted
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
