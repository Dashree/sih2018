from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
#from django.contrib import messages
from .forms import OptionsPage, LoginPage
from django.contrib.auth import authenticate, login
from django.conf import settings
from .calculate import calculate
from .management.commands.videoProcessing import VideoProcessing, Demuxer
from .models import VideoUpload, ImageUpload
import os
from datetime import datetime

def sendvideo(from_date, to_date, from_time, to_time, Fps, Res):
    pathlist = []
    pathlist = VideoUpload.objects.filter(uploadDate__range=[from_date, to_date], resfield = Res, fpsfield = Fps)     
    pathlist = [os.path.join(media_path, str(path.uploadDate),'videos' ,path.uploadPath) for path in pathlist]
    print(pathlist)
    #pathlist.append(pathlist.uploadpath)
    sec = calculate(day.days, from_time.hour, from_time.minute, to_time.hour, to_time.minute, Fps)
    outvideo = Demuxer(pathlist, Res, Fps)
    videopath = outvideo.multipleDemuxInput()
    videopath = videopath.replace(media_path, '/media')

def sendimage(from_date, to_date, from_time, to_time, dur, Fps, Res):
    start_time  = datetime.combine(from_date, from_time)
    end_time = datetime.combine(to_date, to_time)
    dur = datetime.timedelta(hour=dur.hour, min=dur.min)

    def calc_intermediate_time(start_time, end_time, dur):
        st = start_time
        while st < end_time:
            yield st,st+dur
            st = st + dur

    imagelist = []
    for t_start, t_end in calc_intermediate_time(start_time, end_time, dur):
        imagelist.append(ImageUpload.objects.filter(imgDate__in=[t_start.date(), t_end.date()], 
                    imgTime__in =[t_start.time(), t_end.time()]))
        
    pathimage = [os.path.join(media_path, str(path.uploadDate),'images' ,pathimage.upload) for path in imagelist]
    outimage = ConcatImg(pathimage, Res, Fps)
    videopath = outimage.multipleDemuxInput()
    videopath = videopath.replace(media_path, '/media')

def index(request):
    return HttpResponse("Hello, world. You're at the GrazerFeed index.")

def option(request):
    if request.method == 'POST':

        form = OptionsPage(request.POST)
        if form.is_valid():
            from_time = form.cleaned_data['fromtime']
            to_time = form.cleaned_data['totime']
            from_date = form.cleaned_data['fromdate']
            to_date = form.cleaned_data['todate']
            Res = form.cleaned_data['res']
            Fps = form.cleaned_data['fps']
            dur = form.cleaned_data['duration']
            day = to_date - from_date
            media_path = os.path.join(settings.BASE_DIR, 'media') 
            if (dur.minute == 30):
                sendvideo(from_date, to_date, from_time, to_time, Fps, Res)
            else:
                sendimage(from_date, to_date, from_time, to_time, dur, Fps, Res)
            
            return render(request, 'GrazerFeed/VideoPage.html', context={'videopath' : videopath , 'start' : sec[0], 'end' : sec[1]})
        else:
            print('form is not valid')
            return render(request, 'GrazerFeed/OptionsPage.html', { 'form': OptionsPage()}, {'error_message' : 'Invalid field values'})
    else:
        return render(request, 'GrazerFeed/OptionsPage.html', { 'form': OptionsPage()})

def loginuser(request):
    if request.method == 'POST':
        print('In get')
        form = LoginPage(request.POST)
        if form.is_valid():
            print('In is_valid()')
            username = form.cleaned_data['Username']
            print('Username = ', username)
            password = form.cleaned_data['Password']
            print('Password = ', password)
            user = authenticate(username=username, password=password)
            print('Authenticated')
            if user is not None:
                print('not none')
                if user.is_active:
                    print('active')
                    login(request, user)
                    return render(request, 'GrazerFeed/OptionsPage.html', { 'form': OptionsPage()})
    else:
        return render(request, 'GrazerFeed/LoginPage.html', { 'form': LoginPage()})        
