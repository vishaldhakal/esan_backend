from django.db import models

from account.models import UserProfile

class Testimonial(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    rating = models.PositiveIntegerField(default=4)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
