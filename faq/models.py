from django.db import models

# Create your models here.
from django.db import models

class FAQ(models.Model):
    heading = models.CharField(max_length= 100)
    detail = models.TextField()
    value = models.CharField(max_length= 100)


