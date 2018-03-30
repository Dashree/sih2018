from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Options', views.option, name='OptionsPage'),
    path('Login', views.loginuser, name="LoginPage")
]