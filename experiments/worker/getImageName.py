'''
print the name of the added image which triggered the event
'''

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess, time, os

class Handler(PatternMatchingEventHandler):
    def __init__(self):
            PatternMatchingEventHandler.__init__(self, patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)
    def on_created(self,event):
        #print(event.src_path)
        print(os.path.basename(event.src_path))
        
if __name__ == '__main__':
   
    observer = Observer()
    event_handler = Handler()
    observer.schedule(event_handler, '/mnt/c/Hackathon/image', recursive=True)
    observer.start()
    try:     
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
