from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('video', views.video, name='video'),
    path('Options', views.option, name='TrialOptionsForm'),
    path('Login', views.login, name='LoginPage')
   # url('', views.index, name='index'),
]
