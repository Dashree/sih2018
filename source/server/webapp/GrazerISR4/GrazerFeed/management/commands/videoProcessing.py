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
        self.imgDate = datetime.strptime(self.dateStr, '%d%b%Y').date()
        return self.imgDate
    
    def copyImage(self):
        self.getDate()
        self.dateImagePath = 'media/' + str(self.imgDate) + '/images'
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
                clip.resize(newsize=(self.width[res],self.height[res])).write_videofile('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]), fps=11, codec='libvpx-vp9', ffmpeg_params=['-lossless','1'])
    
    def getImagePath(self):
        return self.destImagePath

    def getVideosPath(self):
        return os.path.join(settings.BASE_DIR, self.dateVideoPath)
    
    def demuxerInput(self):
         for res in range(len(self.width)):
            for d in range(len(self.duration)):
                if(os.path.exists(os.path.join(settings.BASE_DIR,'media/%s/videos/'%str(self.imgDate),os.path.join('video_%d_%d.webm'%(self.height[res],self.duration[d]))))):
                   print(self.videoPath('video_%d_%d.webm'%(self.height[res],self.duration[d]))) 
                   with open('concat_%d_%d.txt'%(res,d),'w') as f:
                       f.write('file %s'%self.videoPath('video_%d_%d.webm'%(self.height[res],self.duration[d])))
                       f.write('\n'+'file singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]))
                   self.concat('concat_%d_%d.txt'%(res,d), res, d)
                else:
                    os.rename('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]),'video_%d_%d.webm'%(self.height[res],self.duration[d]))
                    self.videoPath('video_%d_%d.webm'%(self.height[res],self.duration[d]))
                    self.copyVideo('video_%d_%d.webm'%(self.height[res],self.duration[d]))

    def multipleDemuxInput(self, nVideo,res,d):
        with open('nconcat.txt','a') as f:
            for n in range(len(nVideo)):
                f.write("file '%s'"%nVideo[n]+"\n") #append base path
        self.concat('nconcat.txt',res,d)#here res and d is user input
        
    
    def multipleCopyVideo(self,videoNames):
        self.destVideoPath1 = os.path.join(settings.BASE_DIR, os.path.join('media/output/', videoNames))
        directory = os.path.dirname(self.destVideoPath1)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.move(videoNames, self.destVideoPath1)
    
    def concat(self, file, res, d): 
        command = ['ffmpeg','-y',
               '-f', 'concat',
               '-safe', '0',
               '-i', file,
               '-c', 'copy',
               '-flags', 'global_header',
               'video1.webm']
        subprocess.run(command)
        if(file == 'nconcat.txt'):
            os.rename('video1.webm', 'outputvideo_%d_%d.webm'%(self.height[res],self.duration[d]))
            self.multipleCopyVideo('outputvideo_%d_%d.webm'%(self.height[res],self.duration[d])) 
            os.remove('nconcat.txt')
        else:
            os.remove(os.path.join(settings.BASE_DIR, os.path.join('media/' + str(self.imgDate) + '/videos', 'video_%d_%d.webm'%(self.height[res],self.duration[d]))))
            os.rename('video1.webm', 'video_%d_%d.webm'%(self.height[res],self.duration[d]))
            self.copyVideo('video_%d_%d.webm'%(self.height[res],self.duration[d]))
    
    def videoPath(self,videoName):
        self.dateVideoPath = 'media/' + str(self.imgDate) + '/videos'
        self.destVideoPath = os.path.join(settings.BASE_DIR, os.path.join(self.dateVideoPath, videoName))
        return self.destVideoPath
    
    def copyVideo(self, videoName):
        if not os.path.exists(os.path.join(settings.BASE_DIR,self.dateVideoPath)):
            os.makedirs(os.path.join(settings.BASE_DIR,self.dateVideoPath))
        shutil.move(videoName, self.destVideoPath)

        
