import os, shutil
from datetime import datetime
from django.conf import settings
import moviepy.editor as moviepy
from PIL import Image 

class VideoProcessing():
    def __init__(self, imageSrc):
        self.imageSrc = imageSrc
        self.width = [640, 1280, 1920, 2560]
        self.height = [360, 720, 1080, 1440]
        self.duration = [0.25, 0.5, 1, 2]

    def getDate(self):
        imageName = os.path.basename(self.imageSrc)
        list = imageName.split("_")
        self.dateStr = str(list[1]);
        print(str(list[1]));
        conv = datetime.strptime(self.dateStr, '%d%b%Y')
        self.date = conv.date().strftime('%d-%m-%Y')
    
    
    def copyImage(self):
        self.dateImagePath = 'media/' + self.date + '/images'
        print(self.dateImagePath)
        self.destImagePath = os.path.join(settings.BASE_DIR, os.path.join(self.dateImagePath, os.path.basename(self.imageSrc)))
        directory = os.path.dirname(self.destImagePath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.copy(self.imageSrc, self.destImagePath)

    def createVideo(self):
        self.copyImage()
        im = Image.open(self.imageSrc)
        width1, height1 = im.size
        for res in range(len(self.width)):
            for d in range(len(self.duration)):
                clip = moviepy.ImageClip(self.imageSrc, duration=self.duration[d])
                if(width1 <= 360 or height1 <= 360):
                    clip.write_videofile('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]), fps=11, codec='libvpx-vp9', ffmpeg_params=['-lossless','1'])
                else:
                    clip.resize(newsize=(self.width[res],self.height[res])).write_videofile('singleVideo_%d_%d.webm'%(self.height[res],self.duration[d]), fps=11, codec='libvpx-vp9', ffmpeg_params=['-lossless','1'])  
    
    
vP = videoProcessing('/mnt/c/Hackathon_Images/3DIMG_01SEP2017_0000_L1C_ASIA_MER_IR1.jpg')
vP.getDate()
vP.createVideo()
