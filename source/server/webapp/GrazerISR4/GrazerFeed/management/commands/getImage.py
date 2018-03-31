from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from django.core.management.base import BaseCommand
from GrazerFeed.models import ImageUpload, VideoUpload

from .videoProcessing import VideoProcessing

class Handler(PatternMatchingEventHandler):
    def __init__(self):
        super(Handler, self).__init__(patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)

    def convert_image(self, srcpath):
        videoP = VideoProcessing(srcpath)
        videoP.createVideo()
        newimage = ImageUpload(upload = videoP.getImagePath(), imgDate = videoP.getDate(), imgTime = videoP.getTime())
        newimage.save()
        videoP.demuxerInput()
        videoList = videoP.getVideosPath()
        for res, fps, videopath in videoList:
            newVideo, created = VideoUpload.objects.get_or_create(resfield=res,fpsfield=fps,uploadDate=videoP.getDate(), uploadtime = videoP.getTime())
            newVideo.uploadPath = videopath
            newVideo.save()

    def on_created(self,event):
        self.convert_image(event.src_path)
        
class Command(BaseCommand):
    def start_observer(self):
        observer = Observer()
        event_handler = Handler()
        observer.schedule(event_handler,'/mnt/c/images', recursive=True)
        observer.start()
        observer.join()

    def handle(self, **options):
        self.start_observer()
        #handler = Handler()
        #handler.convert_image('/mnt/c/Hackathon_Images/3DIMG_01SEP2017_0000_L1C_ASIA_MER_IR1.jpg')
