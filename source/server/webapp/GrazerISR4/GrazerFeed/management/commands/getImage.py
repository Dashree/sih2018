from datetime import datetime,timedelta
import os
import os.path

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from django.core.management.base import BaseCommand
from GrazerFeed.models import ImageUpload, VideoUpload

from PIL import Image, ImageChops
from .videoProcessing import VideoProcessing, getImageTimeStamp

def calc_intermediate(startimg, starttime, endimage): 
    def time_range(start, end, step):
        s = start
        while (s < end):
            yield s
            s = s + step
            
    if startimg == None:
        yield endimage
        raise StopIteration

    
    endtime = getImageTimeStamp(endimage)
    timediff = endtime - starttime
    tdiff = timedelta(minutes=45)
    if timediff > tdiff :
        img1 = Image.open(startimg)
        img2 = Image.open(endimage)

        t_step = timedelta(minutes=30)
        rangeAlpha = 10

        basedir = os.path.dirname(endimage)
        for t in time_range(starttime, endtime, t_step):
            alpha = (t-starttime)/(endtime-starttime)
            imgBlend = ImageChops.blend(img1,img2,alpha)
            imgname = t.strftime("3DIMG_%d%b%Y_%H%M_L1C_ASIA_MER_IR1.JPG")
            imgname = os.path.join(basedir, imgname)
            imgBlend.save(imgname)
            print("Intermediate image : %s" % imgname)
            yield imgname
    else:
        yield endimage
        
    

class Handler(PatternMatchingEventHandler):
    def __init__(self):
        super(Handler, self).__init__(patterns=['*.jpg', '*.png'],
            ignore_directories=True, case_sensitive=False)

    def convert_image(self, srcpath):
        videoP = VideoProcessing(srcpath)
        videoP.createVideo()
        newimage = ImageUpload(upload = videoP.destImagePath, imgDateTime = videoP.getTimeStamp())
        newimage.save()
        videoP.demuxerInput()
        videoList = videoP.getVideosPath()
        for res, fps, videopath in videoList:
            newVideo, created = VideoUpload.objects.get_or_create(resfield=res,fpsfield=fps,uploadDate=videoP.getDate(), uploadtime = videoP.getTime())
            newVideo.uploadPath = videopath
            newVideo.save()

    def convert_image_with_intermediate(self, newimagepath):
        try:
            last_img = ImageUpload.objects.latest('imgDateTime')
            lastdt = last_img.imgDateTime
            last_img= last_img.upload
        except Exception as exp:
            import pdb
            pdb.set_trace()
    
            last_video = None
            lastdt = None

        for path in calc_intermediate(last_img, lastdt, newimagepath):
            self.convert_image(path)
        
    def on_created(self,event):
        self.convert_image_with_intermediate(event.src_path)
        
class Command(BaseCommand):
    def start_observer(self):
        observer = Observer()
        event_handler = Handler()
        observer.schedule(event_handler,'/mnt/c/images', recursive=True)
        observer.start()
        observer.join()

    def handle(self, **options):
        #self.start_observer()
        handler = Handler()
        handler.convert_image_with_intermediate('/mnt/c/images/3DIMG_01SEP2017_1130_L1C_ASIA_MER_IR1.jpg')
