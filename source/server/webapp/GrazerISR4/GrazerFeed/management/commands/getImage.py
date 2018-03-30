from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from django.core.management.base import BaseCommand

from .videoProcessing import VideoProcessing

class Handler(PatternMatchingEventHandler):
    def __init__(self):
        super(Handler, self).__init__(patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)

    def on_created(self,event):
        videoP = VideoProcessing(event.src_path)
        videoP.createVideo()
        videoP.demuxerInput()


class Command(BaseCommand):
    def handle(self, **options):
        observer = Observer()
        event_handler = Handler()
        observer.schedule(event_handler,'/mnt/c/images', recursive=True)
        observer.start()
        observer.join()
