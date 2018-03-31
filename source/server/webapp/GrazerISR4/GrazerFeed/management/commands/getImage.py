from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from django.core.management.base import BaseCommand
from GrazerFeed.models import ImageUpload, VideoUpload

from .videoProcessing import VideoProcessing

class Handler(PatternMatchingEventHandler):
    def __init__(self):
        super(Handler, self).__init__(patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)

    def on_created(self,event):
        videoP = VideoProcessing(event.src_path)
        videoP.createVideo()
        newimage = ImageUpload(upload = videoP.getImagePath(), imgDate = videoP.getDate(), imgTime = videoP.getTime())
        newimage.save()
        videoP.demuxerInput()
        videoList = videoP.getVideosPath()
        for res, fps, videopath in videoList:
            newVideo = VideoUpload.objects.get_or_create(resfield=res,fpsfield=fps,date=videoP.getDate())
            newVideo.uploadPath = videopath
            newvideo.save()

class Command(BaseCommand):
    def handle(self, **options):
        observer = Observer()
        event_handler = Handler()
        observer.schedule(event_handler,'/mnt/c/images', recursive=True)
        observer.start()
        observer.join()
