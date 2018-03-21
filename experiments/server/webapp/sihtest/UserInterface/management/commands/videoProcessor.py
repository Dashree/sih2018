from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess, time, os, sys
import moviepy.editor as moviepy

class videoProcessor:
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
    
    def createVideo(self, imagePath, width, height, duration):
        imagePath = event.src_path
        #dirPath = os.path.dirname(event.src_path)
        #print(os.path.basename(event.src_path))
        for res in range(width):
            for d in range(duration):
                clip = moviepy.ImageClip(imagePath, duration=int(duration[d]))
                clip.resize(newsize=(width[res],height[res])).write_videofile('singleVideo%d%d.webm'%(res,d), fps=11,codec='libvpx-vp9')

