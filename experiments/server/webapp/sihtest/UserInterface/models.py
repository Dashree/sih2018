from django.db import models
import os
from datetime import date
class videoDir(models.Model):
    res = (
       (0, 360),
       (1, 720),
       (2, 1080),
       (3, 1440),
    )
    fps = (
       (0, 0.5),
       (1, 1),
       (2, 2),
       (3, 4),
    )
    resfield = models.IntegerField(choices=res)                 # to get 1 resolution
    fpsfield = models.IntegerField(choices=fps)                 # to get one frame per sec value
    upload = models.TextField()    # to upload it to a folder
    date = models.DateField()   # passing a reference to the EntryDate



class upload_image(models.Model):
    date = models.DateField()
    uploadpath = models.TextField()

    def __str__(self):
        return str(self.uploadpath)
