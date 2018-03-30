from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from django.core.management.base import BaseCommand
from GrazerFeed.models import ImageUpload

from .videoProcessing import VideoProcessing

class Handler(PatternMatchingEventHandler):
    def __init__(self):
        super(Handler, self).__init__(patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)

    def on_created(self,event):
        videoP = VideoProcessing(event.src_path)
        videoP.createVideo()
        newimage = ImageUpload(upload = videoP.getImagePath(), imgDate = videoP.getDate())
        newimage.save()
        videoP.demuxerInput()

        videoList = os.listdir(videoP.getVideosPath())
        for video in range(len(videoList)):
            videoName = videoList[video].split("_")
            videoDur= videoName[2].split(".")
            newVideo = videoUpload(resfield=videoName[1],fpsfield=videoDur[0],uploadPath=os.path.join(videoP.getVideosPath(),videoList[video]),uploadDate=datetime.strptime(videoP.getDate(), '%d%b%Y'))
            newVideo.save()


class Command(BaseCommand):
    def handle(self, **options):
        observer = Observer()
        event_handler = Handler()
        observer.schedule(event_handler,'/mnt/c/images', recursive=True)
        observer.start()
        observer.join()
