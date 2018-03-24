from django.db import models
import os
from datetime import date
"""
# Create your models here.

# def upload_path_videos(instance, filename):
#     directory =os.path.dirname('videos/{date}'%(instance.date))
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#     directory =os.path.dirname('videos/{date}/{res}'%(instance.date, instance.res))
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#     directory =os.path.dirname('videos/{date}/{res}/{fps}'%(instance.date, instance.resfield, instance.fpsfield))
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#     return "videos/{date}/{res}/{fps}/{file}"%(instance.date, instance.resfield, instance.fpsfield, filename)


# def upload_path_images(instance, filename):
#     directory =os.path.dirname('/mnt/c/sih2018/experiments/worker/images/{date}'%(instance.date))
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#     return "/mnt/c/sih2018/experiments/worker/images/{date}/{file}"%(instance.date, filename)
"""
class PnC(models.Model):
   # res = [360, 720, 1080, 1440]
   # fps = [0.5, 1, 2, 4]
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
    upload = models.FileField(upload_to='videos/%Y-%m-%d/{res}/{fps}' + str(resfield, fpsfield))    # to upload it to a folder
    date = models.DateField()   # passing a reference to the EntryDate

    def __str__(self):
        return str(self.upload)

class upload_image(models.Model):
    date = models.DateField()
    # directory =os.path.dirname('/mnt/c/sih2018/experiments/worker/images/{date}' + (str(date)))
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
    uploadpath = models.FileField(upload_to='images/%Y-%m-%d')

    def __str__(self):
        return str(self.uploadpath)
