from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
#from django.contrib import messages
from .forms import OptionsPage, LoginPage
from django.contrib.auth import authenticate, login
from django.conf import settings
from .calculate import calculate
from .management.commands.videoProcessing import VideoProcessing

def index(request):
    return HttpResponse("Hello, world. You're at the GrazerFeed index.")

def option(request):
    if request.method == 'POST':
        form = OptionsPage(request.POST)
        if form.is_valid():
            from_time = form.cleaned_data['fromtime']
            to_time = form.cleaned_data['totime']
            list_date = form.check_date()
            from_date = list_date[0]
            to_date = list_date[1]
            Res = form.cleaned_data['res']
            Fps = form.cleaned_data['fps']
            day = from_date - to_date
            hour1 = str(from_time).split(':')[0]
            min1 = str(from_time).split(':')[1]
            hour2 = str(to_time).split(':')[0]
            min2 = str(to_time).split(':')[1]
            pathlist = []
            for x in range(int(day.days)):
                extractdate = VideoUpload.objects.get(uploadDate = from_date)
                print(extractdate)
                pathlist.append(extractdate.uploadPath)
            sec = calculate(int(day.days), int(hour1), int(min1), int(hour2), int(min2), int(Fps))
            #videopath = settings.MEDIA_URL + str(from_date) + '/videos/video_' + str(Res) + '_' + str(Fps) + '.webm'
            videoP = VideoProcessing()
            videopath = videoP.multipleDemuxInput(pathlist, Res, Fps)
            return render(request, 'GrazerFeed/VideoPage.html', context={'videopath' : videopath, 'start' : sec[0], 'end' : sec[1]})
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
