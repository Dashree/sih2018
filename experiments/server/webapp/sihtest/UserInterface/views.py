from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from .forms import OptionsForm, LoginForm
from django.conf import settings
from .calculate import calculate

def index(request):
    return HttpResponse("UserInterface Created")

def video(request):
    return render(request, 'UserInterface/OptionsPage.html')

def option(request):
    if request.method == 'POST':
        form = OptionsForm(request.POST)
        if form.is_valid():
            list_date = form.check_date()
            fromdate = list_date[0]
            todate = list_date[1]
            fromtime = form.cleaned_data['FromTime']
            print(fromtime)
            totime = form.cleaned_data['ToTime']
            print(totime)
            res = form.cleaned_data['Resolution']
            fps = form.cleaned_data['FPS']
            day = (todate) - (fromdate)
            hour1 = str(fromtime).split(':')[0]
            min1 = str(fromtime).split(':')[1]
            hour2 = str(totime).split(':')[0]
            min2 = str(totime).split(':')[1]
            sec = calculate(int(day.days), int(hour1), int(min1), int(hour2), int(min2), int(fps))
            videopath = settings.MEDIA_URL + str(datetime.strptime(fromdate, '%d%b%Y') + '/videos/video_' + str(res) + '_' + str(fps) + '.webm' #write logic for convert 10-3-2018 to 03OCT2018
            #videopath = settings.STATIC_URL + str(fromdate) + '/videos/video_' + str(res) + '_' + str(fps) + '.webm'
            print(videopath)
            #return render(request, 'UserInterface/TrialOptionsForm.html', context={'videopath' : videopath})#, 'start' : str(fromtime).split(':')[2], 'end' : str(totime).split(':')[2]})
            return render(request, 'UserInterface/playvideo.html', context={'videopath' : videopath, 'start' : sec[0], 'end' : sec[1]})
    else:
        form = OptionsForm()
        return render(request, 'UserInterface/OptionsPage.html', {'form' : form})

def loginuser(request):
    if request.method == 'POST':
        print('In POST')
        form = LoginForm(request.POST)
        if form.is_valid():
            print('In is_valid()')
            username = form.cleaned_data['Username']
            print('Username = ', username)
            password = form.cleaned_data['Password']
            print('Password = ', password)
            user = authenticate(username=username, password=password)
            print('user', user)
            if user is not None:
                print('In user in not none')
                if user.is_active:
                    print('In user is active')
                    login(request, user)
                    print('Login Successful')
                    return render(request, 'UserInterface/OptionsPage.html', {'form' : OptionsForm()})
                    #return option(request)
                else:
                    return render(request, 'UserInterface/LoginPage.html', {'error_message': 'Account has been disabled'}, status=401)
            else:
                return render(request, 'UserInterface/TrialOptionsForm.html')
    else:
        form = LoginForm()
    return render(request, 'UserInterface/LoginPage.html', {'form' : form})
