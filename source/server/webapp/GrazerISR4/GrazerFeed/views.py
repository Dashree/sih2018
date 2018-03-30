from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .forms import OptionsPage#, LoginForm

def index(request):
    return HttpResponse("Hello, world. You're at the GrzerFeed index.")

def option(request):
    '''if request.method == 'POST':
        form = OptionsPage(request.POST)
        if form.is_valid():
            list_date = form.check_date()
            if list_date == None:
                messages.error(request, 'Invalid from and to date pair')
                return render(request, 'GrazerFeed/OptionsPage.html', { 'form': OptionsPage()})
            fromdate = list_date[0]
            todate = list_date[1]
    else:'''
    print ('in option')
    return render(request, 'GrazerFeed/OptionsPage.html', { 'form': OptionsPage()})