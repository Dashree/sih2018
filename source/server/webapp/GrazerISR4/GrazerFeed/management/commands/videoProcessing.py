import os, shutil, subprocess
from datetime import datetime
from django.conf import settings
import moviepy.editor as moviepy

class VideoProcessing():
    def __init__(self, imageSrc):
        self.imageSrc = imageSrc
        self.width = [640, 1280, 1920, 2560]
        self.height = [360, 720, 1080, 1440]
        self.duration = [0.5, 1, 2, 3]

    def getDate(self):
        imageName = os.path.basename(self.imageSrc)
        list = imageName.split("_")
        self.dateStr = str(list[1]);
        conv = datetime.strptime(self.dateStr, '%d%b%Y')
        self.date = conv.date().strftime('%d-%m-%Y')
        return self.date
    
    def copyImage(self):
        self.getDate()
        self.dateImagePath = 'media/' + self.date + '/images'
        print(self.dateImagePath)
        self.destImagePath = os.path.join(settings.BASE_DIR, os.path.join(self.dateImagePath, os.path.basename(self.imageSrc)))
        directory = os.path.dirname(self.destImagePath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.copy(self.imageSrc, self.destImagePath)
    
    def createVideo(self):
        self.copyImage()
        for res in range(len(self.width)):
            for d in range(len(self.duration)):
                clip = moviepy.ImageClip(self.imageSrc, duration=self.duration[d])
                clip.write_videofile('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]), fps=11, codec='libvpx-vp9', ffmpeg_params=['-lossless','1'])
    
    def getImagePath(self):
        return self.destImagePath    
    
    def demuxerInput(self):
         for res in range(len(self.width)):
            for d in range(len(self.duration)):
                if(os.path.exists(os.path.join(settings.BASE_DIR,'media/%s/videos/'%self.date,os.path.join('video_%d_%d.webm'%(self.height[res],self.duration[d]))))):
                   print(self.videoPath('video_%d_%d.webm'%(self.height[res],self.duration[d]))) 
                   with open('concat_%d_%d.txt'%(res,d),'w') as f:
                       f.write('file %s'%self.videoPath('video_%d_%d.webm'%(self.height[res],self.duration[d])))
                       f.write('\n'+'file singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]))
                   self.concat('concat_%d_%d.txt'%(res,d), res, d)
                else:
                    os.rename('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]),'video_%d_%d.webm'%(self.height[res],self.duration[d]))
                    self.videoPath('video_%d_%d.webm'%(self.height[res],self.duration[d]))
                    self.copyVideo('video_%d_%d.webm'%(self.height[res],self.duration[d]))
    
    def concat(self, file, res, d): 
        command = ['ffmpeg','-y',
               '-f', 'concat',
               '-safe', '0',
               '-i', file,
               '-c', 'copy',
               '-flags', 'global_header',
               'video1.webm']
        subprocess.run(command)
        os.remove(os.path.join(settings.BASE_DIR, os.path.join('media/' + self.date + '/videos', 'video_%d_%d.webm'%(self.height[res],self.duration[d]))))
        os.rename('video1.webm', 'video_%d_%d.webm'%(self.height[res],self.duration[d]))
        self.copyVideo('video_%d_%d.webm'%(self.height[res],self.duration[d]))
    
    def videoPath(self,videoName):
        self.dateVideoPath = 'media/' + self.date + '/videos'
        self.destVideoPath = os.path.join(settings.BASE_DIR, os.path.join(self.dateVideoPath, videoName))
        return self.destVideoPath
    
    def copyVideo(self, videoName):
        if not os.path.exists(os.path.join(settings.BASE_DIR,self.dateVideoPath)):
            os.makedirs(os.path.join(settings.BASE_DIR,self.dateVideoPath))
        shutil.move(videoName, self.destVideoPath)

        
