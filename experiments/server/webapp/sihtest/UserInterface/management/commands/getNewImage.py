'''
print the name of the added image which triggered the event
'''
from django.core.management.base import BaseCommand
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess, time, os

class Handler(PatternMatchingEventHandler):
    def __init__(self):
            PatternMatchingEventHandler.__init__(self, patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)
    def on_created(self,event):
        #print(event.src_path)
        #print(os.path.basename(event.src_path))
        date = datetime.now()
        newimage = upload_image(uploadpath = os.path.basename(event.src_path), date = datetime.now())
        newimage.save()
               

        
        
if __name__ == '__main__':
   
    

class Command(BaseCommand):
    def handle(self, **options):
        observer = Observer()
        event_handler = Handler()
        observer.schedule(event_handler, '/mnt/c/sih2018/experiments/worker/images', recursive=True)
        observer.start()
        observer.join()
