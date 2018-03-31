from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
#from django.contrib import messages
from .forms import OptionsPage, LoginPage
from django.contrib.auth import authenticate, login
from django.conf import settings
from .calculate import calculate
from .management.commands.videoProcessing import VideoProcessing, Demuxer
from .models import VideoUpload

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
            day = to_date - from_date
            pathlist = []
            pathlist = VideoUpload.objects.filter(uploadDate__range=[from_date, to_date])
            pathlist = [path.uploadPath for path in pathlist]
            #pathlist.append(pathlist.uploadpath)
            sec = calculate(day.days, from_time.hour, from_time.minute, to_time.hour, to_time.minute, Fps)
            #videopath = settings.MEDIA_URL + str(from_date) + '/videos/video_' + str(Res) + '_' + str(Fps) + '.webm'
            videopath = Demuxer(pathlist, Res, Fps)
            return render(request, 'GrazerFeed/VideoPage.html', context={'videopath' :  videopath.multipleDemuxInput(), 'start' : sec[0], 'end' : sec[1]})
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
