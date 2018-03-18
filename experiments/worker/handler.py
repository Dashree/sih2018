'''
print the name of the added image which triggered the event
'''

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess, time, os, sys
import moviepy.editor as moviepy

class Handler(PatternMatchingEventHandler):
    def __init__(self):
            PatternMatchingEventHandler.__init__(self, patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)
    
    def concat(self, video): 
        resolution = sys.argv[3]
        print(video)
        command = ['ffmpeg',
               '-c:v', 'libvpx-vp9',
               '-i', 'video.webm',
               '-c:v', 'libvpx-vp9',
               '-i', video,
               '-filter_complex', '[0:v:0] [1:v:0] concat=n=2:v=1:a=0[outv]',
               '-map', '[outv]','-y','video1.webm']
        subprocess.run(command)
        #os.rename('video1.webm','video.webm')
        
    def on_created(self,event):
        imagePath = event.src_path
        dirPath = os.path.dirname(event.src_path)
        print(os.path.basename(event.src_path))
        width=int(sys.argv[1])
        height = int(sys.argv[2])
        clip = moviepy.ImageClip(imagePath, duration=10)
        clip.resize(newsize=(width,height)).write_videofile('singleVideo.webm', fps=1,codec='libvpx-vp9')
        self.concat('singleVideo.webm')

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
