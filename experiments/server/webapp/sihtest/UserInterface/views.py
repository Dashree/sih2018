from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from .forms import OptionsForm

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
            totime = form.cleaned_data['ToTime']
            res = form.cleaned_data['Resolution']
            fps = form.cleaned_data['FPS']
            return render(request, 'UserInterface/' + str(fromdate) + '/' + str(res) + '/' + str(fps) + '/TrialVideo.html')
    else:
        form = OptionsForm()
    return render(request, 'UserInterface/TrialOptionsForm.html', {'form' : form})