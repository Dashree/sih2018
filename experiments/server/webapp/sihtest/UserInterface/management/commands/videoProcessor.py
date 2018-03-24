from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess, time, os, sys
import moviepy.editor as moviepy
from PIL import Image

class videoProcessor:
    def __init__(self,imagePath):
        self.imagePath = imagePath
        self.width = [2560, 1920, 1280, 640]
        self.height = [1440, 1080, 720, 360]
        self.duration = [0.5, 1, 2 , 3]
        self.day = 0
        self.n = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    def demuxerInput(self):
        for res in range(len(self.width)):
            for d in range(len(self.duration)):
                if(os.path.exists('concat%d%d.txt'%(res,d)) and self.day <= 47):
                    if(self.n[res][d] == 1):
                        f = open('concat%d%d.txt'%(res,d), 'a')
                        f.write("\n" + "file 'singleVideo_%d_%d.webm'"%(self.height[res],self.duration[d]))
                        self.n[res][d] = 0
                        f.close()
                          
                else:
                     os.rename('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]), 'video_%d_%d.webm'%(self.height[res],self.duration[d]))
                     f = open('concat%d%d.txt'%(res,d), 'w') 
                     f.write("file 'video_%d_%d.webm'"%(self.height[res],self.duration[d]))
                     f.close()
                     self.n[res][d] = 1
                     self.day = 0
            
                print("%d%d"%(res,d))
                if(self.n[res][d] != 1):
                    videoP.concat('concat%d%d.txt'%(res,d), res, d)
                    self.day += 1
        
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

