from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('video', views.video, name='video'),
    path('Options', views.option, name='TrialOptionsForm'),
    url(r'^$', views.index, name='index'),
]
