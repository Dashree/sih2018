from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
#from django.contrib import messages
from .forms import OptionsPage, LoginPage

def index(request):
    return HttpResponse("Hello, world. You're at the GrzerFeed index.")

def option(request):
    if request.method == 'POST':
        form = OptionsPage(request.POST)
        if form.is_valid():
            from_time = form.cleaned_data['fromtime']
            to_time = form.cleaned_data['totime']
            from_date = form.cleaned_data['fromdate']
            to_date = form.cleaned_data['todate']
            Res = form.cleaned_data['res']
            FPS = form.cleaned_data['fps']
            return render(request, 'GrazerFeed/VideoPage.html')
        else:
            return render(request, 'GrazerFeed/OptionsPage.html', { 'form': OptionsPage()})
    else:
        return render(request, 'GrazerFeed/OptionsPage.html', { 'form': OptionsPage()})

def loginuser(request):
    if request.method == 'POST':
        form = LoginPage(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'GrazerFeed/OptionsPage.html', { 'form': OptionsPage()})
    else:
        return render(request, 'GrazerFeed/LoginPage.html', { 'form': LoginPage()})        