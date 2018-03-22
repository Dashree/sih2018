from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("UserInterface Created")

def video(request):
    return render(request, 'UserInterface/Page2.html')