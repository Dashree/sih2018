from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess, time, os, sys
import moviepy.editor as moviepy
from PIL import Image

class videoProcessor:
    def concat(self, file, res, d): 
        command = ['ffmpeg',
               '-f', 'concat',
               '-safe', '0',
               '-i', file,
               '-c', 'copy',
               '-flags', 'global_header',
               'video1.webm']
        subprocess.run(command)
        os.remove('video%d%d.webm'%(res,d))
        os.rename('video1.webm', 'video%d%d.webm'%(res,d))
    
    def createVideo(self, imagePath, width, height, duration):
        #imagePath = event.src_path
        #dirPath = os.path.dirname(event.src_path)
        #print(os.path.basename(event.src_path))
        print(imagePath)
        im = Image.open(imagePath)
        width1, height1 = im.size
        for res in range(len(width)):
            for d in range(len(duration)):
                clip = moviepy.ImageClip(imagePath, duration=duration[d])
                if(width1 <= 360 and height1 <= 360):
                    clip.write_videofile('singleVideo%d%d.webm'%(res, d), fps=11, codec='libvpx-vp9', ffmpeg_params=['-lossless','1'])
                else:
                    clip.resize(newsize=(width[res],height[res])).write_videofile('singleVideo%d%d.webm'%(res,d), fps=11, codec='libvpx-vp9', ffmpeg_params=['-lossless','1'])

