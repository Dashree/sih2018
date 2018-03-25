from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess, time, os, sys, shutil
import moviepy.editor as moviepy
from PIL import Image
from django.conf import settings

class VideoProcessor(object):
    def __init__(self,imageSrc):
        self.imageSrc = imageSrc
        self.width = [2560, 1920, 1280, 640]
        self.height = [1440, 1080, 720, 360]
        self.duration = [0.5, 1, 2 , 3]
        self.day = 0
        self.n = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    
    
    def copyImage(self):
        imageName = os.path.basename(self.imageSrc)
        list = imageName.split("_")
        print(list[1], list[2])
        self.dateImagePath = 'media/' + str(list[1]) + '/images'
        self.destImagePath = os.path.join(settings.BASE_DIR,os.path.join(self.dateImagePath, os.path.basename(self.imageSrc)))
        directory = os.path.dirname(self.destImagePath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.copy(self.imageSrc, self.destImagePath)

    def multipleDemuxInput(self, nVideo,res,d):
        f = open('nconcat.txt','a')
        for n in range(len(nVideo)):
            f.write("file '%s'"%nVideo[n]+"\n")
        concat(nconcat.txt,res,d)#here res and d is user input

    def getImagePath(self):
        return self.destImagePath
    
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
                
                if(self.n[res][d] != 1):
                    self.concat('concat%d%d.txt'%(res,d), res, d)
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
        os.remove('video_%d_%d.webm'%(self.height[res],self.duration[d]))
        os.rename('video1.webm', 'video_%d_%d.webm'%(self.height[res],self.duration[d]))
        if(file == 'nconcat.txt'):
            os.remove('nconcat.txt')
    
    def createVideo(self):
        #imagePath = event.src_path
        #dirPath = os.path.dirname(event.src_path)
        #print(os.path.basename(event.src_path))
        self.copyImage()
        print(self.imageSrc)
        im = Image.open(self.imageSrc)
        width1, height1 = im.size
        for res in range(len(self.width)):
            for d in range(len(self.duration)):
                clip = moviepy.ImageClip(self.imageSrc, duration=self.duration[d])
                if(width1 <= 360 and height1 <= 360):
                    clip.write_videofile('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]), fps=11, codec='libvpx-vp9', ffmpeg_params=['-lossless','1'])
                else:
                    clip.resize(newsize=(self.width[res],self.height[res])).write_videofile('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]), fps=11, codec='libvpx-vp9', ffmpeg_params=['-lossless','1'])

        

