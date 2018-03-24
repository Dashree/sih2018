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
            self.width = [2560, 1920, 1280, 640]
            self.height = [1440, 1080, 720, 360]
            self.duration = [0.5, 1, 2 , 3]
            self.day = 0
            self.n = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    
    def on_created(self,event):
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
        videoP = videoProcessor()
        videoP.createVideo(event.src_path, self.width, self.height, self.duration)
        #width=int(sys.argv[1]) //import width and height according to resolution from views 
        #height = int(sys.argv[2])// import duration from views(all three given by user)
        for x in range(len(self.width)):
            for y in range(len(self.duration)):
                if(os.path.exists('concat%d%d.txt'%(x,y)) and self.day <= 47):
                    if(self.n[x][y] == 1):
                        f = open('concat%d%d.txt'%(x,y), 'a')
                        f.write("\n" + "file 'singleVideo%d%d.webm'"%(x,y))
                        self.n[x][y] = 0
                        f.close()
                          
                else:
                     os.rename('singleVideo%d%d.webm'%(x,y), 'video%d%d.webm'%(x,y))
                     f = open('concat%d%d.txt'%(x,y), 'w') 
                     f.write("file 'video%d%d.webm'"%(x,y))
                     f.close()
                     self.n[x][y] = 1
                     self.day = 0
            
                print("%d%d"%(x,y))
                if(self.n[x][y] != 1):
                    videoP.concat('concat%d%d.txt'%(x,y), x, y)
                    self.day += 1

class Command(BaseCommand):
    def handle(self, **options):
        observer = Observer()
        event_handler = Handler()
        observer.schedule(event_handler, '/mnt/c/sih2018/experiments/worker/images', recursive=True)
        observer.start()
        observer.join()
