from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('video', views.video, name='video'),
    path('Options', views.option, name='OptionsPage'),
    path('Login', views.loginuser, name='LoginPage')
    #url('', views.index, name='index'),
]
