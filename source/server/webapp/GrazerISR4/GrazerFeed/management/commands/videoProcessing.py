import os, shutil, subprocess
import os.path
from datetime import datetime

from django.conf import settings
import moviepy.editor as moviepy

from PIL import Image

class VideoProcessing(object):
    def __init__(self, imageSrc):
        self.imageSrc = imageSrc
        self.width = [640, 1280, 1920, 2560]
        self.height = [360, 720, 1080, 1440]
        self.duration = [0.5, 1, 2, 3]
        self.imgQ = 0

    def getDate(self):
        imageName = os.path.basename(self.imageSrc)
        list1 = imageName.split("_")
        self.dateStr = list1[1]
        self.imgDate = datetime.strptime(self.dateStr, '%d%b%Y').date()
        return self.imgDate
    
    def getTime(self):
        imageName = os.path.basename(self.imageSrc)
        list2 = imageName.split("_")
        self.dateStr = list2[1]
        self.imgTime = datetime.strptime(self.dateStr, '%d%b%Y').time()
        return self.imgTime
    
    def copyImage(self):
        self.getDate()
        self.dateImagePath = os.path.join('media', str(self.imgDate), 'images')
        print(self.dateImagePath)
        self.destImagePath = os.path.join(settings.BASE_DIR, self.dateImagePath, os.path.basename(self.imageSrc))
        directory = os.path.dirname(self.destImagePath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.copy(self.imageSrc, self.destImagePath)
    
    def createVideo(self):
        self.copyImage()
        if(self.imageSrc is not None):
            img = Image.open(self.imageSrc)
            width1, height1 = img.size
            
            for res in range(len(self.width)):
                for d in range(len(self.duration)):
                    clip = moviepy.ImageClip(self.imageSrc, duration=self.duration[d])
                    if (width1 <= 360 or height1 <=360):
                        clip.write_videofile('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]), fps=11, codec='libvpx-vp9', ffmpeg_params=['-lossless','1'])
                        self.imgQ = 1
                    else:
                        clip.resize(newsize=(self.width[res],self.height[res])).write_videofile('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]), fps=11, codec='libvpx-vp9', ffmpeg_params=['-lossless','1'])
    
    def getImagePath(self):
        return self.destImagePath

    def getVideosPath(self):
        return os.path.join(settings.BASE_DIR, self.dateVideoPath)
    
    
    def concat(self, file, res, d): 
        command = ['ffmpeg','-y',
               '-f', 'concat',
               '-safe', '0',
               '-i', file,
               '-c', 'copy',
               '-flags', 'global_header',
               'video1.webm']
        subprocess.run(command) 
        os.remove(os.path.join(settings.BASE_DIR, 'media', str(self.imgDate),'videos', 'video_%d_%d.webm'%(self.height[res],self.duration[d])))
        os.rename('video1.webm', 'video_%d_%d.webm'%(self.height[res],self.duration[d]))
        self.copyVideo('video_%d_%d.webm'%(self.height[res],self.duration[d]))
    
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
    
    
    def videoPath(self,videoName):
        self.dateVideoPath = 'media/' + str(self.imgDate) + '/videos'
        self.destVideoPath = os.path.join(settings.BASE_DIR, os.path.join(self.dateVideoPath, videoName))
        return self.destVideoPath
    
    def copyVideo(self, videoName):
        fullpath = os.path.join(settings.BASE_DIR,self.dateVideoPath)
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        shutil.move(videoName, self.destVideoPath)


class Demuxer(object):
    def __init__(self, nVideo,res,d):
        self.nVideo = nVideo
        self.res = res
        self.d = d
    
    def multipleDemuxInput(self):
        with open('nconcat.txt','w') as f:
            for videoname in self.nVideo:
                f.write("file %s"%os.path.join(settings.BASE_DIR,videoname,"\n")) 
        self.vConcat('nconcat.txt')
    
    def multipleCopyVideo(self,videoNames):
        self.destVideoPath1 = os.path.join(settings.BASE_DIR, "media", "output", videoNames)
        directory = os.path.dirname(self.destVideoPath1)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.move(videoNames, self.destVideoPath1)

    def vConcat(self, file):
        command = ['ffmpeg','-y',
               '-f', 'concat',
               '-safe', '0',
               '-i', file,
               '-c', 'copy',
               '-flags', 'global_header',
               'video1.webm']
        subprocess.run(command)
        os.rename('video1.webm', 'outputvideo_%d_%d.webm'%(self.res,self.d))
        self.multipleCopyVideo('outputvideo_%d_%d.webm'%(self.res,self.d)) 

        
