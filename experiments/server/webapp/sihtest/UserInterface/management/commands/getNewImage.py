'''
print the name of the added image which triggered the event
'''
import subprocess, time, os
from datetime import date, datetime

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from django.core.management.base import BaseCommand
from UserInterface.models import upload_image, videoDir
import UserInterface.views

from .videoProcessor import VideoProcessor

class Handler(PatternMatchingEventHandler):
    def __init__(self):
        super(Handler, self).__init__(patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)
                
    def on_created(self,event):
        '''
        #print(event.src_path)
        #print(os.path.basename(event.src_path))
        today = date.today()
        newimage = upload_image(date=today, uploadpath=event.src_path)
        newimage.save()
        '''
        
        videoP = VideoProcessor(event.src_path)
        videoP.createVideo()
        #width=int(sys.argv[1]) //import width and height according to resolution from views 
        #height = int(sys.argv[2])// import duration from views(all three given by user)
        videoP.demuxerInput()
        newimage = upload_image(date=datetime.strptime(videoP.getDate(), '%d%b%Y'), uploadpath=videoP.getImagePath())
        newimage.save()
        videoList = os.listdir(videoP.getVideosPath())
        for video in range(len(videoList)):
            videoName = videoList[video].split("_")
            videoDur= videoName[2].split(".")
            newVideo = videoDir(resfield=videoName[1],fpsfield=videoDur[0],upload=os.path.join(videoP.getVideosPath(),videoList[video]),date=datetime.strptime(videoP.getDate(), '%d%b%Y'))
            newVideo.save()

        

class Command(BaseCommand):
    def handle(self, **options):
        observer = Observer()
        event_handler = Handler()
        observer.schedule(event_handler, '/mnt/c/images/', recursive=True)
        observer.start()
        observer.join()
