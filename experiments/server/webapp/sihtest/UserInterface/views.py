from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("UserInterface Created")

def video(request):
    return render(request, 'UserInterface/video.html')
    
class Handler(PatternMatchingEventHandler):
    def __init__(self):
            PatternMatchingEventHandler.__init__(self, patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)
    def on_created(self,event):
        #print(event.src_path)

        print(os.path.basename(event.src_path))
        
# how to run this in background
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