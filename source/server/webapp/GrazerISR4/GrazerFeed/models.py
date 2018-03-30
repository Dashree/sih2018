from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from datetime import date
# Create your models here.

class User(AbstractUser):
    port = models.IntegerField(max_length = 100, null = False, unique  = True)
    
class videoDir(models.Model):
    resfield = models.IntegerField(null = False)
    fpsfield = models.IntegerField(null = False)
    uploadPath = models.TextField()
    uploadDate = models.DateField()
    
class ImageDir(models.Model):
    upload = models.TextField()
    date = models.DateField()