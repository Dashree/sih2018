import os, shutil, subprocess
import os.path
from datetime import datetime

from django.conf import settings
import moviepy.editor as moviepy

from PIL import Image


class VideoProcessing(object):
    WIDTH = [640, 1280, 1920, 2560]
    HEIGHT = [360, 720, 1080, 1440]
    def __init__(self, imageSrc):
        self.imageSrc = imageSrc
        self.width = [640, 1280, 1920, 2560]
        self.height = [360, 720, 1080, 1440]
        self.duration = [0.5, 1, 2, 3]
        self.imgQ = 0
        self.singleVideoList = list()
        self.outVideoList = list()

    @classmethod
    def getMatchingWidth(cls, height):
        for ht, wd in zip(cls.HEIGHT, cls.WIDTH):
            if ht == height:
                return wd
            
    def getDate(self):
        imageName = os.path.basename(self.imageSrc)
        list1 = imageName.split("_")
        self.dateStr = list1[1]
        imgDate = datetime.strptime(self.dateStr, '%d%b%Y').date()
        return imgDate
        
    def getTime(self):
        imageName = os.path.basename(self.imageSrc)
        list2 = imageName.split("_")
        self.dateStr = list2[1]
        imgTime = datetime.strptime(self.dateStr, '%d%b%Y').time()
        return imgTime
    
    def copyImage(self):
        imgDate = self.getDate()
        self.dateImagePath = os.path.join('media', str(imgDate), 'images')
        print(self.dateImagePath)
        self.destImagePath = os.path.join(settings.BASE_DIR, self.dateImagePath, os.path.basename(self.imageSrc))
        directory = os.path.dirname(self.destImagePath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.copy(self.imageSrc, self.destImagePath)

    def make_video_filename(self, prefix, res, d):
        return '%s_%d_%d.webm'%(prefix, res, d)
                
    def createVideo(self):
        self.copyImage()
        img = Image.open(self.imageSrc)
        width1, height1 = img.size  
        ffmpeg_params = ['-lossless','1']
        fps = 11
        for width, height in zip(self.width, self.height):
            for d in self.duration:
                clip = moviepy.ImageClip(self.imageSrc, duration=d)
                videofilename= self.make_video_filename('singleVideo', height, d)
                if (width1 <= 360 or height1 <=360):
                    clip.write_videofile(videofilename, fps=fps, codec='libvpx-vp9', ffmpeg_params=ffmpeg_params)
                    self.imgQ = 1
                else:
                    clip.resize(newsize=(width,height)).write_videofile(videofilename, fps=fps, codec='libvpx-vp9', ffmpeg_params=ffmpeg_params)
                self.singleVideoList.append((height, d, videofilename))
    
    def getImagePath(self):
        return self.destImagePath
    
    def getVideosPath(self):
        videoslist = list()
        for res in self.height:
            for d in self.duration:
                videopath = os.path.join(settings.BASE_DIR, 'media', str(self.getDate()),'videos', self.make_video_filename('video', res, d))
                videoslist.append((res,d, videopath))
        return videoslist
        
    def concat(self, file, res, d): 
        command = ['ffmpeg','-y',
               '-f', 'concat',
               '-safe', '0',
               '-i', file,
               '-c', 'copy',
               '-flags', 'global_header',
               'video1.webm']
        subprocess.run(command)
        videoname = 'video_%d_%d.webm'%(res,d)
        os.remove(os.path.join(settings.BASE_DIR, 'media', str(self.getDate()),'videos', videoname))
        os.rename('video1.webm', videoname)
        self.copyVideo(videoname)
        self.outVideoList.append((res,d, file))
    
    def demuxerInput(self):
        dateVideoPath = self.getDateVideoPath()
        for height, d, videopath in self.singleVideoList:
            videoname = self.make_video_filename('video', height, d)
            singlevideoname = self.make_video_filename('singleVideo', height, d)
                          
            if(os.path.exists(os.path.join(settings.BASE_DIR,dateVideoPath,videoname))):
                ffmpeg_cmd = self.make_video_filename('concat', height, d) + '.txt'
                with open(ffmpeg_cmd,'w') as f:
                    f.write('file %s\n'%self.videoPath(videoname))
                    f.write('file %s' % videopath)
                self.concat(ffmpeg_cmd, height, d)
            else:
                os.rename(singlevideoname,videoname)
                self.videoPath(videoname)
                self.copyVideo(videoname)
    
    
    def getDateVideoPath(self):
        return os.path.join('media',str(self.getDate()), 'videos')
                          
    def videoPath(self,videoName):
        dateVideoPath = self.getDateVideoPath() 
        destVideoPath = os.path.join(settings.BASE_DIR, dateVideoPath, videoName)
        return destVideoPath
                          
    def copyVideo(self, videoName):
        fullpath = os.path.join(settings.BASE_DIR,self.getDateVideoPath())
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        shutil.move(videoName, self.videoPath(videoName))


class Demuxer(object):
    def __init__(self, nVideo,res,d):
        self.nVideo = nVideo
        self.res = res
        self.d = d
    
    def multipleDemuxInput(self):
        with open('nconcat.txt','w') as f:
            for videoname in self.nVideo:
                f.write("file %s\n" % videoname) 
        self.vConcat('nconcat.txt')
        return self.destVideoPath1
    
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
    

