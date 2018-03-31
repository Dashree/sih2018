import shutil,os.path,tempfile

import moviepy.editor as moviepy

from django.conf import settings

from .management.commands.videoProcessing import VideoProcessing

def interval(source,dur,res):
    tempfile.mkdtemp(prefix = Grz)
    for files in source:
        shutil.copy(files,tempfile.gettempdir())

    clip = moviepy.ImageSequenceClip('temp', fps = dur)
    clip.resize(newsize=(VideoProcessing.getMatchingWidth(res),res)).write_videofile("output.webm", fps=len(source),codec='libvpx-vp9')

    outputpath = os,path.join(settings.BASE_DIR, 'media', 'output_interval')
    shutil.move("output.webm", outputpath)

