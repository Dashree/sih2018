from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm

def index(request):
    return HttpResponse("UserInterface Created")

def video(request):
    return render(request, 'UserInterface/temp.html')

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['your_name']
            return HttpResponse(date)
        else:
            return HttpResponse('No validation done')
    else:
        form = NameForm()
    return render(request, 'UserInterface/temp.html', {'form':form})