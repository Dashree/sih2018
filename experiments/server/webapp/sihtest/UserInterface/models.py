from django.db import models
#import itertools

# Create your models here.

class EntryDate(models.Model):
    entry = models.DateTimeField(auto_now_add=True)

def upload_path_videos(instance, filename):
    return "videos/{date}/{res}/{fps}/{file}".format(date = instance.date, res=instance.resfield, fps =instance.fpsfield,file=filename)
                                # ^ 4 fps folders per resolution
def upload_path_images(instance, filename):
    return "images/{date}/{file}".format(date = instance.date,file=filename)
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
    upload = models.FileField(upload_to=upload_path_videos)    # to upload it to a folder
    date = models.ForeignKey(EntryDate, on_delete=models.CASCADE)   # passing a reference to the EntryDate


class upload_image(models.Model):
    upload = models.ImageField(upload_to=upload_path_images)
    date = models.ForeignKey(EntryDate, on_delete=models.CASCADE)   # passing a reference to the EntryDate
