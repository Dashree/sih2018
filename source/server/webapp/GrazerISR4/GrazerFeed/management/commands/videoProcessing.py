import os, shutil
from datetime import datetime
from django.conf import settings

class videoProcessing():
    def __init__(self, imageSrc):
        self.imageSrc = imageSrc
        self.width = [640, 1280, 1920, 2560]
        self.height = [360, 720, 1080, 1440]
        self.duration = [0.5, 1, 2, 3]

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
        
    
    
vP = videoProcessing('/mnt/c/Hackathon_Images/3DIMG_01SEP2017_0000_L1C_ASIA_MER_IR1.jpg')
vP.getDate()
vP.copyImage()
