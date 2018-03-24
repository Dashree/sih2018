'''
print the name of the added image which triggered the event
'''
from django.core.management.base import BaseCommand
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess, time, os
from datetime import date
from .videoProcessor import videoProcessor
from UserInterface.models import upload_image
import UserInterface.views

class Handler(PatternMatchingEventHandler):
    def __init__(self):
            PatternMatchingEventHandler.__init__(self, patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)
                
    def on_created(self,event):
        '''
        #print(event.src_path)
        #print(os.path.basename(event.src_path))
        today = date.today()
        print(today)
        # directory = os.path.dirname('images/{date}' + (str(today)))
        # if not os.path.exists(directory):
        #    os.makedirs(directory)
        newimage = upload_image(date=today, uploadpath=event.src_path)
        print('in databse')
        newimage.save()
        print('calling videoprocessor now')
        '''
        videoP = videoProcessor(event.src_path)
        videoP.createVideo()
        #width=int(sys.argv[1]) //import width and height according to resolution from views 
        #height = int(sys.argv[2])// import duration from views(all three given by user)
        videoP.demuxerInput()

class Command(BaseCommand):
    def handle(self, **options):
        observer = Observer()
        event_handler = Handler()
        observer.schedule(event_handler, '/mnt/c/sih2018/experiments/worker/images', recursive=True)
        observer.start()
        observer.join()
