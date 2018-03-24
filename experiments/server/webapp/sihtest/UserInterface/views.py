from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
#from .forms import NameForm

def index(request):
    return HttpResponse("UserInterface Created")

def video(request):
    return render(request, 'UserInterface/temp.html')

def get_name(request):
    if request.method == 'POST':
        print('Inside POST method')
        data = request.POST['FromDate']
        print(data)
    return render(request, 'UserInterface/OptionsPage.html')