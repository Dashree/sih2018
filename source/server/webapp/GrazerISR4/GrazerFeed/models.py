from django.db import models
from django.contrib.auth.models import User
import os
import datetime
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    port = models.IntegerField(unique = True)   
    
class VideoUpload(models.Model):
    resfield = models.IntegerField(null = False)
    fpsfield = models.IntegerField(null = False)
    uploadPath = models.TextField()
    uploadDate = models.DateField(null = False, blank=False)
    uploadtime = models.TimeField(null = False, blank=False)
    
class ImageUpload(models.Model):
    upload = models.TextField()
    imgDate = models.DateField(null=False, blank=False)
    imgTime = models.TimeField(null = False, blank = False)

