from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100,null=False)
    jpg = models.CharField(max_length=100,null=False)
    download = models.CharField(max_length=100,null=False)
