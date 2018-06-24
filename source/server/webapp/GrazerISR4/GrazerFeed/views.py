import os
from datetime import datetime, timedelta

#from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from .forms import OptionsPage, LoginPage
from .calculate import calculate
from .management.commands.videoProcessing import VideoProcessing, Demuxer
from .models import VideoUpload, ImageUpload
from .intervalimages import interval
    

def sendimage(from_date, to_date, from_time, to_time, interval, Fps, Res):
    start_time  = datetime.combine(from_date, from_time)
    end_time = datetime.combine(to_date, to_time)
    interval = timedelta(hours=interval.hour, minutes=interval.minute)

    def calc_intermediate_time(start_time, end_time, interval):
        st = start_time
        while st < end_time:
            yield st,st+interval
            st = st + interval

    imagelist = []
    for t_start, t_end in calc_intermediate_time(start_time, end_time, interval):
        for img in ImageUpload.objects.filter(imgDate__in=[t_start.date(), t_end.date()], 
                    imgTime__in =[t_start.time(), t_end.time()]):
            imagelist.append(img)
        
    pathimage = [path.upload for path in imagelist]
    outimage = interval(pathimage, Fps, float(Res))
    return outimage
    #videopath = videopath.replace(media_path, '/media')

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
            interval = form.cleaned_data['interval']
            day = to_date - from_date
            media_path = os.path.join(settings.BASE_DIR, 'media') 
            if (interval.minute == 30):
                pathlist = []
                pathlist = VideoUpload.objects.filter(uploadDateTime__range=[from_date, to_date], resfield = Res, fpsfield = Fps)     
                pathlist = [os.path.join(settings.MEDIA_ROOT, str(path.uploadDateTime.date()),'videos' ,path.uploadPath) for path in pathlist]
                #pathlist.append(pathlist.uploadpath)
                sec = calculate(day.days, from_time.hour, from_time.minute, to_time.hour, to_time.minute, Fps)
                outvideo = Demuxer(pathlist, Res, Fps)
                videopath = outvideo.multipleDemuxInput()
            else:
                sec = (0, 1000000)
                videopath = sendimage(from_date, to_date, from_time, to_time, interval, float(Fps), Res)
                
            finalpath = videopath.replace(media_path, '/media')
            return render(request, 'GrazerFeed/VideoPage.html', context={'videopath' : finalpath , 'start' : sec[0], 'end' : sec[1]})
        else:
            print("form error")
            print(form.errors)
            return render(request, 'GrazerFeed/OptionsPage.html', { 'form': OptionsPage()}, {'error_message' : 'Invalid field values'})
    else:
        return render(request, 'GrazerFeed/OptionsPage.html', { 'form': OptionsPage()})

def loginuser(request):
    if request.method == 'POST':
        form = LoginPage(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('OptionsPage')
    else:
        return render(request, 'GrazerFeed/LoginPage.html', { 'form': LoginPage()})        
