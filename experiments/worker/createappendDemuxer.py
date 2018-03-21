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
            self.n = 0
    
    def concat(self, file): 
        command = ['ffmpeg',
               '-f', 'concat',
               '-safe', '0',
               '-i', file,
               '-c', 'copy',
               '-flags', 'global_header',
               'video1.webm']
        subprocess.run(command)
        os.remove('video.webm')
        os.rename('video1.webm', 'video.webm')

    def createVideo():
        imagePath = event.src_path
        dirPath = os.path.dirname(event.src_path)
        print(os.path.basename(event.src_path))
        width=int(sys.argv[1])
        height = int(sys.argv[2])
        clip = moviepy.ImageClip(imagePath, duration=4)
        clip.resize(newsize=(width,height)).write_videofile('singleVideo.webm', fps=4,codec='libvpx-vp9')
        
    def on_created(self,event):
        if(os.path.exists('concat.txt')):
            if(self.n == 0):
                f = open('concat.txt', 'a')
                f.write("\n" + "file 'singleVideo.webm'")
                f.close()
                self.n = 1
            self.concat('concat.txt')
        else:
            os.rename('singleVideo.webm', 'video.webm')
            f = open('concat.txt', 'w') 
            f.write("file 'video.webm'")
            f.close()


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
